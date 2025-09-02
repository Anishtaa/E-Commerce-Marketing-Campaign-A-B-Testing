# dashboard.py

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load cleaned data
df = pd.read_csv("data/cleaned_campaign.csv", delimiter=";")

# Map campaign columns to friendly names
campaign_map = {
    'AcceptedCmp1': 'Campaign 1',
    'AcceptedCmp2': 'Campaign 2',
    'AcceptedCmp3': 'Campaign 3',
    'AcceptedCmp4': 'Campaign 4',
    'AcceptedCmp5': 'Campaign 5',
    'Response': 'Last Campaign'
}

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "E-Commerce Marketing Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div([
    html.H1("E-Commerce Marketing Dashboard", style={'textAlign':'center','color':'#003366'}),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Filter by Education:"),
            dcc.Dropdown(
                id='edu-filter',
                options=[{'label': edu, 'value': edu} for edu in sorted(df['Education'].unique())],
                value=None,
                placeholder="Select Education",
                clearable=True
            )
        ], style={'width':'45%', 'display':'inline-block','margin':'10px'}),

        html.Div([
            html.Label("Filter by Marital Status:"),
            dcc.Dropdown(
                id='mar-filter',
                options=[{'label': m, 'value': m} for m in sorted(df['Marital_Status'].unique())],
                value=None,
                placeholder="Select Marital Status",
                clearable=True
            )
        ], style={'width':'45%', 'display':'inline-block','margin':'10px'})
    ]),
    
    # KPI Cards
    html.Div(id='kpi-cards', style={'margin':'10px','display':'flex','justifyContent':'space-around'}),
    
    # Customer Distributions
    html.Div([
        html.H2("Customer Distributions", style={'color':'#00509E'}),
        dcc.Graph(id='edu-graph'),
        dcc.Graph(id='mar-graph'),
        dcc.Graph(id='income-graph')
    ], style={'margin':'20px'}),
    
    # A/B Testing
    html.Div([
        html.H2("A/B Testing Insights", style={'color':'#00509E'}),
        dcc.Graph(id='ab-graph')
    ], style={'margin':'20px'})
], style={'fontFamily':'Arial, sans-serif', 'backgroundColor':'#F5F5F5','padding':'10px'})

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output('kpi-cards', 'children'),
    Output('edu-graph', 'figure'),
    Output('mar-graph', 'figure'),
    Output('income-graph', 'figure'),
    Output('ab-graph', 'figure'),
    Input('edu-filter', 'value'),
    Input('mar-filter', 'value')
)
def update_dashboard(selected_edu, selected_mar):
    # Filter data
    filtered_df = df.copy()
    if selected_edu:
        filtered_df = filtered_df[filtered_df['Education'] == selected_edu]
    if selected_mar:
        filtered_df = filtered_df[filtered_df['Marital_Status'] == selected_mar]

    # ----------------------------
    # KPI Cards
    # ----------------------------
    total_customers = len(filtered_df)
    avg_income = filtered_df['Income'].mean() if total_customers > 0 else 0
    overall_conversion = filtered_df[list(campaign_map.keys())].mean().mean()*100 if total_customers > 0 else 0

    # Detailed tooltips
    edu_breakdown = filtered_df['Education'].value_counts().to_dict()
    edu_tooltip = "<br>".join([f"{k}: {v}" for k,v in edu_breakdown.items()]) if edu_breakdown else "No data"

    income_min = filtered_df['Income'].min() if total_customers > 0 else 0
    income_max = filtered_df['Income'].max() if total_customers > 0 else 0
    income_median = filtered_df['Income'].median() if total_customers > 0 else 0

    conv_per_campaign = {campaign_map[col]: f"{filtered_df[col].mean()*100:.2f}%" for col in campaign_map}
    conv_tooltip = "<br>".join([f"{k}: {v}" for k,v in conv_per_campaign.items()])

    kpi_cards = [
        html.Div([
            html.H4("Total Customers"),
            html.H2(f"{total_customers:,}")
        ], title=f"Breakdown by Education:<br>{edu_tooltip}", 
           style={'backgroundColor':'#1E90FF','color':'white','padding':'25px','borderRadius':'10px','textAlign':'center','flex':1,'margin':'5px'}),
        
        html.Div([
            html.H4("Average Income"),
            html.H2(f"${avg_income:,.0f}")
        ], title=f"Min: ${income_min:,.0f}<br>Median: ${income_median:,.0f}<br>Max: ${income_max:,.0f}",
           style={'backgroundColor':'#32CD32','color':'white','padding':'25px','borderRadius':'10px','textAlign':'center','flex':1,'margin':'5px'}),
        
        html.Div([
            html.H4("Overall Conversion Rate"),
            html.H2(f"{overall_conversion:.2f}%")
        ], title=f"Per-Campaign Conversion:<br>{conv_tooltip}",
           style={'backgroundColor':'#FF8C00','color':'white','padding':'25px','borderRadius':'10px','textAlign':'center','flex':1,'margin':'5px'})
    ]

    # ----------------------------
    # Education Distribution
    # ----------------------------
    edu_df = filtered_df['Education'].value_counts().reset_index()
    edu_df.columns = ['Education', 'Count']
    fig_edu = px.bar(edu_df, x='Education', y='Count', text='Count', 
                     title="Distribution of Education Levels", color='Education')

    # ----------------------------
    # Marital Distribution
    # ----------------------------
    mar_df = filtered_df['Marital_Status'].value_counts().reset_index()
    mar_df.columns = ['Marital_Status', 'Count']
    fig_mar = px.bar(mar_df, x='Marital_Status', y='Count', text='Count', 
                     title="Distribution of Marital Status", color='Marital_Status')
    
    # ----------------------------
    # Income Distribution
    # ----------------------------
    fig_income = px.histogram(filtered_df, x='Income', nbins=20, 
                              title="Income Distribution", color_discrete_sequence=['#FF69B4'])

    # ----------------------------
    # A/B Testing
    # ----------------------------
    campaign_data = [{'Campaign': campaign_map[col], 'Conversion Rate (%)': filtered_df[col].mean()*100} for col in campaign_map]
    ab_df = pd.DataFrame(campaign_data)
    fig_ab = px.bar(ab_df, x='Campaign', y='Conversion Rate (%)', text='Conversion Rate (%)',
                    title="Campaign Conversion Rates (A/B Testing)", color='Campaign', color_discrete_sequence=px.colors.qualitative.Bold)
    fig_ab.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_ab.update_layout(yaxis=dict(range=[0, max(ab_df['Conversion Rate (%)'])*1.2 if not ab_df.empty else 10]))
    
    return kpi_cards, fig_edu, fig_mar, fig_income, fig_ab

# ----------------------------
# Run app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
