import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set Streamlit page configuration
st.set_page_config(
    page_title="Marketing Dashboard",
    page_icon=":bar_chart:",
    layout="centered",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .row_heading.level0 {display:none}
            .blank {display:none}
            .dataframe {text-align: left !important}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load the data from the provided file
file_path = 'Customerattributiondata.csv'
data = pd.read_csv(file_path, delimiter='\t')

# Display the first few rows of the dataset to understand its structure
st.subheader('DataFrame Overview')
st.write(data.head())

# Basic Data Overview: Checking for missing values and data types
st.subheader('Summary of a DataFrame')
buffer = io.StringIO()
data.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Filter and prepare the revenue data
df = data[data['REVENUE'].notnull() & (data['REVENUE'] != '')]
df['REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce')
revenue_by_channel = df.groupby('MARKETINGCHANNEL')['REVENUE'].sum().reset_index()

# Set custom color palette for Seaborn plots
custom_palette = "coolwarm"  # Using a named palette
sns.set_palette(custom_palette)
col1, col2 = st.columns(2)
with col1:
    st.subheader('Revenue Attribution by Marketing Channel')
    plt.figure(figsize=(10, 6))
    plt.pie(revenue_by_channel['REVENUE'], labels=revenue_by_channel['MARKETINGCHANNEL'], autopct='%1.1f%%', startangle=90)
    plt.title('Revenue Attribution by Marketing Channel')
    st.pyplot()

# Plotting Distribution of Customers per Marketing Channel as a Pie Chart
with col2:
    st.subheader('Distribution of Customers per Marketing Channel')
    customer_dist_by_channel = data.groupby('MARKETINGCHANNEL')['CUSTOMERID'].nunique().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(10, 6))
    plt.pie(customer_dist_by_channel['CUSTOMERID'], labels=customer_dist_by_channel['MARKETINGCHANNEL'], autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Unique Customers per Marketing Channel')
    st.pyplot()

# Time Series Analysis of Touchpoints
st.subheader('Time Series Analysis of Touchpoints (Daily)')
plt.figure(figsize=(12, 6))
data['TIMESTAMP_TOUCHPOINT'] = pd.to_datetime(data['TIMESTAMP_TOUCHPOINT'], errors='coerce')
data.set_index('TIMESTAMP_TOUCHPOINT').resample('D').size().plot()
plt.title('Time Series Analysis of Touchpoints (Daily)')
plt.xlabel('Date')
plt.ylabel('Number of Touchpoints')
st.pyplot()

# Further Data Exploration Using All Columns
st.subheader('Distribution of Touchpoints by Year/Month/Hour of Day')
data['TIMESTAMP_TOUCHPOINT'] = pd.to_datetime(data['TIMESTAMP_TOUCHPOINT'], errors='coerce')

# Extracting date components from 'TIMESTAMP_TOUCHPOINT'
data['YEAR'] = data['TIMESTAMP_TOUCHPOINT'].dt.year
data['MONTH'] = data['TIMESTAMP_TOUCHPOINT'].dt.month
data['DAY'] = data['TIMESTAMP_TOUCHPOINT'].dt.day
data['HOUR'] = data['TIMESTAMP_TOUCHPOINT'].dt.hour
data['WEEKDAY'] = data['TIMESTAMP_TOUCHPOINT'].dt.day_name()

time_component = st.selectbox("Choose time component:", ["Year", "Month", "Hour"])

# Analyzing distribution of touchpoints over different time components
if time_component == "Year":
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.countplot(x='YEAR', data=data, ax=ax)
    ax.set_title('Distribution of Touchpoints by Year')
    st.pyplot(fig)
elif time_component == "Month":
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.countplot(x='MONTH', data=data, ax=ax)
    ax.set_title('Distribution of Touchpoints by Month')
    st.pyplot(fig)
elif time_component == "Hour":
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.countplot(x='HOUR', data=data, ax=ax)
    ax.set_title('Distribution of Touchpoints by Hour of Day')
    st.pyplot(fig)

# Analyzing the number of sessions per customer
sessions_per_customer = data.groupby('CUSTOMERID')['SESSIONID'].nunique().sort_values(ascending=False)
st.subheader('Distribution of Number of Sessions per Customer')
plt.figure(figsize=(10, 6))
sns.histplot(sessions_per_customer, bins=50, kde=False)
plt.xlim(0, 10)
plt.title('Distribution of Number of Sessions per Customer')
plt.xlabel('Number of Sessions')
plt.ylabel('Frequency')
st.pyplot()