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

dc_train = DataCleaner(questions)
dc_test = DataCleaner(question, training=False)

X_train, y_train = dc_train.get_clean()
X_test, y_test = dc_test.get_clean()


rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)
rf_pred = rfr.predict(X_train)
print('RF R-sq: ' + rf.score(X_test, y_test))
print('RF MSE: ' + mean_squared_error(y_test, rf_pred))


lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_train)
print('LR R-sq: ' + lr.score(X_test, y_test))
print('LR MSE: ' + mean_squared_error(y_test, lr_pred))

baseline_model(y_train)


def baseline_model(y_train):
    '''
    Predicts the score for a post, always predicts the average of the
    normalized scores.

    RETURNS:
        r-squared score for the baseline predictions.
    '''
    avg_normed_score = y_train.mean()
    y_pred = [avg_normed_score for row in xrange(len(y_train))]
    print('R-squared: ' + r2_score(y_train, y_pred))
    print('MSE: ' + mean_squared_error(y_train, y_pred))
