import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner

# %load_ext autoreload
# %autoreload 2

q = create_questions_df()
a = create_answers_df()

q_train_dc = DataCleaner(q)
q_test_dc = DataCleaner(q, training=False)

X_train, y_train = q_train_dc.get_clean()
X_test, y_test = q_test_dc.get_clean()


rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)
rf_pred = rfr.predict(X_test)
print('RF R-sq: ', rf.score(X_test, y_test))
print('RF MSE: ', mean_squared_error(y_test, rf_pred))


lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
print('LR R-sq: ', lr.score(X_test, y_test))
print('LR MSE: ', mean_squared_error(y_test, lr_pred))

gbr = GradientBoostingRegressor()
gbr.fit(X_train, y_train)
gbr_pred = gbr.predict(X_test)
print('GBR R-sq: ', gbr.score(X_test, y_test))
print('GBR MSE: ', mean_squared_error(y_test, gbr_pred))

baseline_model(y_train, y_test)

rfr_params = {'n_estimators': [10, 20, 50, 100, 5000], 'max_depth': [2, 3, 5]}
# gbr_params = {'loss': ['ls', 'lad', 'huber', 'quantile'],
            #   'learning_rate' = [.001, .01, .1, .2], 'max_depth': [2, 3, 5],
            #   'n_estimators': [10, 20, 50, 100, 5000]}

model_list = [RandomForestRegressor, LinearRegression, GradientBoostingRegressor]
# for model in model_list:

GridSearchCV(RandomForestRegressor, rfr_params, n_jobs=2, cv=5)


def baseline_model(y_train, y_test):
    '''
    Predicts the score for a post, always predicts the average of the
    normalized scores.

    RETURNS:
        R-squared score and MSE for the baseline predictions.
    '''
    avg_normed_score = y_train.mean()
    y_pred = [avg_normed_score for row in xrange(len(y_test))]
    print('Baseline R-squared: ', r2_score(y_test, y_pred))
    print('Baseline MSE: ', mean_squared_error(y_test, y_pred))
