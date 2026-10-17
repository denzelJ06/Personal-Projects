import pandas as pd

#Load the data
df = pd.read_csv("Project4a_Option2\Bank Rate History Raw.csv")
df['Date Changed'] = pd.to_datetime(df['Date Changed'])

#Create a table of year start Date Changeds
years = range(df['Date Changed'].dt.year.min(), df['Date Changed'].dt.year.max() + 1)
year_starts = pd.DataFrame({
    'Year': years,
    'YearStart': pd.to_datetime([f"{y}-01-01" for y in years])
})

#Merge using "last known value before or on Jan 1"
year_start_rates = pd.merge_asof(
    year_starts.sort_values('YearStart'),
    df[['Date Changed', 'Rate']].sort_values('Date Changed'),
    left_on='YearStart',
    right_on='Date Changed',
    direction='backward'
)

#Final output
result = year_start_rates[['Year', 'Rate']]
result = result.rename(columns={'Rate': 'StartOfYearBankRate'})
result['AnnualRateChange'] = result['StartOfYearBankRate'].diff()
print(result)
output_path = "Project4a_Option2\\StartOfYearBankRate_AnnualChange.csv"
#result.to_csv(output_path, index=False)