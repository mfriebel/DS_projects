# Import
from feature import clean_data, time_features, season_feature, create_lag_features

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ar_model import AutoReg, ar_select_order

#Read Data
df = pd.read_csv("data/TG_STAID002759.txt", skiprows=19, index_col=1, parse_dates=True)

# Clean Data
df_clean = clean_data(df)

# Timesteps
df_clean['timestep'] = list(range(len(df_clean.index)))

# Train-test-split
train = df_clean.iloc[:-365]
test = df_clean.iloc[-365:]

# Seasonality
train = season_feature(train)

# Predict seasonal trend
X_season = train.drop(['temp'], axis=1)
y_season = train['temp']

m_season = LinearRegression()
m_season.fit(X_season,y_season)

train['seasonal_trend'] = m_season.predict(X_season)

# Calculate Remainder
train['remainder'] = train['temp'] - train['seasonal_trend']

# Add lag features
train = create_lag_features(train, 2)

# Full Model
X_full = train.drop(['temp', 'seasonal_trend', 'remainder'], axis=1)
y_full = train['temp']

m_full = LinearRegression()
m_full.fit(X_full, y_full)

train['full_model'] = m_full.predict(X_full)
print(f'Training-Score: {round(m_full.score(X_full, y_full),3)}')

sns.lineplot(x=train.loc['2000'].index, y='temp', data=train.loc['2000'])
sns.lineplot(x=train.loc['2000'].index, y='full_model', data=train.loc['2000'])
plt.show()

# Cross-Validation
time_series_split = TimeSeriesSplit(n_splits=5)
splits = time_series_split.split(X_full, y_full) 
cv = cross_val_score(estimator=m_full, X=X_full, y=y_full, cv=splits)
cv.mean()
print(f'CV-Score: {round(cv.mean(),3)}')

# Test Model
test = season_feature(test)
test['seasonal_trend'] = m_season.predict(test.drop(['temp'], axis=1))
test['remainder'] = test['temp'] - test['seasonal_trend']
test = create_lag_features(test, 2)
X_test = test.drop(['temp', 'seasonal_trend', 'remainder'], axis=1)
test['full_model'] = m_full.predict(X_test)
y_test = test['temp']
print(f'Test-Score: {round(m_full.score(X_test, y_test),3)}')

sns.lineplot(x=test.index, y='temp', data=test)
sns.lineplot(x=test.index, y='full_model', data=test)
plt.show()