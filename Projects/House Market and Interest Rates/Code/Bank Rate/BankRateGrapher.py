import pandas as pd
import matplotlib.pyplot as plt

#Load the start of year data for bank rate
df = pd.read_csv("Project4a_Option2\\StartOfYearBankRate_AnnualChange.csv")

#Plots the data of start of year bank rate against the year
plt.figure()
plt.step(
    df['Year'],
    df['StartOfYearBankRate'],
    where='post'
)

#Labels title and grid
plt.xlabel("Year")
plt.ylabel("Start-of-Year Bank Rate (%)")
plt.title("Start-of-Year Bank Rate by Year")
plt.grid(True)
plt.show()
