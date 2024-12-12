#!/usr/bin/env python
# coding: utf-8

# # Project Title: Income-Health-Analysis

# Description:
# 
# In this project, I applied data wrangling skills to gather and process real-world data focusing on income levels and health outcomes. The project involved retrieving and extracting data from multiple sources, assessing data quality and structure both programmatically and visually, and implementing a comprehensive cleaning strategy. The cleaned data was then stored in a selected database, combined, and analyzed to answer a key research question.
# 
# Throughout the project, I:
# 
# Explained the methods used for data gathering, assessment, cleaning, storage, and analysis.
# Included detailed code comments for readability and understanding.
# Required packages were installed to facilitate the data wrangling process.

# In[1]:


get_ipython().system('python -m pip install kaggle==1.6.12')


# In[2]:


get_ipython().system('pip install --target=/workspace ucimlrepo numpy==1.24.3')


# **Note:** Restart the kernel to use updated package(s).

# ## 1. Gather data
# 
# In this section, you will extract data using two different data gathering methods and combine the data. Use at least two different types of data-gathering methods.

# ### **1.1.** Problem Statement
# 
# 
# For this project, I aim to explore the relationship between GDP and mortality rates across different countries over time. The goal is to analyze how economic factors (such as GDP) impact health outcomes (represented by mortality rates) and explore patterns or trends in this relationship. To answer this, I will gather data on GDP and mortality rates for various countries over a span of several years, using two different methods for data collection.
# 
# 

# Here are the datasets I worked with and their respective sources:
# 
# 1. World Bank - GDP Data
# Description: This dataset provides information on Gross Domestic Product (GDP) in USD for various countries across different years.
# Variables:
# Country: The country name or code.
# Year: The year of the data.
# GDP: Gross Domestic Product (in USD) for the respective country and year.
# Gathering Method: Programmatically downloaded using the World Bank API.
# Link:  https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
# 2. World Bank - Mortality Rate Data
# World Health Organization (WHO) - Mortality Rate Data
# Description: This dataset contains information on mortality rates (deaths per 1,000 people) for various countries across different years.
# Variables:
# 
# Country (SpatialDim): The country or region name or code.
# Year (TimeDim): The year of the data.
# Mortality Rate (Value): The mortality rate (deaths per 1,000 people) for the respective country and year.
# Gathering Method: Programmatically downloaded using the WHO Global Health Observatory (GHO) API.
# Link: https://ghoapi.azureedge.net/api/MORT_100

# ### **1.2.** Gather at least two datasets using two different data gathering methods
# 
# List of data gathering methods:
# 
# - Download data manually
# 
# - Gather data by accessing APIs
# 
# 
# 

# #### **Dataset 1**
# 
# ##### GDP Data from World Bank
# Data Gathering Method: Programmatically downloading files
# 
# Dataset Description: This dataset provides GDP data from the World Bank, which is used to understand economic growth and trends in various countries. The variables of interest in the dataset are:
# 
# Country: The country for which GDP data is recorded.
# GDP (current US$): The GDP value in current US dollars for each country over time.
# Reason for Choosing: This dataset is significant because it allows the analysis of the economic performance of countries over the years, which is a key economic indicator. It helps answer questions related to economic growth, comparison across countries, and how GDP evolves over time.
# 
# 
# type: CSV File
# 
# Method: The data was gathered using the "Downloading files" method from the World Bank's World Development Indicators.
# 
# *Dataset variables*:
# 
# *   *Variable 1: Country Name - The name of the country.
# *   *Variable 2: Country Code - The code representing the country.
# *   *Variable 3: Indicator Name - The name of the economic indicator.
# *   *Variable 4: Indicator Code - The code representing the economic indicator.
# *   *Variable 5: Year Columns (1960 - 2023) - GDP values for each year from 1960 to 2023.
# 

# In[77]:


import pandas as pd

# File path for the CSV
file_path = 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2.csv'

# Load the data with the correct encoding and handle bad lines
gdp_data = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

# Display the first 5 rows of the raw data to understand its structure
print(gdp_data.head())


# #### Dataset 2
# 
# #####
# 
# Dataset 2: Mortality Rate Data from the World Health Organization
# Data Gathering Method: Programmatically downloading files (via API)
# 
# Dataset Description: This dataset provides mortality rate data from the World Health Organization (WHO). It helps in analyzing public health trends by tracking the number of deaths per 1,000 people per year across different countries. This data is essential for understanding health challenges worldwide and evaluating the effectiveness of healthcare systems.
# 
# Dataset Variables:
# 
# SpatialDim (Country or Region Code): This variable represents the country or region for which mortality data is recorded.
# TimeDim (Year): The year in which the mortality data was recorded.
# Value (Mortality Rate): The number of deaths per 1,000 people per year.
# Reason for Choosing the Dataset: This dataset was selected because it provides vital information about public health across various countries. Mortality rates are a key indicator of healthcare system effectiveness, life expectancy, and health-related challenges in different countries. This data allows for a comparison of health outcomes and the effectiveness of health systems globally.
# 
# Data Gathering Method:
# The data was collected using the API method from the World Health Organization's Global Health Observatory (GHO), which provides global health indicators including mortality rates.
# 
# Type: *JSON Data* 
# 
# Method: *he data was gathered using the "API" method from the World Health Organization's Global Health Observatory (GHO).
# 
# 
# 
# Dataset variables:
# 
# *   *Variable 1: SpatialDim - The country or region code
# *   *Variable 2: TimeDim - The year of the data
# *   *Variable 3: Value - The mortality rate or the value of the indicator

# In[78]:


import requests
import pandas as pd

# URL for the GHO API to fetch mortality data
url = "https://ghoapi.azureedge.net/api/MORT_100"

# Sending the request to fetch the data
response = requests.get(url)

# Checking the response status
if response.status_code == 200:
    try:
        data = response.json()
        
        # Extracting data and converting it to a DataFrame
        countries_data = data['value']
        df = pd.json_normalize(countries_data)
        
        # Displaying the data
        print(df[['SpatialDim', 'TimeDim', 'Value']])
    except ValueError:
        print("Error parsing JSON response")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


# ## 2. Assess data
# 
# 

# ### Quality Issue 1:

# In[79]:


#FILL IN - Inspecting the dataframe visually
print(gdp_data.head())
print(gdp_data.info())


# In[80]:


#FILL IN - Inspecting the dataframe programmatically
missing_values = gdp_data.isnull().sum()
print(missing_values[missing_values > 0])


# Issue and justification: *The visual inspection of the dataframe shows that there are a lot of NaN values in the dataset. Programmatically, the info() method and the isnull().sum() method confirm the presence of missing values across many columns. Missing data can lead to inaccurate analyses and should be handled appropriately by either imputing or removing the missing values.*

# ### Quality Issue 2:

# In[81]:


#FILL IN - Inspecting the dataframe visually
print(df.head())
print(df.info())


# In[82]:


#FILL IN - Inspecting the dataframe programmatically
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])


# Issue and justification: *
# The visual inspection of the dataframe shows that there are several columns with missing values, such as ParentLocationCode, ParentLocation, DataSourceDimType, DataSourceDim, Value, NumericValue, Low, High, and Comments. Programmatically, the info() method and the isnull().sum() method confirm the presence of missing values across these columns. Missing data can lead to inaccurate analyses and should be handled appropriately by either imputing or removing the missing values. Specifically, DataSourceDimType, DataSourceDim, Low, High, and Comments columns are entirely missing values, indicating that they might be unnecessary or require additional data sources for completion.*

# ### Tidiness Issue 1:

# In[83]:


#FILL IN - Inspecting the dataframe visually
print(gdp_data.head())


# In[84]:


#FILL IN - Inspecting the dataframe programmatically
print(gdp_data.columns)


# Issue and justification: 
# Issue: The first three rows contain metadata rather than actual data. This results in multiple rows that are not part of the actual dataset, making it untidy and requiring manual cleaning before analysis. Justification: Metadata rows should be excluded, and column names should be set appropriately to ensure the dataframe is tidy and ready for analysis.

# ### Tidiness Issue 2: 

# In[85]:


#FILL IN - Inspecting the dataframe visually
print(df.head())


# In[86]:


#FILL IN - Inspecting the dataframe programmatically
print(df.columns)


# Issue and justification: *Issue: The first three rows contain metadata rather than actual data. This results in multiple rows that are not part of the actual dataset, making it untidy and requiring manual cleaning before analysis. Justification: Metadata rows should be excluded, and column names should be set appropriately to ensure the dataframe is tidy and ready for analysis.*

# ## 3. Clean data
# Clean the data to solve the 4 issues corresponding to data quality and tidiness found in the assessing step. **Make sure you include justifications for your cleaning decisions.**
# 
# After the cleaning for each issue, please use **either** the visually or programatical method to validate the cleaning was succesful.
# 
# At this stage, you are also expected to remove variables that are unnecessary for your analysis and combine your datasets. Depending on your datasets, you may choose to perform variable combination and elimination before or after the cleaning stage. Your dataset must have **at least** 4 variables after combining the data.

# In[87]:


# FILL IN - Make copies of the datasets to ensure the raw dataframes 
# are not impacted
gdp_data_clean = gdp_data.copy()
df_clean = df.copy()


# ### **Quality Issue 1: FILL IN**

# In[88]:


# FILL IN - Apply the cleaning strategy
# Drop the first three rows
gdp_data_clean = gdp_data_clean.drop([0, 1, 2])

# Set the fourth row as the header
gdp_data_clean.columns = gdp_data_clean.iloc[0]
gdp_data_clean = gdp_data_clean.drop(3)

# Drop any remaining completely empty rows
gdp_data_clean = gdp_data_clean.dropna(how='all')

# Reset the index
gdp_data_clean = gdp_data_clean.reset_index(drop=True)


# In[89]:


# FILL IN - Validate the cleaning was successful
print(gdp_data_clean.head())


# Justification: *The metadata rows were removed, and the dataframe's column headers were set correctly. The cleaned dataframe now only contains relevant data.*

# ### **Quality Issue 2: FILL IN**

# In[90]:


#FILL IN - Apply the cleaning strategy
# Convert the Value column to numeric, setting errors='coerce' to force non-numeric values to NaN
df_clean['Value'] = pd.to_numeric(df_clean['Value'], errors='coerce')

# Drop rows with NaN values in the Value column
df_clean = df_clean.dropna(subset=['Value'])


# In[91]:


#FILL IN - Validate the cleaning was successful
print(df_clean.head())


# Justification: *The Value column now only contains numeric data, and any non-numeric entries have been removed, ensuring the column is ready for analysis.*

# ### **Tidiness Issue 1: FILL IN**

# In[92]:


#FILL IN - Apply the cleaning strategy
# Remove columns that are completely empty (all NaN values)
gdp_data_clean = gdp_data_clean.dropna(axis=1, how='all')

# Remove irrelevant columns, keeping only 'Country Name', 'Country Code', and GDP columns
relevant_columns = ['Country Name', 'Country Code'] + [col for col in gdp_data_clean.columns if col not in ['Country Name', 'Country Code']]
gdp_data_clean = gdp_data_clean[relevant_columns]


# In[93]:


#FILL IN - Validate the cleaning was successful
print(gdp_data_clean.head())
print(gdp_data_clean.columns)


# Justification: *This ensures that only the relevant data is kept, making the dataframe tidy and easier to work with for analysis.*

# ### **Tidiness Issue 2: FILL IN**

# In[94]:


#FILL IN - Apply the cleaning strategy
# Remove unnecessary columns, keeping only 'SpatialDim', 'TimeDim', 'IndicatorCode', and 'Value'
relevant_columns = ['SpatialDim', 'TimeDim', 'IndicatorCode', 'Value']
df_clean = df_clean[relevant_columns]


# In[95]:


#FILL IN - Validate the cleaning was successful
print(df_clean.head())
print(df_clean.columns)


# Justification: *By keeping only the necessary columns, we make the dataframe tidy and focused on the analysis.*

# ### **Remove unnecessary variables and combine datasets**
# 
# Depending on the datasets, you can also peform the combination before the cleaning steps.

# In[96]:


# Verify the columns in the GDP dataset
print(gdp_data_clean.columns)

# Drop the '1960.0' column if it exists (or use the correct column name if different)
gdp_data_clean = gdp_data_clean.drop(columns=['1960.0'], errors='ignore')

# Merge the datasets
combined_data = pd.merge(df_clean, gdp_data_clean, left_on='SpatialDim', right_on='Country Code', how='inner')

# Rename columns for clarity
combined_data = combined_data.rename(columns={'SpatialDim': 'Country', 'Value': 'Mortality Rate'})



# In[69]:


# Display the merged data
print(combined_data.head())


# In[70]:


# Remove the dots from the column names
combined_data.columns = combined_data.columns.astype(str).str.replace('.0', '', regex=False)

# Filter the columns related to years between 2014 and 2023
year_columns = [str(year) for year in range(2014, 2024) if str(year) in combined_data.columns]

# Reshape the data using pd.melt
combined_data_melted = pd.melt(combined_data, 
                               id_vars=['Country', 'Country Code', 'Indicator Code', 'Mortality Rate', 'Country Name'], 
                               value_vars=year_columns, 
                               var_name='Year', 
                               value_name='GDP')

# Convert the "Year" column to DateTime format
combined_data_melted['Date'] = pd.to_datetime(combined_data_melted['Year'])

# Drop the old "Year" column
combined_data_melted = combined_data_melted.drop(columns=['Year'])

# Display the reshaped data
print(combined_data_melted.head())


# In[71]:


# Drop the 'Country' column
combined_data_melted = combined_data_melted.drop(columns=['Country'])

# Display the updated data
print(combined_data_melted.head())


# In[72]:


# Get unique values in the 'Indicator Code' column
unique_indicator_codes = combined_data_melted['Indicator Code'].unique()

# Display the unique values
print(unique_indicator_codes)


# In[73]:


# Drop the 'Country' column from combined_data_melted
combined_data_melted = combined_data_melted.drop(columns=['Indicator Code'], errors='ignore')

# Display the updated data
print(combined_data_melted.head())


# ## 4. Update your data store
# Update your local database/data store with the cleaned data, following best practices for storing your cleaned data:
# 
# - Must maintain different instances / versions of data (raw and cleaned data)
# - Must name the dataset files informatively
# - Ensure both the raw and cleaned data is saved to your database/data store

# In[74]:


# Assuming combined_data is the raw data and combined_data_melted is the cleaned data

# Save raw data (if you still have the original raw data)
raw_data_file_path = 'raw_combined_data.csv'
combined_data.to_csv(raw_data_file_path, index=False)

# Save cleaned data
cleaned_data_file_path = 'cleaned_combined_data.csv'
combined_data_melted.to_csv(cleaned_data_file_path, index=False)

# Display confirmation messages
print(f"Raw data saved to: {raw_data_file_path}")
print(f"Cleaned data saved to: {cleaned_data_file_path}")


# ## 5. Answer the research question
# 
# ### **5.1:** Define and answer the research question 
# Going back to the problem statement in step 1, use the cleaned data to answer the question you raised. Produce **at least** two visualizations using the cleaned data and explain how they help you answer the question.

# *Research question:* 1 "What is the relationship between GDP and mortality rate across different countries from 2014 to 2023?"
# 
# 
# 2 "How does the GDP growth correlate with changes in mortality rates over time in countries with varying income levels?"

# Explanation: A scatter plot can show the relationship between GDP and Mortality Rate for each country across the years. You can use the cleaned data to plot "GDP" (as the x-axis) against "Mortality Rate" (as the y-axis) to observe if there's any correlation.

# In[75]:


#Visual 1 - FILL IN
import matplotlib.pyplot as plt

# Plot GDP vs Mortality Rate
plt.figure(figsize=(10, 6))
plt.scatter(combined_data_melted['GDP'], combined_data_melted['Mortality Rate'], alpha=0.5)
plt.title('GDP vs Mortality Rate (2014-2023)')
plt.xlabel('GDP (Current US$)')
plt.ylabel('Mortality Rate')
plt.show()


# *Answer to research question:* The relationship between GDP and mortality rate can show trends where countries with higher GDP may have lower mortality rates. This is due to better healthcare systems, higher life expectancy, and more access to resources. However, the relationship could vary depending on the country’s development stage, healthcare infrastructure, and other socio-economic factors.

# #### Explanation 
# : A line plot can show how the GDP of different countries evolved over time. This can help you understand if the trends in GDP are consistent across countries and how they relate to mortality rates over the years

# In[76]:


#Visual 2 - FILL IN
import seaborn as sns

# Plot GDP over the years for different countries
plt.figure(figsize=(12, 6))
sns.lineplot(data=combined_data_melted, x='Date', y='GDP', hue='Country Name', markers=True)
plt.title('GDP Over Time for Different Countries (2014-2023)')
plt.xlabel('Year')
plt.ylabel('GDP (Current US$)')
plt.legend(title='Country Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# Mortality rates likely vary across countries due to differences in healthcare systems, economic development, public health policies, and social factors. Countries with more advanced healthcare systems, higher GDP, and better living standards typically experience lower mortality rates. On the other hand, countries with fewer resources may have higher mortality rates. The trends can also be influenced by specific global events like pandemics, economic crises, or health reforms in certain countries.
# 
# By analyzing the mortality rates over time, we can identify which countries have improved or worsened, and correlate these changes with relevant factors such as healthcare infrastructure, policies, and economic conditions.

# ### **5.2:** Reflection
# In 2-4 sentences, if you had more time to complete the project, what actions would you take? For example, which data quality and structural issues would you look into further, and what research questions would you further explore?

# *Answer:* If I had more time to complete the project, I would focus on addressing any potential data quality issues, such as missing values or outliers in the "GDP" and "Mortality Rate" columns. I would also consider investigating the impact of other factors (e.g., healthcare expenditure, population density, or education levels) on mortality rates. Additionally, I would explore further research questions, such as how the relationship between GDP and mortality rate varies across regions or income groups.
# 

# In[ ]:




