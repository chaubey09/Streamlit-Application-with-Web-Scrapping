import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup

# Function to create visualizations
def create_visualizations(data):
    st.subheader("Explore Your Data")

    # Use columns for a better layout
    col1, col2 = st.columns(2)
    
    with col1:
        numeric_columns = data.select_dtypes(include='number').columns.tolist()
        selected_column = st.selectbox("Select a numeric column for visualization:", numeric_columns)

        # Histogram
        if st.checkbox("Show Histogram"):
            st.write(f"Displaying Histogram for {selected_column}")
            plt.figure(figsize=(10, 5))
            sns.histplot(data[selected_column], bins=30, kde=True, color='skyblue')
            plt.title(f"Histogram of {selected_column}")
            st.pyplot(plt)

        # Box plot
        if st.checkbox("Show Box Plot"):
            st.write(f"Displaying Box Plot for {selected_column}")
            plt.figure(figsize=(10, 5))
            sns.boxplot(y=data[selected_column], color='lightgreen')
            plt.title(f"Box Plot of {selected_column}")
            st.pyplot(plt)

    # Scatter plot in the second column for better layout
    with col2:
        if len(numeric_columns) > 1:
            selected_column_2 = st.selectbox("Select another numeric column for scatter plot:", numeric_columns)
            if st.checkbox("Show Scatter Plot"):
                st.write(f"Displaying Scatter Plot between {selected_column} and {selected_column_2}")
                plt.figure(figsize=(10, 5))
                plt.scatter(data[selected_column], data[selected_column_2], color='coral')
                plt.xlabel(selected_column)
                plt.ylabel(selected_column_2)
                plt.title(f"Scatter Plot of {selected_column} vs {selected_column_2}")
                st.pyplot(plt)

# Main app structure
st.image("Screenshot 2024-09-27 161253.png", width=500)
st.title("Data Exploration Dashboard Made By Anmol Chaubey")
st.markdown("""
    <style>
    .css-18e3th9 {
        background-color: #E8F4F8; 
    }
    .css-1d391kg {
        color: #1D4E89;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "Data Upload", "Visualizations", "Web Scraping"])

# Content based on the selected page
if page == "Home":
    st.header("Welcome to the Data Exploration Dashboard")
    st.write("This app allows you to upload a dataset and explore it interactively with a variety of visualizations.")
    st.image("https://www.streamlit.io/images/brand/streamlit-mark-color.svg", width=300)

elif page == "Data Upload":
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Load the data into a DataFrame
        st.session_state.data = pd.read_csv(uploaded_file)
        st.success("Data Loaded Successfully!")
        st.dataframe(st.session_state.data)

elif page == "Visualizations":
    st.header("Visualize Your Data")

    # Check if data is available in session state
    if 'data' in st.session_state:
        create_visualizations(st.session_state.data)
    else:
        st.warning("Please upload a dataset first.")


# Web Scraping Page
elif page == "Web Scraping":
    st.header("Web Scraping")
    st.title("Simple Weather Web Scrapper")
    
    location = st.text_input("Enter a location to get weather information:")

    if st.button("Get Weather Info"):
        if location:
            try:
                # Handle location formatting (replace spaces with hyphens)
                location = location.replace(' ', '-')
                
                # Example scraping URL (replace with actual URL)
                url = f"https://www.weather-forecast.com/locations/{location}/forecasts/latest"
                
                response = requests.get(url)
                
                # Check if the request was successful
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract weather information (modify selectors based on actual HTML structure)
                    weather_info = soup.find('span', class_='phrase')
                    
                    if weather_info:
                        st.success(f"The current weather in {location.replace('-', ' ')} is: {weather_info.text}")
                    else:
                        st.error("Could not find weather information on the page.")
                elif response.status_code == 404:
                    st.error(f"Location '{location}' not found. Please check the spelling and try again.")
                else:
                    st.error("Could not retrieve weather information. Check the location or URL.")
            except Exception as e:
                st.error(f"Could not retrieve data for {location}. Error: {e}")
        else:
            st.warning("Please enter a location.")
