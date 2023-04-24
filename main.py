import streamlit as st
import plotly.express as px
from backend import get_data
import datetime

st.set_page_config(layout="wide")

# Add title, text input, slider, selectbox, and subheader
st.title("Upcoming Weather Forecast")

place = st.text_input("Place:")

days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")

option = st.selectbox("Select data to view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [int(dict["main"]["temp"])/10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            # Create a temperature plot
            figure = px.line(x = dates, y = temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            api_data = get_data(place, days)
            dates = [date["dt_txt"] for date in api_data]
            sky_condition =[f"images/{data['weather'][0]['main']}.png" for data in api_data]
            display_dates = [i.split('-') for i in dates]
            out=[]
            for i in range(len(dates)):
                out.append(datetime.datetime(int(display_dates[i][0]),int(display_dates[i][1]),int(display_dates[i][2][:2]),int(display_dates[i][2][3:5]),0))
            final = [x.strftime("%a, %b %d %H:%M") for x in out]
            st.image(sky_condition, width=100,caption=final)
    except KeyError:
        st.subheader("Please pick the name of a city that exists")