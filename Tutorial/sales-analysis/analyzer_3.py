# analyzer.py
import pandas as pd
from helpers import calculate_total, format_currency



# 一步精簡：pipe 串接所有操作
def add_total_and_format(df):
    df = df.assign(
        total=lambda d: d.apply(lambda row: calculate_total(row['quantity'], row['price']), axis=1),
        formatted_total=lambda d: d['total'].apply(format_currency)
    )
    return df

df = pd.read_csv('data/sales.csv').pipe(add_total_and_format)

print("Sales Data:")
print(df[['product', 'formatted_total']].to_string(index=False, header=False))

print(f"\nGrand Total: {df['total'].agg(lambda x: format_currency(x.sum()))}")