import streamlit as st
import argparse
import os
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
from phonepe_functions import *
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import geo_map as gm
from scripts.data.hover_data import *
from scripts.pulse.layers import *
from scripts.pulse.viewstate import *
from scripts.data.aggerated_data import *
from scripts.data.top_data import *

#streamlit UI

def detail_col_1():
    state_map = gpd.read_file("geo_map/indian_states.geojson")
    states = state_map["ST_NM"].to_list()
    states.insert(0,"All-India")
    
    space1,trans_col,year_col,q_col, allindia_col,recenter_col, space2 = st.columns([1,9,6,10,12,9,1])

    with trans_col:
        data_option = st.selectbox(label = "" ,options= ["Transaction", "User", "Insurance"], index=0, label_visibility="collapsed")
    with year_col:
        year_option = [2018,2019,2020,2021,2022,2023]
        if data_option == "Insurance":
            year_option = [2020,2021,2022,2023]
        
        year = st.selectbox(label = "" ,options= year_option, index=year_option.index(2023), label_visibility="collapsed")
    with q_col:
        quater_options = ["Q1(Jan - Mar)","Q2(Apr - Jun)", "Q3(Jul - Sep)", "Q4(Oct - Dec)"]
        if (data_option == "Insurance") & (year == 2020):
            quater_options = ["Q2(Apr - Jun)", "Q3(Jul - Sep)", "Q4(Oct - Dec)"]
        quater = st.selectbox(label="", options =quater_options,index=quater_options.index("Q4(Oct - Dec)"), label_visibility="collapsed")

    with recenter_col:
        with stylable_container(key="Recenterbutton",
                                css_styles="""button {background-color:#87d0ab}"""):
            recenter_button = st.button("Recenter Map")

    with allindia_col:
        load_map = st.selectbox(label= "", options=states,index=states.index("All-India"), key="load_map", label_visibility="collapsed")

    
    return data_option, year, quater, recenter_button, load_map



def detail_col_3(load_map, data_option):
    if load_map == "All-India":
        state_b, district_b, pincode_b = st.columns([5,5,5])
        
        with state_b:
            with stylable_container(key="statebutton",
                                    css_styles="""button {background-color:#121326; border-radius: 18px;}"""):
                state_button = st.button("State")
        with district_b:
            with stylable_container(key="districtbutton",
                                    css_styles="""button {background-color:#121326; border-radius: 18px;}"""):
                district_button = st.button("District")
        with pincode_b:
            with stylable_container(key="pincodebutton",
                                    css_styles="""button {background-color:#121326; border-radius: 18px;}"""):
                pincode_button = st.button("Pincode")
    else:
        district_b, pincode_b = st.columns([5,5], gap="small")
        
        with district_b:
            with stylable_container(key="districtbutton",
                                    css_styles="""button {background-color:#121326; border-radius: 18px;}"""):
                district_button = st.button("District")
        with pincode_b:
            with stylable_container(key="pincodebutton",
                                    css_styles="""button {background-color:#121326; border-radius: 18px;}"""):
                pincode_button = st.button("Pincode")


    top_data = "District"
    if district_button:
        top_data ="District"
    if pincode_button:
        top_data = "Pincode"
    if load_map == "All-India":
        top_data = "State"
        if district_button:
            top_data ="District"
        if pincode_button:
            top_data = "Pincode"
        if state_button:
            top_data = "State"
    return top_data

def detail_info_col(info_dict):
    data = aggregated_data(info_dict)
    data_option = info_dict["data_option"]
    if data_option == "Transaction":
        #st.write("All PhonePe transactions (UPI + Cards + Wallets)")
        total_count = data["Count"].sum()
        total_payement = data["Amount"].sum()
        avg_amount = total_payement/total_count
        total_count = '{:,.2f}'.format(total_count)
        total_payement = '{:,.2f}'.format(total_payement)
        total_payement = '₹'+str(total_payement)
        avg_amount = '{:,.2f}'.format(avg_amount)
        avg_amount = '₹'+str(avg_amount)
        st.markdown(f"""<p style='margin: 0;'>All PhonePe transactions (UPI + Cards + Wallets)</p>
                    <h2 style='color:#b069ff; margin: 0;'>{total_count}</h2>
                    <p style='margin: 0;'>Total payment value</p>
                    <h3 style='color:#b069ff; margin: 0;'>{total_payement}</h3>
                    <p style='margin: 0;'>Avg. transaction value</p>
                    <h2 style='color:#b069ff; margin: 0;'>{avg_amount}</h2>
                    """, unsafe_allow_html=True)
        
    elif data_option == "User":
        if isinstance(data, dict):
            reg_user = data["registeredUsers"]
            app_opens = data["appOpens"]
        else:
            reg_user =  data["registeredUsers"]
            app_opens = data["appOpens"]
            reg_user = reg_user.drop_duplicates()[0]
            app_opens = app_opens.drop_duplicates()[0]
        
        reg_user = '{:,.2f}'.format(reg_user)
        app_opens = '{:,.2f}'.format(app_opens)
        #st.write(type(app_opens))
        if app_opens == "0.00":
            app_opens = "Unavailable"
        quater = info_dict["quater"]
        year = info_dict["year"]
        st.markdown(f"""<p style='margin: 0;'>Registered PhonePe users till {quater} {year}</p>
                    <h2 style='color:#b069ff; margin: 0;'>{reg_user}</h2>
                    <p style='margin: 0;'>PhonePe app opens in {quater} {year}</p>
                    <h3 style='color:#b069ff; margin: 0;'>{app_opens}</h3>
                    """, unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    
    else:
        ins_purchased = data["paymentInstruments"][0]["count"]
        ins_amount = data["paymentInstruments"][0]["amount"]
        avg_amount = ins_amount/ins_purchased
        ins_purchased = '{:,.2f}'.format(ins_purchased)
        ins_amount = '{:,.2f}'.format(ins_amount)
        ins_amount = '₹'+str(ins_amount)
        avg_amount = '{:,.2f}'.format(avg_amount)
        avg_amount = '₹'+str(avg_amount)
        load_map = info_dict["data_option"]
        st.markdown(f"""<p style='margin: 0;'>{load_map} Insurance Policies Purchased (Nos.)</p>
                    <h2 style='color:#b069ff; margin: 0;'>{ins_purchased}</h2>
                    <p style='margin: 0;'>Total premium value</p>
                    <h3 style='color:#b069ff; margin: 0;'>{ins_amount}</h3>
                    <p style='margin: 0;'>Average premium value</p>
                    <h2 style='color:#b069ff; margin: 0;'>{avg_amount}</h2>
                    """, unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    return None


## UI for home screen
def load_home_page():
    #st.title ("PHONEPE DATA VISUALIZATION AND EXPLORATION")
    st.subheader("PHONEPE DATA VISUALIZATION AND EXPLORATION")
    #st.markdown("**PHONEPE DATA VISUALIZATION AND EXPLORATION**")

    if st.button(label="Insert PhonePe Pulse Data into DB", type="primary"):
        insert_data_from_file_to_sql("D:\Python_Proj\PhonePe_Data\pulse\data")


## UI for Data Exploration
def load_data_exploration_page():
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
                        
                        fig = px.sunburst(map_user_list, path=['states', 'districts'], values='registeredUsers')
                        st.plotly_chart(fig, use_container_width=True)
                    
            

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
                        

## UI for data visualization
def load_data_visualization_page():
        
        with stylable_container(key="option_container", css_styles="""
                                {background-color: #034424;}"""):
            st.write("")

            data_option, year, quater, recenter_button,load_map  = detail_col_1()
            
            st.write("")

            # draw map
            info_dict =  {"data_option":data_option,"year":year, "quater":quater, "state": load_map, "top_data": "State"}
                
                    
            initial_view_state = viewstate(load_map)

        layer = list(create_layers(info_dict))
        if data_option == "Transaction":
            r = pdk.Deck(
            initial_view_state=initial_view_state,
            layers=layer, map_provider=None, tooltip={"html": """<p style= 'margin: 0; line-height: 1;'>{state}</p> 
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{ST_NM}</b>
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>All Transactions</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Count}</b> 
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Total Payment Value</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Amount}</b> 
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Avg. Transactions Value</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Avg}</b>""", 
                                                        "style": {"color": "white", "backgroundColor": "#034424"}})
            
        elif data_option =="User":
            r = pdk.Deck(
            initial_view_state=initial_view_state,
            layers=layer, map_provider=None, tooltip={"html": """<p style= 'margin: 0; line-height: 1;'>{state}</p> 
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{ST_NM}</b>
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Registered Users</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{registeredUsers}</b> 
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>App Opens</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{appOpens}</b> """, 
                                                        "style": {"color": "white", "backgroundColor": "#034424"}})
        else:
            r = pdk.Deck(
            initial_view_state=initial_view_state,
            layers=layer, map_provider=None, tooltip={"html": """<p style= 'margin: 0; line-height: 1;'>{state}</p> 
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{ST_NM}</b>
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Insurance Policies(Nos.)</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Count}</b> 
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Total Premium Value</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Amount}</b> 
                                                    <p style= 'margin: 0; line-height: 1; color:white;'>Avg. Premium Value</p>
                                                    <b style='color:#b069ff; margin: 0;line-height: 3;'>{Avg}</b>""", 
                                                        "style": {"color": "white", "backgroundColor": "#034424"}})

        if recenter_button:
            r.initial_view_state = initial_view_state
        with st.spinner("Loading the Map"):
            c = st.pydeck_chart(r)
            


        return None
        
    


## UI fortop chart
def load_top_chart_page():
    pass


def load_main_page():
    
    with st.sidebar:
        select = option_menu("Main Menu", ["HOME","DATA EXPLORATION", "DATA VISUALIZATION","TOP CHART"])

    if select == "HOME":
        load_home_page()
        pass
    elif select == "DATA EXPLORATION":
        load_data_exploration_page()
        pass
    elif select == "DATA VISUALIZATION":
        load_data_visualization_page()
        pass
    elif select == "TOP CHARTS":
        load_top_chart_page()
        pass



st.set_page_config(layout="wide", page_title="Phonepe Data Visuvalization", )
load_main_page()