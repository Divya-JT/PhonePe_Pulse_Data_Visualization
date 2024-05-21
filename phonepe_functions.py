import pandas as pd 
from phonepe_pulse_data_insertion import *



def get_dataframe_from_db(query):
    client = getSqlClient_1()
    cursor = client.cursor()

    df_1 = pd.read_sql(query, client)
    client.close()
    return df_1


