import streamlit as st
from streamlit_option_menu import option_menu
from phonepe_functions import *
import plotly.express as px
import plotly.graph_objects as go


def show_test_chart():
    # Assuming you have data containing Indian states and districts
    # Example data (replace this with your actual data)
    #data = {
        #'state': ['State A', 'State A', 'State B', 'State B'],
        #'district': ['District 1', 'District 2', 'District 3', 'District 4'],
        #'value': [100, 200, 150, 250]
    #}

    #df = pd.DataFrame(data)

    # Create a Sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=map_user_list["states"],
        parents=map_user_list["districts"],
        values=map_user_list['registeredUsers'],
    ))

    # Update layout
    fig.update_layout(
        title='Indian States and Districts Sunburst Chart',
        sunburstcolorway=["#f0f0f0", "#cfcfcf", "#afafaf", "#8f8f8f", "#6f6f6f", "#4f4f4f", "#2f2f2f"],  # Optional: customize color scheme
    )

    # Show the chart
    #st.plotly_chart(fig, use_container_width=True)
    fig.show()
pass

#streamlit UI

st.set_page_config (layout="wide")
st.title ("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu", ["HOME","DATA EXPLORATION","TOP CHART"])

if select == "HOME":
    if st.button(label="Insert PhonePe Pulse Data into DB", type="primary"):
        insert_data_from_file_to_sql("D:\Python_Proj\PhonePe_Data\pulse\data")
    
    pass
elif select == "DATA EXPLORATION":
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method_1 = st.radio('Select The Method', ["Aggregated Insurance analysis", "Aggregated Transaction Analysis", "Aggregated User Analysis"])
        
        if method_1 == "Aggregated Insurance analysis":
            aggregated_insurance = get_dataframe_from_db("select * from phonepe_data.agg_insu_list;")
            #year = st.slider(label = "select the year", min_value=2020, max_value=2024, value=None)
            year = st.selectbox (label= "select the year", key = "select the year", options= aggregated_insurance["year"].unique())
            if year:
                if st.button("Show Graph", key= "show_graph", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(aggregated_insurance, x = "states", y = "transaction_count", title = f"{year} INSURANCE TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(aggregated_insurance, x = "states", y = "transaction_amount", title = f"{year} TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)
                       

        elif method_1 == "Aggregated Transaction Analysis":
            aggregated_transaction = get_dataframe_from_db("select * from phonepe_data.agg_tran_list;")
            year = st.selectbox(label= "select the year", key = "select the year_1", options= aggregated_transaction["year"].unique())
            #year = st.slider(label = "select the year", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(aggregated_transaction, x = "states", y = "transaction_count", title = f"{year} TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(aggregated_transaction, x = "states", y = "transaction_amount", title = f"{year} TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)


        elif method_1 == "Aggregated User Analysis":
            aggregated_user = get_dataframe_from_db("select * from phonepe_data.agg_user_list;")
            year = st.selectbox(label= "select the year", key = "select the year_1", options= aggregated_user["year"].unique())
            #year = st.slider(label = "select the year", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(aggregated_user, x = "states", y = "transaction_count", title = f"{year} USER TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)

                    with st.container(border = True):
                        #fig_brands = px.pie(aggregated_user, values='brands', names='states')
                        #fig_brands = px.line(aggregated_user, x = "states", y = "brands", title = f"{year} USER BRANDS", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        fig_brands = px.bar(aggregated_user, x="states", y="transaction_count", color="brands", title="Long-Form Input")
                        st.plotly_chart(fig_brands, use_container_width=True)      
        
    with tab2:
        method_2 = st.radio('Select The Method', ["Map Insurance analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_2 == "Map Insurance analysis":
            map_insu_list = get_dataframe_from_db("select * from phonepe_data.map_insu_list;")
            year = st.selectbox(label= "select the year", key = "select the year_2", options= map_insu_list["year"].unique())
            #year = st.slider(label = "select the year", key= "select_year_2", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph2", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(map_insu_list, x = "states", y = "transaction_count", title = f"{year} INSURANCE TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(map_insu_list, x = "states", y = "transaction_amount", title = f"{year} INSURANCE TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)

        elif method_2 == "Map Transaction Analysis":
            map_tran_list = get_dataframe_from_db("select * from phonepe_data.map_tran_list;")
            year = st.selectbox(label= "select the year", key= "select_year_3", options= map_tran_list["year"].unique())
            #year = st.slider(label = "select the year",key= "select_year_3", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph_3", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(map_tran_list, x = "states", y = "transaction_count", title = f"{year} TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(map_tran_list, x = "states", y = "amount", title = f"{year} TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)

        elif method_2 == "Map User Analysis":
             map_user_list = get_dataframe_from_db("select * from phonepe_data.map_user_list;")
             year = st.selectbox(label= "select the year", key= "select_year_3", options= map_user_list["year"].unique())
            #year = st.slider(label = "select the year",key= "select_year_3", min_value=2020, max_value=2024, value=None)
             if year:
                if st.button("Show Graph", key= "show_graph_3", type= "primary"):
                    with st.container(border = True):
                        #fig = px.bar(map_user_list, x = "districts", y = "registeredUsers", title = f"{year} DISTRICT REGISTERED USER COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        #fig = px.sunburst(map_user_list, path=['states', 'districts', 'registeredUsers'], values='appOpens')
                        #fig = px.bar(map_user_list, x="states", y="registeredUsers", color="districts", title="Long-Form Input")
                        #st.plotly_chart(fig, use_container_width=True)


                        import plotly.graph_objects as go
                        import pandas as pd
                        import mysql.connector

                        client = getSqlClient_1()
                        cursor = client.cursor()
                        # Query your SQL database to retrieve hierarchical data
                        query = """SELECT states, districts, registeredUsers FROM map_user_list"""
                        df = pd.read_sql_query(query, client)

                        # Create a Sunburst chart
                        fig = go.Figure(go.Sunburst(
                            labels=df['districts'],
                            parents=df['states'],
                            values=df['registeredUsers'],
                        ))

                        # Update layout
                        fig.update_layout(
                            title='Sunburst Chart of States and Districts',
                            sunburstcolorway=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],  # Custom color scheme
                        )

                        # Show the chart
                        fig.show()

                        #show_test_chart()
                        
                       
                    
            
   
    with tab3:
        method_3 = st.radio ('Select The Method', ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_3 == "Top Insurance Analysis":
            top_insu_list = get_dataframe_from_db("select * from phonepe_data.top_insu_list;")
            year = st.selectbox(label= "select the year", key= "select_year_4", options= top_insu_list["year"].unique())
            #year = st.slider(label = "select the year",key= "select_year_4", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph_4", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(top_insu_list, x = "states", y = "transaction_count", title = f"{year} INSURANCE TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(top_insu_list, x = "states", y = "transaction_amount", title = f"{year} INSURANCE AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)

        elif method_3 == "Top Transaction Analysis":
            top_tran_list = get_dataframe_from_db("select * from phonepe_data.top_tran_list;")
            year = st.selectbox(label= "select the year", key= "select_year_5", options= top_tran_list["year"].unique())
            #year = st.slider(label = "select the year", key= "select_year_5", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph_5", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(top_tran_list, x = "states", y = "transaction_count", title = f"{year} TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        
                    with st.container(border = True):    
                        fig_amount = px.bar(top_tran_list, x = "states", y = "transaction_amount", title = f"{year} TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl)
                        st.plotly_chart(fig_amount, use_container_width=True)

        elif method_3 == "Top User Analysis":
            top_user_list = get_dataframe_from_db("select * from phonepe_data.top_user_list;")
            year = st.selectbox(label= "select the year", key= "select_year_5", options= top_user_list["year"].unique())
            #year = st.slider(label = "select the year", key= "select_year_5", min_value=2020, max_value=2024, value=None)
            if year:
                if st.button("Show Graph", key= "show_graph_5", type= "primary"):
                    with st.container(border = True):
                        fig_count = px.bar(top_user_list, x = "pincodes", y = "registeredUsers", title = f"{year} REGISTERED USER", color_discrete_sequence = px.colors.sequential.Bluered_r)
                        st.plotly_chart(fig_count, use_container_width=True)
                        

elif select == "TOP CHARTS":
    pass

