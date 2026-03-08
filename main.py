import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

# --- Կարգավորումներ (Settings) ---
DB_URL = 'postgresql://postgres:123@localhost:5432/economy_data'
CSV_PATH = os.path.expanduser("~/Desktop/Data_Projects/01_Coffee_Chain_Analysis/data/Coffee_Chain_Sales.csv")
OUTPUT_DIR = os.path.expanduser("~/Desktop/Data_Projects/01_Coffee_Chain_Analysis/outputs")

# Ստեղծել outputs թղթապանակը, եթե այն չկա
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data_to_db():
    """Կարդում է CSV-ն և ուղարկում PostgreSQL"""
    print("⏳ Տվյալների վերբեռնումը սկսված է...")
    df = pd.read_csv(CSV_PATH)
    # Սյունակների մաքրում
    df.columns = [c.replace(' ', '_').lower() for c in df.columns]
    
    engine = create_engine(DB_URL)
    df.to_sql('coffee_sales', engine, if_exists='replace', index=False)
    print("✅ Տվյալները հաջողությամբ պահպանվեցին 'coffee_sales' աղյուսակում:")

def create_visualizations():
    """SQL-ից վերցնում է տվյալները և սարքում գրաֆիկ"""
    print("📊 Գրաֆիկների պատրաստում...")
    engine = create_engine(DB_URL)
    
    # SQL հարցում
    query = "SELECT product, sum(profit) as total_profit FROM coffee_sales GROUP BY product"
    df = pd.read_sql(query, engine)
    
    # Գրաֆիկի ստեղծում
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='product', y='total_profit', palette='viridis')
    plt.title('Շահույթը ըստ ապրանքների')
    plt.xticks(rotation=45)
    
    # ԱՎՏՈՄԱՏ ՊԱՀՊԱՆՈՒՄ
    save_path = os.path.join(OUTPUT_DIR, "profit_chart.png")
    plt.savefig(save_path)
    print(f"💾 Գրաֆիկը պահպանվեց այստեղ՝ {save_path}")
    plt.close() # Փակում ենք գրաֆիկը, որ հիշողություն չզբաղեցնի

if __name__ == "__main__":
    # Այս հատվածը աշխատեցնում է ամբողջ շղթան
    load_data_to_db()
    create_visualizations()
    print("\n🚀 Աշխատանքն ավարտված է:")
