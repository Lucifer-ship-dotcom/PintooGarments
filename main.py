import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "all stk.xlsx"

# -----------------------------
# LOAD & CLEAN
# -----------------------------
df = pd.read_excel(file_path, header=1)
df = df.dropna(how='all')
df = df.dropna(axis=1, how='all')
df.columns = df.columns.astype(str).str.strip()

def root(): return {"message":"Welcome to MedAI Healthcare Platform","version":settings.APP_VERSION,"status":"running"}
branch_keywords = ["C G ROAD", "S G ROAD", "MANINAGAR", "S. BOPAL", "GOTA"]

branch_map = {}

for col in df.columns:
    for branch in branch_keywords:
        if branch in col.upper():
            branch_map.setdefault(branch, []).append(col)

def get_series(col):
    data = df[col]
    if isinstance(data, pd.DataFrame):
        data = data.iloc[:, 0]
    return pd.to_numeric(data, errors='coerce').fillna(0)

# -----------------------------
# CALCULATIONS
# -----------------------------
branch_sales = {}
branch_qty = {}

for branch, cols in branch_map.items():
    total_sale = 0
    total_qty = 0
    for col in cols:
        series = get_series(col)
        total_sale += series.sum()
        total_qty += series.count()
    branch_sales[branch] = total_sale
    branch_qty[branch] = total_qty

branch_sales = pd.Series(branch_sales).sort_values(ascending=False)
branch_qty = pd.Series(branch_qty)

# Product totals
item_col = df.columns[0]

df["TOTAL"] = 0
for branch, cols in branch_map.items():
    for col in cols:
        df["TOTAL"] += get_series(col)

top15 = (
    df.groupby(item_col)["TOTAL"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

# -----------------------------
# DASHBOARD DESIGN
# -----------------------------
plt.figure(figsize=(20,10))

# ========== 1️⃣ Branch-wise Sales + Quantity ==========
plt.subplot(2,2,1)

x = np.arange(len(branch_sales))
width = 0.3   # reduced bar width

plt.bar(x - width/2, branch_sales.values, width=width, label="Sales Value")
plt.bar(x + width/2, branch_qty.values, width=width, label="Quantity")

plt.xticks(x, branch_sales.index, rotation=45)
plt.title("📊 Branch Performance (Sales vs Quantity)")
plt.xlabel("Branches")
plt.ylabel("Value / Quantity")
plt.legend()

# ========== 2️⃣ Top 15 Products ==========
plt.subplot(2,1,2)

colors = plt.cm.tab20(np.linspace(0,1,len(top15)))

plt.bar(top15.index, top15.values, color=colors, width=0.5)

plt.title("🏆 Top 15 Products by Sales")
plt.xlabel("Product Name")
plt.ylabel("Total Sales Value")
plt.xticks(rotation=75)

# ========== 3️⃣ Branch Quantity Distribution ==========
plt.subplot(2,2,2)

plt.bar(branch_qty.index, branch_qty.values, width=0.4)
plt.title("📦 Branch-wise Quantity Distribution")
plt.xlabel("Branches")
plt.ylabel("Total Quantity")
plt.xticks(rotation=45)

plt.suptitle("📊 SALES & INVENTORY DASHBOARD", fontsize=18, fontweight='bold')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
