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

# Hide Streamlit style
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

# Disable deprecated pyplot global use warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load the data from the provided file
file_path = 'Customerattributiondata.csv'
data = pd.read_csv(file_path, delimiter='\t')
data2 = data.copy()

# Display the first few rows of the dataset to understand its structure
st.subheader('DataFrame Overview')
st.write(data.head())

# Basic Data Overview: Checking for missing values and data types
st.subheader('Summary of a DataFrame')
buffer = io.StringIO()
data.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Provide information about the data
st.info("""
This DataFrame contains 13,304 rows and 5 columns. It features data related to customer interactions, including customer IDs, session IDs, timestamp of touchpoints, marketing channels, and revenue. The DataFrame has 1142 non-null values for revenue, indicating that not all customers generated revenue.
""")

# Filter and prepare the revenue data
df = data[data['REVENUE'].notnull() & (data['REVENUE'] != '')]
df.loc[:, 'REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce')
revenue_by_channel = df.groupby('MARKETINGCHANNEL')['REVENUE'].sum().reset_index()

# Set custom color palette for Seaborn plots
custom_palette = "coolwarm"  # Using a named palette
sns.set_palette(custom_palette)

# Plotting Revenue Attribution by Marketing Channel
col1, col2 = st.columns(2)
with col1:
    st.subheader('Revenue Attribution by Marketing Channel')
    plt.figure(figsize=(10, 6))
    plt.pie(revenue_by_channel['REVENUE'], labels=revenue_by_channel['MARKETINGCHANNEL'], autopct='%1.1f%%', startangle=90)
    st.pyplot()

# Plotting Distribution of Customers per Marketing Channel as a Pie Chart
with col2:
    st.subheader('Distribution of Customers per Marketing Channel')
    customer_dist_by_channel = data.groupby('MARKETINGCHANNEL')['CUSTOMERID'].nunique().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(10, 6))
    plt.pie(customer_dist_by_channel['CUSTOMERID'], labels=customer_dist_by_channel['MARKETINGCHANNEL'], autopct='%1.1f%%', startangle=90)
    st.pyplot()

st.info("""
The pie charts show revenue distribution and customer distribution by marketing channel. The top revenue channels are Direct NON-BRAND and SEO_BRAND, while the top customer channels are Direct NON-BRAND and SEO_BRAND.
""")

# Time Series Analysis of Touchpoints
st.subheader('Time Series Analysis of Touchpoints (Daily)')
plt.figure(figsize=(11, 7))
data['TIMESTAMP_TOUCHPOINT'] = pd.to_datetime(data['TIMESTAMP_TOUCHPOINT'], errors='coerce')
data.set_index('TIMESTAMP_TOUCHPOINT').resample('D').size().plot()
plt.axvline(x=pd.Timestamp('2019-12-23'), linestyle="--", linewidth=2, color="green")
plt.axvline(x=pd.Timestamp('2020-01-07'), linestyle="--", linewidth=2, color="green")
plt.xlabel('Date')
plt.ylabel('Number of Touchpoints')
st.pyplot()

st.info("""
The line chart shows the number of touchpoints over time. As you can see, the touchpoints increase significantly around the Christmas holiday (between 23 December and 7 January).
""")

# Further Data Exploration Using All Columns
st.subheader('Distribution of Touchpoints by Year/Month/Hour of Day')
data['TIMESTAMP_TOUCHPOINT'] = pd.to_datetime(data['TIMESTAMP_TOUCHPOINT'], errors='coerce')

# Extracting date components from 'TIMESTAMP_TOUCHPOINT'
data['YEAR'] = data['TIMESTAMP_TOUCHPOINT'].dt.year
data['MONTH'] = data['TIMESTAMP_TOUCHPOINT'].dt.month
data['DAY'] = data['TIMESTAMP_TOUCHPOINT'].dt.day
data['HOUR'] = data['TIMESTAMP_TOUCHPOINT'].dt.hour
data['WEEKDAY'] = data['TIMESTAMP_TOUCHPOINT'].dt.day_name()

time_component = st.selectbox("Choose time component:", ["Year", "Month", "Hour", "WeekDay"])

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
elif time_component == "WeekDay":
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.countplot(x='WEEKDAY', data=data, ax=ax)
    ax.set_title('Distribution of Touchpoints by Day of the week')
    st.pyplot(fig)

st.info("""
- Customer engagement is highest during the end of the year.
- Customer engagement is highest during the end of the day.
- Customer engagement is highest during the weekend.
""")

# Analyzing the number of sessions per customer"
sessions_per_customer = data.groupby('CUSTOMERID')['SESSIONID'].nunique().sort_values(ascending=False)

st.subheader('Distribution of Number of Sessions per Customer')

# Plotting with Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(sessions_per_customer, bins=50, edgecolor='black', alpha=0.7)

ax.set_xlim(0, 10)

ax.set_title('Distribution of Number of Sessions per Customer')
ax.set_xlabel('Number of Sessions')
ax.set_ylabel('Frequency')

# Display the plot in Streamlit
st.pyplot(fig)


st.text("### References:")
st.markdown("- **Streamlit Documentation:** [Streamlit Docs](https://docs.streamlit.io/)")
st.markdown("- **Pandas Documentation:** [Pandas Docs](https://pandas.pydata.org/pandas-docs/stable/)")
st.markdown("- **Matplotlib Documentation:** [Matplotlib Docs](https://matplotlib.org/stable/contents.html)")
st.markdown("- **Seaborn Documentation:** [Seaborn Docs](https://seaborn.pydata.org/)")

st.info("The histogram indicates a high concentration of customers with only one session, suggesting that a majority of the customer base might be engaging in one-time interactions. This finding can be pivotal for strategies focusing on customer retention and repeated engagement.")
