# Import
from feature import clean_data, time_features, season_feature, create_lag_features

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from statsmodels.tsa.arima.model import ARIMA
import pickle

import warnings
warnings.filterwarnings("ignore") # specify to ignore warning messages

#Read Data
df = pd.read_csv("data/TG_STAID002759.txt", skiprows=19, index_col=1, parse_dates=True)

# Clean Data
df_clean = clean_data(df)

# Timesteps
df_clean['timestep'] = list(range(len(df_clean.index)))

# Train-test-split
train = df_clean.iloc[:-365]
test = df_clean.iloc[-365:]
test.to_csv('test.csv')

'''Remove Seasonality'''
# Seasonality
train = season_feature(train)

# Predict seasonal trend
X_season = train.drop(['temp'], axis=1)
y_season = train['temp']

m_season = LinearRegression()
m_season.fit(X_season,y_season)

train['seasonal_trend'] = m_season.predict(X_season)


'''Add Lags from remainder'''
# Calculate Remainder
remainder = train['temp'] - train['seasonal_trend']
train['remainder'] = remainder

'''Plot remainder'''

plot_pacf(train['remainder'])
plt.show()
plot_acf(train['remainder'])
plt.show()

# Add lag features
train = create_lag_features(train, 3)


'''Manual AR'''

X_full = train.drop(['temp', 'seasonal_trend', 'remainder'], axis=1)
y_full = train['temp']

m_full = LinearRegression()
m_full.fit(X_full, y_full)

train['full_model'] = m_full.predict(X_full)
print(f'Training-Score (Manual AR): {round(m_full.score(X_full, y_full),3)}')


'''Cross-Validation'''

time_series_split = TimeSeriesSplit(n_splits=5)
splits = time_series_split.split(X_full, y_full) 
cv_manual_ar = cross_val_score(estimator=m_full, X=X_full, y=y_full, cv=splits)
print(f'CV-Score (Manual AR): {round(cv_manual_ar.mean(),3)}')


'''AutoRegressive Model - Statsmodels (on data taking into account trend and seasonality)'''

ar_model = AutoReg(y_season, lags=3, exog=X_season).fit()
#print(ar_model.summary())
prediction_ar = ar_model.predict()

'''ARIMA Model - Statsmodels (on data taking into account trend and seasonality) - very slow!!''' 

#arima_model = ARIMA(y_season, order=(1,0,1), exog=X_season).fit()
#print(arima_model.summary())
#prediction_arima = arima_model.predict()

'''ARIMA Model - only on remainder '''

arima_model = ARIMA(remainder, order=(2,0,2), freq='D').fit()
prediction_arima = arima_model.predict()
prediction_arima.name = 'Arima_lags'

# Use prediction of ARIMA Model as feature(includes lags2 , MA 2) for LinearRegression 
X_arima = X_season.join(prediction_arima)
m_arima = LinearRegression()
m_arima.fit(X_arima, y_season)
outcome_arima = pd.Series(m_arima.predict(X_arima), index=y_season.index)


'''Plot data as residuals '''
#sns.lineplot(x=train.loc['2000'].index, y='temp', data=train.loc['2000'], label = 'true values')
#sns.lineplot(x=train.loc['2000'].index, y='full_model', data=train.loc['2000'], label = 'Manual AR')
sns.lineplot(x=train.loc['2000'].index, y=(train['temp'].loc['2000'] - train['full_model'].loc['2000']), label = 'Residuals Manual AR')
plt.show()

#sns.lineplot(x=train.loc['2000'].index, y='temp', data=train.loc['2000'], label = 'true values')
#sns.lineplot(x=train.loc['2000'].index, y=prediction_ar.loc['2000'], label ='AR')
sns.lineplot(x=train.loc['2000'].index, y=(train['temp'].loc['2000'] - prediction_ar.loc['2000'].loc['2000']), label = 'Residuals AutoReg')
plt.show()

#sns.lineplot(x=train.loc['2000'].index, y='temp', data=train.loc['2000'], label = 'true values')
#sns.lineplot(x=train.loc['2000'].index, y=outcome_arima.loc['2000'], label ='ARIMA')
sns.lineplot(x=train.loc['2000'].index, y=(train['temp'].loc['2000'] - outcome_arima.loc['2000']), label = 'Residuals ARIMA')
plt.show()



'''Save Manual AR Model for testing'''
pickle.dump(m_season, open('seasonal_model.pickle', 'wb'))
pickle.dump(m_full, open('full_model.pickle', 'wb'))