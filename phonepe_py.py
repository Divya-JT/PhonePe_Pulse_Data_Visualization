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
        
    


## UI for top chart


def top_transaction(data):
    Year = data["year"]
    Quarter = data["quater"]
    st.markdown("### :violet[State]")

    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_tranaction_state(Year,Quarter)
            
            fig = px.pie(df, values='Total_Amount',
                                names='States',
                                title='Top 10 Transaction Amount',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:

            df = search_tranaction_state1(Year,Quarter)
            fig = px.pie(df, values='Transactions_Count',
                                names='States',
                                title='Top 10 Transactions',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    
    st.markdown("### :violet[District]")
    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_tranaction_district(Year,Quarter)
            fig = px.pie(df, values='Total_Amount',
                                names='Districts',
                                title='Top 10 Transaction Amount',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            df = search_tranaction_district1(Year,Quarter)
            fig = px.pie(df, values='Transactions_Count',
                                names='Districts',
                                title='Top 10 Transactions',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    
    st.markdown("### :violet[Pincode]")
    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_tranaction_pincode(Year,Quarter)
            
            fig = px.pie(df, values='Total_Amount',
                                names='Pincodes',
                                title='Top 10 Transaction Amount',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            df = search_tranaction_pincode1(Year,Quarter)
        
            fig = px.pie(df, values='Transactions_Count',
                                names='Pincodes',
                                title='Top 10 Transactions',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    return None

    
def top_insurance(data):
    Year = data["year"]
    Quarter = data["quater"]
    
    st.markdown("### :violet[State]")
    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_insurance_state(Year,Quarter)

            fig = px.pie(df, values='Total_Amount',
                                names='States',
                                title='Top 10 Policy Amount',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            df = search_insurance_state1(Year,Quarter)
            
            fig = px.pie(df, values='Transactions_Count',
                                names='State',
                                title='Top 10 Policies Count',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown("### :violet[District]")
    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_insurance_district(Year,Quarter)
            fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10 Policy Amount',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            df = search_insurance_district1(Year,Quarter)
            
            fig = px.pie(df, values='Transactions_Count',
                                names='District',
                                title='Top 10 Policies Count',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown("### :violet[Pincode]")
    with st.container(border=True):
        col1,col2 = st.columns([1,1],gap="small")
        with col1:
            df = search_insurance_pincode(Year,Quarter)
            
            fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10 Policy Amount',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            df = search_insurance_pincode1(Year,Quarter)
            fig = px.pie(df, values='Transactions_Count',
                                names='Pincode',
                                title='Top 10 Policies Count',
                                color_discrete_sequence=px.colors.sequential.Plotly3,
                                hover_data=['Total_Amount'],
                                labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    return None


def  get_user_brand(Year, Quarter):
    df = user_brand(Year,Quarter)
    fig = px.bar(df,
                    title='Top 10',
                    x="Total_Users",
                    y="Brand",
                    orientation='h',
                    color='Avg_Percentage',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True)   
    return None


def top_users(data):
    Year = data["year"]
    Quarter = data["quater"]
    col1,col2 = st.columns(2, gap="large")
    col3,col4 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("### :violet[Brands]")

            if Year in [2022,2023] and Quarter in [1,2,3,4]:
                if not(Year == 2022 and Quarter == 1):
                    st.markdown("#### Sorry No Data to Display")
                else:
                    get_user_brand(Year, Quarter)
            else:
                get_user_brand(Year, Quarter)

    with col2:
        with st.container(border=True):
            st.markdown("### :violet[District]")
            df = user_district(Year,Quarter)
            
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

    with col3:
        with st.container(border=True):             
            st.markdown("### :violet[Pincode]")
            df = user_pincode(Year,Quarter)
            fig = px.pie(df,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    with col4:
        with st.container(border=True):             
            st.markdown("### :violet[State]")
            df = user_state(Year,Quarter)
            
            fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
    return None




def load_top_chart_page():
    with st.container(border=True):
        st.write("")
        space1,type_col, year_col, quater_col, space2 = st.columns([2,4,4,4,2], gap="large")
        with type_col:
            Type = st.selectbox("**Type**", ("Transactions", "Users", "Insurance"))
            if Type == "Insurance":
                year_min = 2020
            else:
                year_min = 2018
        with year_col:
            Year = st.slider("**Year**", min_value=year_min, max_value=2023)
            if (Type == "Insurance") & (Year == 2020):
                quater_min = 2
            else:
                quater_min = 1
        with quater_col:
            Quarter = st.slider("**Quarter**", min_value=quater_min, max_value=4)
        
        st.write("")

    data = {"type":Type, "year":Year, "quater":Quarter}

    
    # get top transactions types
    if Type == "Transactions":
        top_transaction(data)

    if Type == "Insurance":
        top_insurance(data)
        pass

    if Type == "Users":
        top_users(data)

    return None




def load_data_analysis_page():
    with st.container(border=True):
        st.title("Select Query")
    
        options = ["Select Query",
                   "What is the top 10 State list having highest transaction rate?", #1
                   "What is the top 10 Districts list having highest transaction rate?", #2
                   "What is the top 10 State list having highest Insurance transaction rate?", #3
                   "What is the top 10 Districts list having highest Insurance transaction rate?", #4
                   "Which states have the highest and lowest insurance transaction?", #5
                   "Top 10 brands having the highest transaction values?", #6
                   "what is the Top 10 States having higest number of users?", #7
                   "Which year having the highest amount has transferred?", #8 Agregated transaction
                   "Which states contribute the most to the overall revenue generated by transactions?", #9
                   "which state contributed lowest revenue rate by transactions?", #10
                   ] 
        query = st.selectbox(label= "Select Query", options= options, label_visibility= "visible", placeholder="Select Playlist", index=0)

    if(query):
        index = options.index(query)
        if index != 0:
            st.write("**Result**")
            query = None
            if(index == 1): #What is the top 10 State list having highest transaction rate?
                query = """select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_tran_list group 
                    by states order by Total desc limit 10"""
                

            elif(index == 2): #What is the top 10 Districts list having highest transaction rate?
                query = """select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_tran_list group 
                    by districts order by Total desc limit 10"""
                
            elif(index == 3): #What is the top 10 State list having highest Insurance transaction rate?
                query = """select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_insu_list group 
                    by states order by Total desc limit 10"""
                

            elif(index == 4): #What is the top 10 Districts list having highest insurance transaction rate?
                query = """select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_insu_list group 
                    by districts order by Total desc limit 10"""
            elif(index == 5): #Which states have the highest and lowest insurance transaction?
                query = """(select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_insu_list group 
                    by districts order by Total desc limit 1 ) UNION ALL
                    (select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_insu_list group 
                    by districts order by Total asc limit 1 )"""
                
            elif(index == 6): #Top 10 brands having the highest transaction values?
                query = """select brands, sum(transaction_count) as Total_Count 
                        from agg_user_list 
                        group by brands order by Total_Count desc limit 10"""
                
            elif(index == 7): #what is the Top 10 States having higest number of users and its app retention?
                query = """select states, sum(registeredUsers) as Total_Users, sum(appOpens) 
                    as Total_Appopens from map_user_list 
                    group by states order by Total_Users desc limit 10"""
                
            elif(index == 8): #Which year having the highest amount has transferred?
                query = """select year, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_tran_list group 
                    by year order by Total desc limit 1"""
                
            elif(index == 9): #Which states contribute the most to the overall revenue generated by transactions?
                query = """select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_tran_list group 
                    by states order by Total desc limit 1"""
                
            elif (index == 10): #which state contributed lowest revenue rate by transactions?
                query = """select districts,states, sum(transaction_count) as Total_Transactions_Count, sum(amount) 
                    as Total from map_tran_list group 
                    by districts, states order by Total asc limit 1"""
            

        try:    
            col1, col2 = st.columns([1,1])

            with col1:
                result = get_dataframe_from_db(query)

                pd.DataFrame(result)
                st.write(result)
            with col2:
                result = get_dataframe_from_db(query)

                fig = px.bar(data_frame= result,
                            title=options[index],
                            x="states",
                            y = ["Total_Transactions_Count", "Total"],
                            color='states',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

        except Exception as error:
            print("Query Error:", error)

     


def load_main_page():
    
    with st.sidebar:
        select = option_menu("Main Menu", ["HOME","DATA EXPLORATION", "DATA VISUALIZATION","TOP CHART", "DATA  ANALYSIS"])

    if select == "HOME":
        load_home_page()
        pass
    elif select == "DATA EXPLORATION":
        load_data_exploration_page()
        pass
    elif select == "DATA VISUALIZATION":
        load_data_visualization_page()
        pass
    elif select == "TOP CHART":
        load_top_chart_page()
        pass
    elif select == "DATA  ANALYSIS":
        load_data_analysis_page()
        pass



st.set_page_config(layout="wide", page_title="Phonepe Data Visuvalization", )
load_main_page()