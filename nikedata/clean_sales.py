import pandas as pd

df = pd.read_csv("raw_data/Nike_Sales.csv", encoding='utf-8')

#rename columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")

#remove duplicates
df = df.drop_duplicates()

#handle missing values
df = df.fillna({
    "region": "Unknown",
    "gender_category": "unknown",
    "revenue": "unknown",
    "product_line": "unknown",
    "mrp": 0,
    "units_sold": 0,
    "size":0,
    "profit":0,
    "order_date":"unknown",
    "sales_chanel":"unknown"
})

#drop where order_id or product_name missing
df = df.dropna(subset=["order_id", "product_name"])

#clean numeric columns
numeric_cols = ["units_sold", "mrp", "discount_applied", "revenue", "profit"]
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace('[/$,]', '', regex = True)
    df[col] = pd.to_numeric(df[col], errors = 'coerce')

#convert units_sold to integer
df["units_sold"] = df["units_sold"].fillna(0).astype(int)

#fix inconsistent categories
df["gender_category"] = df["gender_category"].replace({
    "mens": "men", "man' s": "men", "man":"men",
    "womens":"women", "woman":"women",
    "uni":"unisex"
})

#strip extra spaces in text columns
for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()

#save cleaned output
df.to_csv("cleaned_data/sales_cleaned.csv", index=False)

print("Cleaning completed. File saved.")