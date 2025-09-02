# 02_eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_campaign.csv")

# ------------------------------
# Load cleaned dataset
# ------------------------------
df = pd.read_csv(DATA_PATH, delimiter=";")  # semicolon important
df.columns = df.columns.str.strip()         # remove extra spaces
print("Columns available:", df.columns.tolist())
print(df.head())

# Set Seaborn style
sns.set(style="whitegrid")

# ------------------------------
# 1. Income Distribution
# ------------------------------
plt.figure(figsize=(8,5))
sns.histplot(df["Income"], bins=20, kde=True, color="skyblue")
plt.title("Customer Income Distribution")
plt.xlabel("Income")
plt.ylabel("Count")
plt.show()

# ------------------------------
# 2. Education Distribution
# ------------------------------
plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Education", order=df["Education"].value_counts().index, palette="pastel")
plt.title("Distribution of Education Levels")
plt.xlabel("Education Level")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

# ------------------------------
# 3. Marital Status Distribution
# ------------------------------
plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Marital_Status", order=df["Marital_Status"].value_counts().index, palette="Set2")
plt.title("Distribution of Marital Status")
plt.xlabel("Marital Status")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

# ------------------------------
# 4. Campaign Acceptance Rates
# ------------------------------
campaign_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"]
campaign_success = df[campaign_cols].mean() * 100  # percentage

plt.figure(figsize=(8,5))
sns.barplot(x=campaign_success.index, y=campaign_success.values, palette="Blues_d")
plt.title("Campaign Acceptance Rates (%)")
plt.ylabel("Acceptance Rate (%)")
plt.xlabel("Campaigns")
plt.show()
print("Campaign Acceptance Rates (%):")
print(campaign_success.round(2))

# ------------------------------
# 5. Customer Spending Behavior
# ------------------------------
purchase_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]

plt.figure(figsize=(10,6))
df[purchase_cols].sum().plot(kind="bar", color="coral")
plt.title("Total Spending per Product Category")
plt.ylabel("Total Amount Spent")
plt.xlabel("Product Category")
plt.show()

# ------------------------------
# 6. Engagement Channels
# ------------------------------
engagement_cols = ["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth"]

plt.figure(figsize=(10,6))
df[engagement_cols].sum().plot(kind="bar", color="mediumseagreen")
plt.title("Total Engagement Across Channels")
plt.ylabel("Total Interactions")
plt.xlabel("Channel")
plt.show()

# ------------------------------
# 7. Complaints vs Response
# ------------------------------
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="Complain", hue="Response", palette="Set1")
plt.title("Complaints vs Last Campaign Response")
plt.xlabel("Complain (0=No, 1=Yes)")
plt.ylabel("Count")
plt.show()

# ------------------------------
# 8. Correlation Heatmap
# ------------------------------
numeric_cols = df.select_dtypes(include="number")
plt.figure(figsize=(12,8))
sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()
