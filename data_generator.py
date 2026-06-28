"""
AI Sales Reporting System — Data Generator
Generates realistic multi-region sales data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

REGIONS = {
    "MENA": ["Saudi Arabia", "UAE", "Egypt", "Kuwait", "Qatar"],
    "Europe": ["Germany", "France", "UK", "Netherlands", "Spain"],
    "Asia": ["India", "Singapore", "Japan", "South Korea", "Indonesia"],
    "Americas": ["USA", "Canada", "Brazil", "Mexico", "Argentina"],
}

CATEGORIES = {
    "Software": {
        "products": ["CRM Pro", "Analytics Suite", "CloudSync", "DataVault", "AutoFlow"],
        "price_range": (200, 5000),
        "margin": 0.72,
    },
    "Hardware": {
        "products": ["Server X200", "Edge Device Pro", "Smart Scanner", "IoT Hub", "NAS Storage"],
        "price_range": (800, 15000),
        "margin": 0.38,
    },
    "Services": {
        "products": ["Implementation", "Training Package", "Support Premium", "Consulting", "Data Migration"],
        "price_range": (500, 20000),
        "margin": 0.55,
    },
    "Subscriptions": {
        "products": ["Basic Plan", "Business Plan", "Enterprise Plan", "Starter Pack", "Elite Tier"],
        "price_range": (50, 2000),
        "margin": 0.80,
    },
}

SALES_REPS = [
    "Ahmed Al-Rashidi", "Sarah Johnson", "Mohammed Al-Otaibi", "Chen Wei",
    "Fatima Al-Zahrani", "Lucas Müller", "Priya Sharma", "Carlos Mendez",
    "Noor Al-Hamdan", "Emma Thompson"
]

CHANNELS = ["Direct Sales", "Online Platform", "Partner Network", "Inbound Lead", "Cold Outreach"]

def generate_sales_data(n_records=2000, start_date="2024-01-01", end_date="2024-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days_range = (end - start).days

    records = []
    order_id = 10001

    for _ in range(n_records):
        category = random.choice(list(CATEGORIES.keys()))
        cat_info = CATEGORIES[category]
        product = random.choice(cat_info["products"])

        region = random.choice(list(REGIONS.keys()))
        country = random.choice(REGIONS[region])

        # Seasonal trend: Q4 boost, Q1 slow
        date = start + timedelta(days=random.randint(0, days_range))
        month = date.month
        seasonal_factor = 1.0
        if month in [10, 11, 12]: seasonal_factor = 1.35
        elif month in [1, 2]: seasonal_factor = 0.75
        elif month in [6, 7, 8]: seasonal_factor = 1.10

        base_price = random.uniform(*cat_info["price_range"])
        unit_price = round(base_price * seasonal_factor, 2)
        quantity = random.choices([1, 2, 3, 5, 10], weights=[45, 25, 15, 10, 5])[0]
        revenue = round(unit_price * quantity, 2)
        cost = round(revenue * (1 - cat_info["margin"]) * random.uniform(0.9, 1.1), 2)
        profit = round(revenue - cost, 2)

        # Shipping cost based on category
        shipping = 0 if category in ["Software", "Subscriptions"] else round(random.uniform(20, 350), 2)

        # Discount occasionally
        discount_pct = random.choices([0, 5, 10, 15, 20], weights=[55, 20, 15, 7, 3])[0]
        discount_amount = round(revenue * discount_pct / 100, 2)
        final_revenue = round(revenue - discount_amount, 2)
        final_profit = round(profit - discount_amount * cat_info["margin"], 2)

        # Status
        status = random.choices(
            ["Completed", "Completed", "Completed", "Returned", "Pending", "Cancelled"],
            weights=[70, 70, 70, 8, 15, 7]
        )[0]

        records.append({
            "Order_ID": f"ORD-{order_id}",
            "Date": date.strftime("%Y-%m-%d"),
            "Month": date.strftime("%B"),
            "Quarter": f"Q{(month-1)//3 + 1}",
            "Year": date.year,
            "Region": region,
            "Country": country,
            "Category": category,
            "Product": product,
            "Sales_Rep": random.choice(SALES_REPS),
            "Channel": random.choice(CHANNELS),
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": revenue,
            "Discount_Pct": discount_pct,
            "Discount_Amount": discount_amount,
            "Final_Revenue": final_revenue,
            "Cost": cost,
            "Shipping_Cost": shipping,
            "Profit": final_profit,
            "Profit_Margin_Pct": round(final_profit / final_revenue * 100, 1) if final_revenue > 0 else 0,
            "Status": status,
        })
        order_id += 1

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def save_data(df, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "sales_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved {len(df)} records to {csv_path}")
    return csv_path


if __name__ == "__main__":
    df = generate_sales_data(2000)
    save_data(df, "data")
    print(df.head())
    print(f"\nDate range: {df['Date'].min().date()} → {df['Date'].max().date()}")
    print(f"Total Revenue: ${df['Final_Revenue'].sum():,.0f}")
