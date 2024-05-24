import pandas as pd 
from phonepe_pulse_data_insertion import *



def get_dataframe_from_db(query, column = None):
    client = getSqlClient_1()
    cursor = client.cursor()

    if(column):
        cursor.execute(query)
        df_1 = pd.DataFrame(cursor.fetchall(),columns=column)
    else:
        df_1 = pd.read_sql(query, client)
    client.close()
    return df_1


def search_tranaction_state(Year, Quarter):
    querry = f"""select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_tran_list where year = {Year} and quarter = {Quarter} group 
                    by states order by Total desc limit 10"""
    
    df = get_dataframe_from_db(query=querry,column=['States', 'Transactions_Count','Total_Amount'])
    return df

    
def search_tranaction_state1(Year, Quarter):
    querry = f"""select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_tran_list where year = {Year} and quarter = {Quarter} group 
                    by states order by Total_Transactions_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry,column=['States', 'Transactions_Count','Total_Amount'])
    return df
    

def search_tranaction_district(Year, Quarter):
    querry = f"""select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_tran_list where year = {Year} and quarter = {Quarter} group 
                    by districts order by Total desc limit 10"""
    df = get_dataframe_from_db(query=querry,column=['Districts', 'Transactions_Count','Total_Amount'])
    return df

def search_tranaction_pincode(Year, Quarter):
    querry = f"""select pincodes, sum(transaction_count) as Total_Transactions_Count, 
                    sum(transaction_amount) as Total from top_tran_list where year = {Year} 
                    and quarter = {Quarter} group by pincodes order by Total desc limit 10"""
    df = get_dataframe_from_db(query=querry,column=['Pincodes', 'Transactions_Count','Total_Amount'])
    return df


def search_tranaction_district1(Year, Quarter):
    querry = f"""select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_tran_list where year = {Year} and quarter = {Quarter} group 
                    by districts order by Total_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry,column=['Districts', 'Transactions_Count','Total_Amount'])
    return df

def search_tranaction_pincode1(Year, Quarter):
    querry = f"""select pincodes, sum(Transaction_count) as Total_Transactions_Count, 
                    sum(Transaction_amount) as Total from top_tran_list where year = {Year} 
                    and quarter = {Quarter} group by pincodes order by Total_Transactions_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry,column=['Pincodes', 'Transactions_Count','Total_Amount'])
    return df


## Insurance
def search_insurance_state(Year, Quarter):
    querry = f"""select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_insu_list where year = {Year} and quarter = {Quarter} group 
                    by states order by Total desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['States', 'Transactions_Count','Total_Amount'])
    return df
    
def search_insurance_district(Year, Quarter):
    querry = f"""select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_insu_list where year = {Year} and quarter = {Quarter} group 
                    by districts order by Total desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['District', 'Transactions_Count','Total_Amount'])
    return df

def search_insurance_pincode(Year, Quarter):
    querry = f"""select pincodes, sum(transaction_count) as Total_Transactions_Count, 
                    sum(transaction_amount) as Total from top_insu_list where year = {Year} 
                    and quarter = {Quarter} group by pincodes order by Total desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['Pincode', 'Transactions_Count','Total_Amount'])
    return df

def search_insurance_state1(Year, Quarter):
    querry = f"""select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) 
                    as Total from  agg_insu_list where year = {Year} and quarter = {Quarter} group 
                    by states order by Total_Transactions_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['State', 'Transactions_Count','Total_Amount'])
    return df

def search_insurance_district1(Year, Quarter):
    querry = f"""select districts , sum(transaction_count) as Total_Count, sum(amount) as Total 
                    from map_insu_list where year = {Year} and quarter = {Quarter} group 
                    by districts order by Total_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['District', 'Transactions_Count','Total_Amount'])
    return df

def search_insurance_pincode1(Year, Quarter):
    querry = f"""select pincodes, sum(transaction_count) as Total_Transactions_Count, 
                    sum(transaction_amount) as Total from top_insu_list where year = {Year} 
                    and quarter = {Quarter} group by pincodes order by Total_Transactions_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['Pincode', 'Transactions_Count','Total_Amount'])
    return df


## User transaction

def user_brand(Year, Quarter):
    querry = f"""select brands, sum(transaction_count) as Total_Count, avg(percentage)*100 as 
                    Avg_Percentage from agg_user_list where year = {Year} and quarter = {Quarter} 
                    group by brands order by Total_Count desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['Brand', 'Total_Users','Avg_Percentage'])
    return df
    

def user_district(Year, Quarter):
    querry = f"""select districts, sum(registeredUsers) as Total_Users, sum(appOpens) 
                    as Total_Appopens from map_user_list where year = {Year} and quarter = {Quarter} 
                    group by districts order by Total_Users desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['District', 'Total_Users','Total_Appopens'])
    return df

def user_pincode(Year, Quarter):
    querry = f"""select pincodes, sum(registeredUsers) as Total_Users from 
                    top_user_list where year = {Year} and quarter = {Quarter} group 
                    by pincodes order by Total_Users desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['Pincode', 'Total_Users'])
    return df
    
def user_state(Year, Quarter):
    querry = f"""select states, sum(registeredUsers) as Total_Users, sum(appOpens) 
                    as Total_Appopens from map_user_list where year = {Year} and quarter = {Quarter} 
                    group by states order by Total_Users desc limit 10"""
    df = get_dataframe_from_db(query=querry, column=['State', 'Total_Users','Total_Appopens'])
    return df

