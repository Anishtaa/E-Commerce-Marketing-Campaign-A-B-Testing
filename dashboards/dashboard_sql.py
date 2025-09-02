# dashboard_sql.py

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import sqlite3

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "E-Commerce SQL Dashboard"

# ----------------------------
# Helper: Friendly campaign names
CAMPAIGN_LABELS = {
    'AcceptedCmp1': 'Campaign 1',
    'AcceptedCmp2': 'Campaign 2',
    'AcceptedCmp3': 'Campaign 3',
    'AcceptedCmp4': 'Campaign 4',
    'AcceptedCmp5': 'Campaign 5',
    'Response': 'Last Campaign'
}

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div([
    html.H1("E-Commerce SQL Dashboard", style={'textAlign':'center','color':'#003366'}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Filter by Education:"),
            dcc.Dropdown(
                id='edu-filter',
                placeholder="Select Education",
                clearable=True
            )
        ], style={'width':'45%', 'display':'inline-block','margin':'10px'}),

        html.Div([
            html.Label("Filter by Marital Status:"),
            dcc.Dropdown(
                id='mar-filter',
                placeholder="Select Marital Status",
                clearable=True
            )
        ], style={'width':'45%', 'display':'inline-block','margin':'10px'})
    ]),

    # KPI Cards
    html.Div(id='kpi-cards', style={'margin':'20px', 'display':'flex', 'justifyContent':'space-around'}),

    # Graphs
    html.Div([
        dcc.Graph(id='sql-campaign-graph'),
        dcc.Graph(id='sql-income-edu-graph')
    ])
], style={'fontFamily':'Arial, sans-serif', 'backgroundColor':'#F5F5F5','padding':'10px'})

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output('edu-filter', 'options'),
    Output('mar-filter', 'options'),
    Input('edu-filter', 'value')  # dummy input to trigger initialization
)
def initialize_dropdowns(_):
    conn = sqlite3.connect("data/marketing_campaign.db", check_same_thread=False)
    edu_opts = [{'label': e, 'value': e} for e in pd.read_sql("SELECT DISTINCT Education FROM marketing", conn)['Education']]
    mar_opts = [{'label': m, 'value': m} for m in pd.read_sql("SELECT DISTINCT Marital_Status FROM marketing", conn)['Marital_Status']]
    conn.close()
    return edu_opts, mar_opts

@app.callback(
    Output('kpi-cards', 'children'),
    Output('sql-campaign-graph', 'figure'),
    Output('sql-income-edu-graph', 'figure'),
    Input('edu-filter', 'value'),
    Input('mar-filter', 'value')
)
def update_sql_dashboard(selected_edu, selected_mar):
    # SQLite connection with thread safety
    conn = sqlite3.connect("data/marketing_campaign.db", check_same_thread=False)

    # Build WHERE clause
    filters = []
    if selected_edu:
        filters.append(f"Education='{selected_edu}'")
    if selected_mar:
        filters.append(f"Marital_Status='{selected_mar}'")
    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    # ---------------- KPI Cards ----------------
    total_df = pd.read_sql(f"SELECT COUNT(*) as cnt FROM marketing {where_clause}", conn)
    total_customers = int(total_df['cnt'][0]) if not total_df.empty else 0

    avg_df = pd.read_sql(f"SELECT AVG(Income) as avg_income FROM marketing {where_clause}", conn)
    avg_income = float(avg_df['avg_income'][0]) if not avg_df.empty else 0

    conv_df = pd.read_sql(f"""
        SELECT 
            AVG(AcceptedCmp1) as C1,
            AVG(AcceptedCmp2) as C2,
            AVG(AcceptedCmp3) as C3,
            AVG(AcceptedCmp4) as C4,
            AVG(AcceptedCmp5) as C5,
            AVG(Response) as R
        FROM marketing
        {where_clause}
    """, conn)
    overall_conversion = conv_df[['C1','C2','C3','C4','C5','R']].mean(axis=1)[0]*100 if not conv_df.empty else 0

    kpi_cards = html.Div([
        html.Div([
            html.H4("Total Customers", style={'textAlign':'center'}),
            html.H2(f"{total_customers:,}", style={'textAlign':'center'})
        ], style={'backgroundColor':'#1E90FF','color':'white','padding':'20px','borderRadius':'10px','flex':'1','margin':'10px'}),

        html.Div([
            html.H4("Average Income", style={'textAlign':'center'}),
            html.H2(f"${avg_income:,.0f}", style={'textAlign':'center'})
        ], style={'backgroundColor':'#32CD32','color':'white','padding':'20px','borderRadius':'10px','flex':'1','margin':'10px'}),

        html.Div([
            html.H4("Overall Conversion Rate", style={'textAlign':'center'}),
            html.H2(f"{overall_conversion:.2f}%", style={'textAlign':'center'})
        ], style={'backgroundColor':'#FF8C00','color':'white','padding':'20px','borderRadius':'10px','flex':'1','margin':'10px'})
    ], style={'display':'flex','justifyContent':'space-around','flexWrap':'wrap'})

    # ---------------- Campaign Conversion Graph ----------------
    ab_df = pd.read_sql(f"""
        SELECT 'AcceptedCmp1' as Campaign, AVG(AcceptedCmp1)*100 as Conversion FROM marketing {where_clause}
        UNION ALL
        SELECT 'AcceptedCmp2', AVG(AcceptedCmp2)*100 FROM marketing {where_clause}
        UNION ALL
        SELECT 'AcceptedCmp3', AVG(AcceptedCmp3)*100 FROM marketing {where_clause}
        UNION ALL
        SELECT 'AcceptedCmp4', AVG(AcceptedCmp4)*100 FROM marketing {where_clause}
        UNION ALL
        SELECT 'AcceptedCmp5', AVG(AcceptedCmp5)*100 FROM marketing {where_clause}
        UNION ALL
        SELECT 'Response', AVG(Response)*100 FROM marketing {where_clause}
    """, conn)

    # Rename campaigns to friendly labels
    ab_df['Campaign'] = ab_df['Campaign'].map(CAMPAIGN_LABELS)

    fig_campaign = px.bar(
        ab_df, x='Campaign', y='Conversion', text='Conversion',
        title="Campaign Conversion Rates (SQL)", color='Campaign',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_campaign.update_traces(texttemplate='%{text:.2f}%', textposition='outside',
                               hovertemplate='%{x}: %{y:.2f}%')
    fig_campaign.update_layout(yaxis=dict(range=[0, max(ab_df['Conversion'])*1.2 if not ab_df.empty else 10]))

    # ---------------- Income by Education ----------------
    inc_edu_df = pd.read_sql(f"""
        SELECT Education, AVG(Income) as AvgIncome
        FROM marketing
        {where_clause}
        GROUP BY Education
    """, conn)

    fig_income_edu = px.bar(
        inc_edu_df, x='Education', y='AvgIncome', text='AvgIncome',
        title="Average Income by Education (SQL)", color='Education',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_income_edu.update_traces(texttemplate='$%{text:.0f}', textposition='outside',
                                 hovertemplate='%{x}: $%{y:.0f}')

    # Close connection
    conn.close()

    return kpi_cards, fig_campaign, fig_income_edu

# ----------------------------
# Run app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
