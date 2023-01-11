import numpy as np
import seaborn as sns
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from pydataset import data
import env as env
import os

def get_telco_data():
    '''

    checks if 'telco.csv' exists
    if it does it will load file with Pandas

    otherwise, it will connect to SQL server
    using get_db_url('telco_churn') from env.py
    and read_sql() from Pandas

    returns a dataframe

    '''
    path = 'telco.csv'
    file_exists = os.path.exists(path)
    if file_exists:

        df = pd.read_csv(path)

        return df

    else:
        url = env.get_db_url('telco_churn')
        sql_query = '''
                        SELECT
                            *
                        FROM
                            customers AS c
                            LEFT JOIN internet_service_types AS ist USING (internet_service_type_id)
                            LEFT JOIN customer_subscriptions AS csb USING (customer_id)
                            LEFT JOIN payment_types AS pt USING (payment_type_id)
                            LEFT JOIN contract_types AS ct USING (contract_type_id)
                            LEFT JOIN customer_churn AS ccr USING (customer_id)
                            LEFT JOIN customer_contracts AS ccn USING (customer_id)
                            LEFT JOIN customer_details AS cd USING (customer_id)
                            LEFT JOIN customer_payments AS cp USING (customer_id)
                            LEFT JOIN customer_signups AS cs USING (customer_id);
                    '''
        df = pd.read_sql(sql_query, url)
        df.to_csv('telco_churn.csv')
        return df
