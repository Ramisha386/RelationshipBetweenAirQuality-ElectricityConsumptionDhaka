import streamlit as st
import plotly.express as px
import pandas as pd
import os
import imp
import warnings
import matplotlib.pyplot as plt
import calendar
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Air Quality", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Air Quality Monitoring")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl=st.file_uploader(":open_file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\Windows\Desktop\sample_project_1")
    df=pd.read_csv("testing.csv",encoding="ISO-8859-1")



col1,col2=st.columns((2))
#col3=st.columns((1))
df["Date"]=pd.to_datetime(df["Date"])

#Getting the min and max Date
startDate=pd.to_datetime(df["Date"]).min()
endDate=pd.to_datetime(df["Date"]).max()

with col1:
    date1=pd.to_datetime(st.date_input("Start Date",startDate))

with col2:
    date2=pd.to_datetime(st.date_input("End Date",endDate))

df=df[(df["Date"]>=date1) & (df["Date"]<=date2)].copy()

st.sidebar.header("Choose your filter: ")
# Create for Hour
hour = st.sidebar.multiselect("Pick your Time", df["Hour"].unique())
if not hour:
    df2 = df.copy()
else:
    df2 = df[df["Hour"].isin(hour)]

#Create for Month
#month = st.sidebar.multiselect("Pick your Month", df["Month"].unique())
#if not month:
#    df3 = df2.copy()
#else:
#    df3 = df2[df2["Month"].isin(month)]

#category_df = df3.groupby(by = ["AQI Category"], as_index = False)["AQI Category"]

#with col1:


st.subheader("Time Wise AQI Value")
fig = px.bar(df2, x = "Date", y = "AQI", template = "seaborn")
st.plotly_chart(fig, use_container_width=True, height = 200)


with col1:
    st.subheader("Pie Chart of AQI Category")
    fig = px.pie(df2, values = "AQI", names = "AQI Category",color='AQI Category',
    color_discrete_map={'Good':'limegreen',
                        'Moderate':'turquoise',
                        'Unhealthy for Sensitive Groups':'lightsteelblue',
                        'Unhealthy':'slateblue',
                        'Very Unhealthy':'lightcoral',
                        'Hazardous':'darkred'}, hole = 0.5)
    fig.update_traces(text = df2["AQI Category"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

#cmap = plt.cm.get_cmap('RdYlGn')
#cl1, cl2 = st.columns((2))

with col2:
    with st.expander("AQI Category over a range of Time"):
        st.write(df2.style.background_gradient(cmap="Oranges"))
        csv = df2.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "PieChart.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


df2["month_year"] = df2["Date"].dt.to_period("M")
st.subheader('Time Series Analysis')



#linechart = df2.groupby(df2["month_year"].dt.strftime("%Y : %b"))["AQI"].mean().reset_index()
#linechart['month_year'] = pd.Categorical(linechart['month_year'], categories=custom_months_order, ordered=True)
#linechart = linechart.sort_values('month_year')
#fig2 = px.line(linechart, x="month_year", y="AQI", labels={"month_year": "Month", "AQI": "AQI"}, height=500, width=1000, template="gridon")

#Another way
linechart = df2.groupby(df2["month_year"].dt.strftime("%Y : %b"))["AQI"].mean().reset_index()
#linechart = linechart.sort_values('month_year')
#linechart = linechart.sort_values(by='month_year', key=lambda month_year: {v:i for i,v in enumerate((calendar.month_abbr[1:]))}.get(month_year))
fig2 = px.line(linechart, x = "month_year", y="AQI", labels = {"Month": "AQI"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')
