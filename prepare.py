def clean_telco_data(df):
    import pandas as pd
    
    df = df.loc[:,~df.columns.duplicated()].copy()
    df['total_charges'] = (df.total_charges + '0').astype('float')
    df = df.drop(columns=['internet_service_type_id', 'contract_type_id', 'payment_type_id'])
    df['gender_encoded'] = df.gender.map({'Female': 1, 'Male': 0})
    df['partner_encoded'] = df.partner.map({'Yes': 1, 'No': 0})
    df['dependents_encoded'] = df.dependents.map({'Yes': 1, 'No': 0})
    df['phone_service_encoded'] = df.phone_service.map({'Yes': 1, 'No': 0})
    df['paperless_billing_encoded'] = df.paperless_billing.map({'Yes': 1, 'No': 0})
    df['churn_encoded'] = df.churn.map({'Yes': 1, 'No': 0})
    dummy_df = pd.get_dummies(df[['multiple_lines', \
                              'online_security', \
                              'online_backup', \
                              'device_protection', \
                              'tech_support', \
                              'streaming_tv', \
                              'streaming_movies', \
                              'contract_type', \
                              'internet_service_type', \
                              'payment_type'
                            ]],
                              drop_first=True)
    df = pd.concat( [df, dummy_df], axis=1 )
    
    return df

def split_telco_data(df, target='churn'):
    from sklearn.model_selection import train_test_split
    '''
    split_data will take in a single pandas dataframe
    it will split it into a train, validate, and test set
    and it will return three values:
    train, val, test (in this order) -- all pandas Dataframes
    '''
    train, test = train_test_split(df, 
                               train_size = 0.8,
                               random_state=1349,
                              stratify=df[target])
    train, val = train_test_split(train,
                             train_size = 0.8,
                             random_state=1349,
                             stratify=train[target])
    return train, val, test

def model_telco_data(df,target='churn_encoded'):
    columns_to_drop = ['customer_id','gender','partner','dependents','phone_service','paperless_billing','churn',\
              'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support',\
               'streaming_tv', 'streaming_movies', 'contract_type', 'internet_service_type', 'payment_type',\
                  'contract_type','churn_month','signup_date']
    columns_to_drop.append(target)
    
    X_df = df.drop(columns=columns_to_drop)
    y_df = df[target]

    return X_df, y_df

def eval_results(p, alpha, group1, group2):
    '''
    this function will take in the p-value, alpha, and a name for the 2 variables
    you are comparing (group1 and group2) and return a string stating 
    whether or not there exists a relationship between the 2 groups. 
    '''
    if p < alpha:
        return f'There exists some relationship between {group1} and {group2}. (p-value: {p:.4f})'
    else:
        return f'There is not a significant relationship between {group1} and {group2}. (p-value: {p:.4f})'