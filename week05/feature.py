import pandas as pd

def clean_data(df):
    '''Cleans removes unnecessary columns, creates temperature column in °C, imputes missing values '''
    df = df.copy()
    # replace column names
    df.columns = ['SOUID', 'TG', 'Q_TG']
    # Get missing values
    missing_values = df[df['Q_TG'] == 9]
    # Get values for the missing data 1 year before and after
    missing_values_1y_bf = missing_values.index - pd.DateOffset(years=1)
    missing_values_1y_af = missing_values.index + pd.DateOffset(years=1)

    temp_replace = (df[missing_values_1y_bf.min():missing_values_1y_bf.max()].reset_index()['TG'] \
+ df[missing_values_1y_af.min():missing_values_1y_af.max()].reset_index()['TG'])/2
    temp_replace.index = missing_values.index
    df.loc[(df['Q_TG'] == 9), 'TG'] = temp_replace

    df['temp'] = df['TG'] / 10

    df = df.drop(['SOUID','Q_TG', 'TG'], axis=1)

    return df

def time_features(df):
    '''Adds time features to dataframe'''
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    
    return df

def season_feature(df):
    '''One-hot encoding of the month to account for seasonality'''
    season_dummies = pd.get_dummies(df.index.month, prefix='month', drop_first=True).set_index(df.index)
    return df.join(season_dummies)

def create_lag_features(df, n_lags, remainder_col = 'remainder'):
    '''Create lags in dataframe based remainder column'''
    data_frame = df.copy()
    for i in range(n_lags):
        data_frame['lag' + str(i+1)] = data_frame[remainder_col].shift(i+1)
    
    return data_frame.dropna()