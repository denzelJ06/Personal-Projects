import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

INPUT_FILE = 'CPIH Clean (1).xlsx'
OUTPUT_IMAGE = 'cpih_forecast_2028.png'
OUTPUT_CSV = 'CPIH_Forecast_2028.csv'
TARGET_YEAR = 2028

def find_header_and_load(filepath):
    print(f"--- Processing File: {filepath} ---")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find '{filepath}'. Make sure it is in the {os.getcwd()} folder.")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.xlsx':
        print("Detected Excel file. Reading...")
        df_raw = pd.read_excel(filepath, header=None, nrows=30)
    else:
        print("Detected CSV file. Reading...")
        try:
            df_raw = pd.read_csv(filepath, header=None, nrows=30, encoding='cp1252')
        except:
            df_raw = pd.read_csv(filepath, header=None, nrows=30, encoding='latin1')

    header_idx = -1
    for i, row in df_raw.iterrows():
        row_str = row.astype(str).str.cat(sep=' ')
        if 'CPIH ALL ITEMS' in row_str or 'CPIH All items' in row_str:
            header_idx = i
            print(f"Found header at row {i}")
            break

    if header_idx == -1:
        print("Warning: Could not auto-detect header row. Defaulting to row 3.")
        header_idx = 3

    if ext == '.xlsx':
        df = pd.read_excel(filepath, header=header_idx)
    else:
        try:
            df = pd.read_csv(filepath, header=header_idx, encoding='cp1252')
        except:
            df = pd.read_csv(filepath, header=header_idx, encoding='latin1')

    df.columns = df.columns.str.strip()

    target_col = None
    for col in df.columns:
        if 'CPIH' in col and 'items' in col.lower():
            target_col = col
            break

    if not target_col:
        raise KeyError("Could not find a column named 'CPIH ALL ITEMS'. Check your file.")

    print(f"Target column identified as: '{target_col}'")

    df_clean = df[['name', target_col]].copy()
    df_clean.rename(columns={target_col: 'Value'}, inplace=True)

    df_clean.dropna(subset=['Value'], inplace=True)
    df_clean['date'] = pd.to_datetime(df_clean['name'], errors='coerce')
    df_clean.dropna(subset=['date'], inplace=True)

    df_clean.sort_values('date', inplace=True)
    df_clean.set_index('date', inplace=True)

    print(f"Data Loaded Successfully: {len(df_clean)} rows from {df_clean.index.min().date()} to {df_clean.index.max().date()}")
    return df_clean

def generate_forecast(df, target_year):
    print("\n--- Generating Forecast ---")

    x = df.index.map(pd.Timestamp.toordinal)
    y = df['Value']

    slope, intercept = np.polyfit(x, y, 1)

    df['Trend'] = slope * x + intercept
    df['Detrended'] = df['Value'] - df['Trend']
    seasonal_profile = df.groupby(df.index.month)['Detrended'].mean()

    last_date = df.index.max()
    last_actual = df['Value'].iloc[-1]

    model_val_at_end = (slope * last_date.toordinal() + intercept) + seasonal_profile[last_date.month]

    offset = last_actual - model_val_at_end

    start_forecast = last_date + pd.DateOffset(months=1)
    end_forecast = pd.Timestamp(f'{target_year}-12-31')

    months_count = (end_forecast.year - start_forecast.year) * 12 + (end_forecast.month - start_forecast.month) + 1
    future_dates = pd.date_range(start=start_forecast, periods=months_count, freq='MS')

    future_x = future_dates.map(pd.Timestamp.toordinal)
    future_trend = slope * future_x + intercept
    future_seasonal = [seasonal_profile[d.month] for d in future_dates]

    future_values = future_trend + future_seasonal + offset

    forecast_df = pd.DataFrame({'Value': future_values}, index=future_dates)
    forecast_df.index.name = 'date'

    return forecast_df

def plot_and_save(hist_df, fore_df):
    print("\n--- Plotting Results ---")

    plt.figure(figsize=(12, 6))

    plt.plot(hist_df.index, hist_df['Value'],
             label='Historical Data', color='#1f77b4', linewidth=2)

    last_hist_date = hist_df.index[-1]
    last_hist_val = hist_df['Value'].iloc[-1]

    conn_dates = [last_hist_date] + fore_df.index.tolist()
    conn_vals = [last_hist_val] + fore_df['Value'].tolist()

    plt.plot(conn_dates, conn_vals,
             label='Forecast (Continuous)', color='#2ca02c', linestyle='--', linewidth=2)

    plt.title(f'CPIH Forecast to {TARGET_YEAR}', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('CPIH Index', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.tight_layout()

    plt.savefig(OUTPUT_IMAGE)
    print(f"Chart saved to: {os.path.abspath(OUTPUT_IMAGE)}")

    print("Opening plot window...")
    plt.show()

def main():
    try:
        df_hist = find_header_and_load(INPUT_FILE)
        
        df_fore = generate_forecast(df_hist, TARGET_YEAR)

        df_hist_out = df_hist[['Value']].copy()
        df_hist_out['Type'] = 'Historical'

        df_fore_out = df_fore[['Value']].copy()
        df_fore_out['Type'] = 'Forecast'

        df_final = pd.concat([df_hist_out, df_fore_out])
        df_final.to_csv(OUTPUT_CSV)
        print(f"Data saved to: {os.path.abspath(OUTPUT_CSV)}")

        plot_and_save(df_hist, df_fore)

    except Exception as e:
        print("\n!!! ERROR OCCURRED !!!")
        print(e)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()