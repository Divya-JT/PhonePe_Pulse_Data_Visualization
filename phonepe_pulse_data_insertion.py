import mysql.connector
import os
import json
import pandas as pd 
import mysql.connector
#import numpy as np
#import plotly.express as px



def change_data_insertion_status(status):
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        cursor.execute("DELETE FROM data_insertion_status;")
        client.commit()
        
        query = """INSERT INTO data_insertion_status (sno, status) VALUES(%s,%s)"""
        values = ("1", 
                  status)
        cursor.execute(query, values)
        client.commit()
        client.close()

    except Exception as err:
        print("change_data_insertion_status => Error : ", err)


def check_data_available_in_sql():
    status = "0"
    try:
        client = getSqlClient_1()
        cursor = client.cursor()
        
        cursor.execute("SELECT status FROM data_insertion_status;")

        myresult = cursor.fetchall()
        for result in myresult:
            status = result

        client.close()            
    except Exception as err:
        print("check_data_available_in_sql => Error : ", err)
        

    return status

# STORING THE DATAFRAME IN TO MSQL DATABASE
def create_database():
    db_client = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "4444")
    cursor = db_client.cursor()
    
    # TO CREATE A DATABASE    
    query = "CREATE DATABASE IF NOT EXISTS Phonepe_data"      
    cursor.execute(query)

    

# Sql Client with exist DB
def getSqlClient_1():
    client = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "4444",
        database = "Phonepe_data"
    )
    return client

# create phonepe database if not exist
create_database()


# create tables
def create_database_and_table():
    client = getSqlClient_1()
    cursor = client.cursor()
    
    # Create "agg_insu_list" TABLE 
    query = """create table IF NOT EXISTS agg_insu_list(states varchar(255), year int, quarter int, transaction_type varchar(255), transaction_count bigint, transaction_amount bigint)"""
    cursor.execute(query)

    # Create "agg_tran_list" table
    query ="""create table IF NOT EXISTS Phonepe_data.agg_tran_list(states varchar(255), year int, quarter int, transaction_type varchar(255), transaction_count bigint, transaction_amount bigint)"""
    cursor.execute(query)

    # Create "agg_user_list" table
    query = """create table IF NOT EXISTS agg_user_list(states varchar(255), year int, quarter int, brands varchar(255), transaction_count bigint, percentage bigint)"""
    cursor.execute(query)

    # Create "map_insu_list" table
    query = """create table IF NOT EXISTS map_insu_list(states varchar(255), year int, quarter int, districts varchar(255), transaction_count bigint, amount bigint)"""
    cursor.execute(query)

    # Create "map_tran_list" table
    query = """create table IF NOT EXISTS map_tran_list(states varchar(255), year int, quarter int, districts varchar(255), transaction_count bigint, amount bigint)"""
    cursor.execute(query)

    # Create "map_user_list" table
    query = """create table IF NOT EXISTS map_user_list(states varchar(255), year int, quarter int, districts varchar(255), registeredUsers bigint, appOpens bigint)"""
    cursor.execute(query)

    # Create "top_insu_list" table
    query = """create table IF NOT EXISTS top_insu_list(states varchar(255), year int, quarter int, pincodes int, transaction_count bigint, transaction_amount bigint)"""
    cursor.execute(query)

    # Create "top_tran_list" table
    query = """create table IF NOT EXISTS top_tran_list(states varchar(255), year int, quarter int, pincodes int, transaction_count bigint, transaction_amount bigint)"""
    cursor.execute(query)

    # Create "top_user_list" table
    query = """create table IF NOT EXISTS top_user_list(states varchar(255), year int, quarter int, pincodes int, registeredUsers bigint)"""
    cursor.execute(query)

    # Create "top_user_list" table
    query = """create table IF NOT EXISTS data_insertion_status(sno varchar(2), status varchar(2))"""
    cursor.execute(query)

    client.close()


def remove_phonepe_database():

    try:
        client = getSqlClient_1()

        cursor = client.cursor()
        # delete database
        cursor.execute("DROP DATABASE IF EXISTS Phonepe_data;")
        client.close()

    except Exception as err:
        print(err)

    
    pass



# file_path => D:/Python_Proj/PhonePe/pulse/data
def insert_data_from_file_to_sql(file_path):
    try:
        # Remove the exist data
        remove_phonepe_database()
        # Create database
        create_database()
        create_database_and_table()

        # AGGRECATED INSURANCE
        fetch_and_insert_aggregated_insurance(file_path)
        # AGGREGATED TRANSACTION
        fetch_and_insert_agregated_transaction(file_path)
        #AGGREGATED USER
        fetch_and_insert_agregated_user(file_path)

        # MAP INSURANCE
        fetch_and_insert_map_insurance(file_path)
        # MAP TRANSACTION
        fetch_and_insert_map_transaction(file_path)
        # MSP USER
        fetch_and_insert_map_user(file_path)

        # TOP INSURANCE
        fetch_and_insert_top_insurance(file_path)
        #TOP TRANSACTION
        fetch_and_insert_top_transaction(file_path)
        # TOP USER
        fetch_and_insert_top_user(file_path)

        
        # change status
        change_data_insertion_status("1")

    except Exception as err:
        print("insert_data_from_file_to_sql => Error:", err)

    pass

# AGGRECATED INSURANCE
def fetch_and_insert_aggregated_insurance(file_path):
    path0 = file_path + "/aggregated/insurance/country/india/state/"
    agg_insu_list = os.listdir(path0)

    col0 = {"states":[], "year":[], "quarter":[], "transaction_type":[], "transaction_count":[], "transaction_amount":[]}

    for state in agg_insu_list:
        cur_states = path0 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                A = json.load(data)

                for i in A ["data"] ["transactionData"]:
                    name = i ["name"]
                    count = i ["paymentInstruments"] [0] ["count"]
                    amount = i ["paymentInstruments"] [0] ["amount"]
                    col0["transaction_type"].append (name)
                    col0["transaction_count"].append (count)
                    col0["transaction_amount"].append (amount)
                    col0["states"].append(state)
                    col0["year"].append(year)
                    col0["quarter"].append(int(file.strip(".json")))

    agg_insu_list = pd.DataFrame(col0)

    agg_insu_list["states"] = agg_insu_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    agg_insu_list["states"] = agg_insu_list["states"].str.replace('-', ' ')
    agg_insu_list["states"] = agg_insu_list["states"].str.title()
    agg_insu_list["states"] = agg_insu_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(agg_insu_list)

    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO agg_insu_list (states, year, quarter, transaction_type, transaction_count,transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = agg_insu_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()

    except Exception as err:
        print("fetch_and_insert_aggregated_insurance = Error : ", err)

pass # 


# AGGREGATED TRANSACTION
def fetch_and_insert_agregated_transaction(file_path):
    path1 = file_path + "/aggregated/transaction/country/india/state/"
    agg_tran_list = os.listdir(path1)

    col1 = {"states":[], "year":[], "quarter":[], "transaction_type":[], "transaction_count":[], "transaction_amount":[]}

    for state in agg_tran_list:
        cur_states = path1 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                B = json.load(data)
                
                for i in B ["data"] ["transactionData"]:
                    name = i ["name"]
                    count = i ["paymentInstruments"] [0] ["count"]
                    amount = i ["paymentInstruments"] [0] ["amount"]
                    col1 ["transaction_type"].append (name)
                    col1 ["transaction_count"].append (count)
                    col1 ["transaction_amount"].append (amount)
                    col1 ["states"].append(state)
                    col1 ["year"].append(year)
                    col1 ["quarter"].append(int(file.strip(".json")))

    agg_tran_list = pd.DataFrame(col1)


    agg_tran_list["states"] = agg_tran_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    agg_tran_list["states"] = agg_tran_list["states"].str.replace('-', ' ')
    agg_tran_list["states"] = agg_tran_list["states"].str.title()
    agg_tran_list["states"] = agg_tran_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(agg_tran_list)

    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO agg_tran_list (states, year, quarter, transaction_type, transaction_count, transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = agg_tran_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()
    except Exception as err:
        print("fetch_and_insert_agregated_transaction => Error : ", err)

    
pass


#AGGREGATED USER
def fetch_and_insert_agregated_user(file_path):
    path2 = file_path + "/aggregated/user/country/india/state/"
    agg_user_list = os.listdir(path2)

    col2 = {"states":[], "year":[], "quarter":[], "brands":[], "transaction_count":[], "percentage":[]}

    for state in agg_user_list:
        cur_states = path2 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                C = json.load(data)


                try:
                    for i in C ['data'] ['usersByDevice']:
                        brand = i ["brand"]
                        count = i ["count"]
                        percentage = i ["percentage"] 
                        col2 ["brands"].append (brand)
                        col2 ["transaction_count"].append (count)
                        col2 ["percentage"].append (percentage)
                        col2 ["states"].append(state)
                        col2 ["year"].append(year)
                        col2 ["quarter"].append(int(file.strip(".json")))

                except:
                    pass

    agg_user_list = pd.DataFrame(col2)

    agg_user_list["states"] = agg_user_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    agg_user_list["states"] = agg_user_list["states"].str.replace('-', ' ')
    agg_user_list["states"] = agg_user_list["states"].str.title()
    agg_user_list["states"] = agg_user_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(agg_user_list)


    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO agg_user_list (states , year , quarter , brands , transaction_count, percentage) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = agg_user_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()
    except Exception as err:
        print("fetch_and_insert_agregated_user => Error : ", err)

    
pass 

# MAP INSURANCE
def fetch_and_insert_map_insurance(file_path):
    path3 = file_path + "/map/insurance/hover/country/india/state/"
    map_insu_list = os.listdir(path3)

    col3 = {"states":[], "year":[], "quarter":[], "districts":[], "transaction_count":[], "amount":[]}

    for state in map_insu_list:
        cur_states = path3 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                D = json.load(data)
                
                for i in D ['data'] ['hoverDataList']:
                    name = i ["name"]
                    count = i ["metric"] [0] ["count"]
                    amount = i ["metric"] [0] ["amount"] 
                    col3 ["districts"].append (name)
                    col3 ["transaction_count"].append (count)
                    col3 ["amount"].append (amount)
                    col3 ["states"].append(state)
                    col3 ["year"].append(year)
                    col3 ["quarter"].append(int(file.strip(".json")))

    map_insu_list= pd.DataFrame(col3)

    map_insu_list["states"] = map_insu_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    map_insu_list["states"] = map_insu_list["states"].str.replace('-', ' ')
    map_insu_list["states"] = map_insu_list["states"].str.title()
    map_insu_list["states"] = map_insu_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(map_insu_list)

    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO map_insu_list(states , year , quarter , districts , transaction_count , amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data =map_insu_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()
    except Exception as err:
        print("fetch_and_insert_map_insurance => Error : ", err)

    
pass

# MAP TRANSACTION
def fetch_and_insert_map_transaction(file_path):
    path4 = file_path + "/map/transaction/hover/country/india/state/"
    map_tran_list = os.listdir(path4)

    col4 = {"states":[], "year":[], "quarter":[], "districts":[], "transaction_count":[], "amount":[]}

    for state in map_tran_list:
        cur_states = path4 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                E = json.load(data)
                
                for i in E ['data'] ['hoverDataList']:
                    name = i ["name"]
                    count = i ["metric"] [0] ["count"]
                    amount = i ["metric"] [0] ["amount"] 
                    col4 ["districts"].append (name)
                    col4 ["transaction_count"].append (count)
                    col4 ["amount"].append (amount)
                    col4 ["states"].append(state)
                    col4 ["year"].append(year)
                    col4 ["quarter"].append(int(file.strip(".json")))

    map_tran_list = pd.DataFrame(col4)


    map_tran_list["states"] = map_tran_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    map_tran_list["states"] = map_tran_list["states"].str.replace('-', ' ')
    map_tran_list["states"] = map_tran_list["states"].str.title()
    map_tran_list["states"] = map_tran_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(map_tran_list)
    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query ="""INSERT INTO map_tran_list(states , year , quarter , districts , transaction_count , amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = map_tran_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()

    except Exception as err:
        print("fetch_and_insert_map_transaction => Error : ", err)

    
pass



# MSP USER
def fetch_and_insert_map_user(file_path):
    path5 = file_path + "/map/user/hover/country/india/state/"
    map_user_list = os.listdir(path5)

    col5 = {"states":[], "year":[], "quarter":[], "districts":[], "registeredUsers":[], "appOpens":[]}

    for state in map_user_list:
        cur_states = path5 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                F = json.load(data)

                for i in F ["data"] ["hoverData"].items():
                    district = i [0]
                    registeredUsers = i [1] ["registeredUsers"]
                    appOpens = i [1] ["appOpens"]
                    col5 ["districts"].append (district)
                    col5 ["registeredUsers"].append (registeredUsers)
                    col5 ["appOpens"].append (appOpens)
                    col5 ["states"].append(state)
                    col5 ["year"].append(year)
                    col5 ["quarter"].append(int(file.strip(".json")))

    map_user_list = pd.DataFrame(col5)

    map_user_list["states"] = map_user_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    map_user_list["states"] = map_user_list["states"].str.replace('-', ' ')
    map_user_list["states"] = map_user_list["states"].str.title()
    map_user_list["states"] = map_user_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(map_user_list)

    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO map_user_list(states , year , quarter , districts , registeredUsers , appOpens) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = map_user_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()

    except Exception as err:
        print("fetch_and_insert_map_user => Error : ", err)

    
pass


# TOP INSURANCE
def fetch_and_insert_top_insurance(file_path):
    path6 = file_path + "/top/insurance/country/india/state/"
    top_insu_list = os.listdir(path6)

    col6 = {"states":[], "year":[], "quarter":[], "pincodes":[], "transaction_count":[], "transaction_amount":[]}

    for state in top_insu_list:
        cur_states = path6 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                G = json.load(data)

                for i in G ["data"] ["pincodes"]:
                    entityname = i ["entityName"]
                    count = i ["metric"] ["count"]
                    amount = i ["metric"] ["amount"]
                    col6 ["pincodes"].append (entityname)
                    col6 ["transaction_count"].append (count)
                    col6 ["transaction_amount"].append (amount)
                    col6 ["states"].append(state)
                    col6 ["year"].append(year)
                    col6 ["quarter"].append(int(file.strip(".json")))


    top_insu_list = pd.DataFrame(col6)

    top_insu_list= top_insu_list.ffill()


    top_insu_list["states"] = top_insu_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    top_insu_list["states"] = top_insu_list["states"].str.replace('-', ' ')
    top_insu_list["states"] = top_insu_list["states"].str.title()
    top_insu_list["states"] = top_insu_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(top_insu_list)

    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO top_insu_list(states, year, quarter, pincodes, transaction_count, transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = top_insu_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()
    except Exception as err:
        print("fetch_and_insert_top_insurance => Error : ", err)

    
pass



#TOP TRANSACTION
def fetch_and_insert_top_transaction(file_path):
    path7 = file_path + "/top/transaction/country/india/state/"
    top_tran_list = os.listdir(path7)

    col7 = {"states":[], "year":[], "quarter":[], "pincodes":[], "transaction_count":[], "transaction_amount":[]}

    for state in top_tran_list:
        cur_states = path7 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                H = json.load(data)

                for i in H ["data"] ["pincodes"]:
                    entityname = i ["entityName"]
                    count = i ["metric"] ["count"]
                    amount = i ["metric"] ["amount"]
                    col7 ["pincodes"].append (entityname)
                    col7 ["transaction_count"].append (count)
                    col7 ["transaction_amount"].append (amount)
                    col7 ["states"].append(state)
                    col7 ["year"].append(year)
                    col7 ["quarter"].append(int(file.strip(".json")))

    top_tran_list = pd.DataFrame(col7)

    top_tran_list["states"] = top_tran_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    top_tran_list["states"] = top_tran_list["states"].str.replace('-', ' ')
    top_tran_list["states"] = top_tran_list["states"].str.title()
    top_tran_list["states"] = top_tran_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(top_tran_list)

    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()

        query = """INSERT INTO top_tran_list(states, year, quarter, pincodes, transaction_count, transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)"""
        data = top_tran_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()
    except Exception as err:
        print("fetch_and_insert_top_transaction => Error : ", err)

    
pass




# TOP USER
def fetch_and_insert_top_user(file_path):
    path8 = file_path + "/top/user/country/india/state/"
    top_user_list = os.listdir(path8)

    col8 = {"states":[], "year":[], "quarter":[], "pincodes":[], "registeredUsers":[]}

    for state in top_user_list:
        cur_states = path8 + state + "/"           # gets state names
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year = cur_states + year + "/"
            agg_file_list = os.listdir (cur_year)
            
            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, "r")

                I = json.load(data)

                for i in I ["data"] ["pincodes"]:
                    name = i ["name"]
                    registeredUsers = i ["registeredUsers"] 

                    col8 ["pincodes"].append (name)
                    col8 ["registeredUsers"].append (registeredUsers)
                    col8 ["states"].append(state)
                    col8 ["year"].append(year)
                    col8 ["quarter"].append(int(file.strip(".json")))

    top_user_list = pd.DataFrame(col8)

    top_user_list["states"] = top_user_list["states"].str.replace ('andaman-&-nicobar-islands', 'Andaman & Nicobar') 
    top_user_list["states"] = top_user_list["states"].str.replace('-', ' ')
    top_user_list["states"] = top_user_list["states"].str.title()
    top_user_list["states"] = top_user_list["states"].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    print(top_user_list)

    
    # start insert Pulse data into DB
    try:
        client = getSqlClient_1()
        cursor = client.cursor()
                
        query = """INSERT INTO top_user_list(states, year, quarter, pincodes, registeredUsers) VALUES(%s,%s,%s,%s,%s)"""
        data = top_user_list.values.tolist()
        cursor.executemany(query,data)
        client.commit()
        client.close()

    except Exception as err:
        print("fetch_and_insert_top_user => Error : ", err)

    
pass
