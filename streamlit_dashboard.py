import streamlit as st
import pandas as pd
import plotly.express as px
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

# Plotting Revenue Attribution by Marketing Channel
col1, col2 = st.columns(2)
with col1:
    st.subheader('Revenue Attribution by Marketing Channel')
    fig = px.pie(revenue_by_channel, values='REVENUE', names='MARKETINGCHANNEL', title='Revenue Attribution by Marketing Channel')
    st.plotly_chart(fig)

# Plotting Distribution of Customers per Marketing Channel as a Pie Chart
with col2:
    st.subheader('Distribution of Customers per Marketing Channel')
    customer_dist_by_channel = data.groupby('MARKETINGCHANNEL')['CUSTOMERID'].nunique().sort_values(ascending=False).reset_index()
    fig = px.pie(customer_dist_by_channel, values='CUSTOMERID', names='MARKETINGCHANNEL', title='Distribution of Customers per Marketing Channel')
    st.plotly_chart(fig)

st.info("""
The pie charts show revenue distribution and customer distribution by marketing channel. The top revenue channels are Direct NON-BRAND and SEO_BRAND, while the top customer channels are Direct NON-BRAND and SEO_BRAND.
""")

# Time Series Analysis of Touchpoints
st.subheader('Time Series Analysis of Touchpoints (Daily)')
fig = px.line(data, x='TIMESTAMP_TOUCHPOINT', title='Number of Touchpoints Over Time (Daily)')
fig.add_shape(dict(type='line', x0='2019-12-23', x1='2020-01-07', y0=0, y1=1, line=dict(color='green', width=2, dash='dash')))
st.plotly_chart(fig)

st.info("""
The line chart shows the number of touchpoints over time. As you can see, the touchpoints increase significantly around the Christmas holiday (between 23 December and 7 January).
""")

# Further Data Exploration Using All Columns
st.subheader('Distribution of Touchpoints by Year/Month/Hour of Day')
data['TIMESTAMP_TOUCHPOINT'] = pd.to_datetime(data['TIMESTAMP_TOUCHPOINT'], errors='coerce')

time_component = st.selectbox("Choose time component:", ["Year", "Month", "Hour", "Weekday"])

# Analyzing distribution of touchpoints over different time components
if time_component == "Year":
    fig = px.histogram(data, x='YEAR', title='Distribution of Touchpoints by Year')
    st.plotly_chart(fig)
elif time_component == "Month":
    fig = px.histogram(data, x='MONTH', title='Distribution of Touchpoints by Month')
    st.plotly_chart(fig)
elif time_component == "Hour":
    fig = px.histogram(data, x='HOUR', title='Distribution of Touchpoints by Hour of Day')
    st.plotly_chart(fig)
elif time_component == "Weekday":
    fig = px.histogram(data, x='WEEKDAY', title='Distribution of Touchpoints by Day of the week')
    st.plotly_chart(fig)

st.info("""
- Customer engagement is highest during the end of the year.
- Customer engagement is highest during the end of the day.
- Customer engagement is highest during the weekend.
""")

# Analyzing the number of sessions per customer
sessions_per_customer = data.groupby('CUSTOMERID')['SESSIONID'].nunique().sort_values(ascending=False)

st.subheader('Distribution of Number of Sessions per Customer')

# Plotting with Plotly Express
fig = px.histogram(sessions_per_customer, x='SESSIONID', nbins=50, title='Distribution of Number of Sessions per Customer')
fig.update_layout(xaxis=dict(range=[0, 10]), title='Distribution of Number of Sessions per Customer', xaxis_title='Number of Sessions', yaxis_title='Frequency')
st.plotly_chart(fig)

st.info("The histogram indicates a high concentration of customers with only one session, suggesting that a majority of the customer base might be engaging in one-time interactions. This finding can be pivotal for strategies focusing on customer retention and repeated engagement.")

st.header("References:")
st.markdown("- **Streamlit Documentation:** [Streamlit Docs](https://docs.streamlit.io/)")
st.markdown("- **Pandas Documentation:** [Pandas Docs](https://pandas.pydata.org/pandas-docs/stable/)")
st.markdown("- **Plotly Express Documentation:** [Plotly Express Docs](https://plotly.com/python/plotly-express/)")
