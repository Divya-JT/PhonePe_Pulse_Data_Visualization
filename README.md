# PhonePe_Pulse_Data_Visualization
PhonePe Pulse data visualization and exploration 
Sample Python Project to demonstrate retreaving Phonepe pulse data and visualizing the data.

Libraries and tools are used in this project:
  1. Github - to retrieve Phonepe pulse data
  2. Pandas DataFrame - to convert the rectrieved pulse data
  3. MYSQL - Backend storage
  4. Streamlit - Frontend development
  5. Plotly - to visualize the pulse data in an interactive way
  6. Pydeck - to create interactive 3D mapping and geospatial visualization
  7. Geo pandas - to make working with geospatial data

## Installation

### Running using streamlit

1. Install the below requried library by using `pip install <library_name>`
    -  _streamlit ==1.30.0
    -  streamlit-option-menu==0.3.12
    - streamlit-extras==0.4.0
    - pydeck==0.8.1b0
    - pandas==2.1.4
    - geopandas==0.14.3
    - plotly==5.18.0
    - mysql-connector-python==8.3.0_

3. Run the Streamlit application using the following command 
    - To run with csv data use `streamlit run phonepe_py.py` 


## USAGE

To run this project, follow these steps:

1. Clone the repository: https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization.git
2. Run the streamlit appliction using the command `streamlit run phonepe_py.py`

## FEATURES:

### The following features are available in the PhonePe Pulse Data Visualization:

1. Data Exploration Screen
This screen will give the ovearall view of the PhonePe Pulse Data using plotly graphs.
![image](https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization/assets/168666654/5aeac332-ec4c-443e-995e-6eb625ed1495)


2. Data Visualization Screen
In data visualization we can get some basic insights through india map(3D).
![image](https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization/assets/168666654/177e4b06-5e17-42a3-8a3c-900232c5262d)


3. Top Chart Screen
This screen will give visual representation of the Top 10 States, Districts, Pincodes & mobile models based on Transaction type, year and Quarter in an interactive way.
![image](https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization/assets/168666654/59042947-402c-46fb-a9ba-0565ad9e5830)
![image](https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization/assets/168666654/f2c0a3df-1587-443d-94ed-f97a77a1ff9e)


4. Data Analysis Screen
In this screen analyses the data with 10 queies and provides result in a tabuler and chart form for better understanding.
![image](https://github.com/Divya-JT/PhonePe_Pulse_Data_Visualization/assets/168666654/6d6f67de-1825-4733-a6b2-3aad63ba47f6)

