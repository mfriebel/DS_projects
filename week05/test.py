# Import
from feature import season_feature, create_lag_features

import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

# Test Model
test = pd.read_csv('data/test.csv', index_col=0, parse_dates=True)
test = season_feature(test)

m_season = pickle.load(open('data/seasonal_model.pickle', 'rb'))
test['seasonal_trend'] = m_season.predict(test.drop(['temp'], axis=1))
test['remainder'] = test['temp'] - test['seasonal_trend']
test = create_lag_features(test, 3)

m_full = pickle.load(open('data/full_model.pickle', 'rb'))
X_test = test.drop(['temp', 'seasonal_trend', 'remainder'], axis=1)
y_test = test['temp']
test['full_model'] = m_full.predict(X_test)
print(f'Test-Score: {round(m_full.score(X_test, y_test),3)}')

sns.lineplot(x=test.index, y='temp', data=test)
sns.lineplot(x=test.index, y='full_model', data=test)
plt.show()