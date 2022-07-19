import pandas as pd 
import numpy as np 
import seaborn as sns

# import the Johns Hopkins University COVID19 dataset
corona_dataset_csv = pd.read_csv("covid19_Confirmed_dataset.csv")

# import the world happiness dataset
happiness_report_csv = pd.read_csv("worldwide_happiness_report.csv")

# drop useless columns
corona_dataset_csv.drop(["Lat", "Long"], axis=1, inplace=True)

# aggregate rows by country
corona_dataset_aggregated = corona_dataset_csv.groupby("Country/Region").sum()

# find the max infection rate for all countries
countries = list(corona_dataset_aggregated.index)
max_infection_rates = []
for country in countries:
    curr_max = corona_dataset_aggregated.loc[country].diff().max()
    max_infection_rates.append(curr_max)
    
corona_dataset_aggregated["Maximum Infection Rate"] = max_infection_rates

# create a new dataframe with the needed column
corona_data = pd.DataFrame(corona_dataset_aggregated["Maximum Infection Rate"])

# drop useless columns
useless_cols = ["Overall rank", "Score", "Generosity", "Perceptions of corruption"]
happiness_report_csv.drop(useless_cols, axis=1, inplace=True)

# change indices of dataframe
happiness_report_csv.set_index("Country or region", inplace=True)

# join both datasets
data = corona_data.join(happiness_report_csv, how="inner")

# plot GDP vs max infection rate
x = data["GDP per capita"]
y = data["Maximum Infection Rate"]
sns.regplot(x, np.log(y))
