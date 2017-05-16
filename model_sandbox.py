import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner

# %load_ext autoreload
# %autoreload 2

questions = create_questions_df()

dc = DataCleaner(questions)

X, y = dc.get_clean()

# create cross-validation subsets
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8,
                                                    random_state=123)

X_train_reg = X_train[['answer_count', 'comment_count', 'favorite_count',
                       'bounty_amount', 'code_yn', 'title_length',
                       'body_length']]

rfr = RandomForestRegressor()

rfr.fit(X_train_reg, y_train)
rfr.predict(X_train_reg)
rfr.score(X_train_reg, y_train)
rfr.feature_importances_

lr = LinearRegression()

lr.fit(X_train_reg, y_train)
lr.predict(X_train_reg)
lr.score(X_train_reg, y_train)


def baseline_model(X_train):
    '''
    Predicts the score for a post, always predicts the average of the
    normalized scores.

    RETURNS:
        r-squared score for the baseline predictions.
    '''
    avg_normed_score = X_train['normed_score'].mean
    y_prediction = [avg_normed_score for row in xrange(len(X_train))]
    return r2_score(X_train['normed_score'], y_prediction)


# Test RF with defaults for un-cleaned data with 1000 rows, no added features:
# In [13]: rfr.score(X_test[['answer_count', 'comment_count', 'favorite_count',
# 'view_count']], X_test['score'])
# Out[13]: 0.58460069056804376

# RF with defaults for cleaned data with 1000 rows, features: answer_count,
# comment_count, favorite_count, bounty_amount, code_yn, title_length,
# body_length
# In [58]: rfr.score(X_train_reg, y_train)
# Out[58]: 0.772954675196411
# In [59]: rfr.feature_importances_
# Out[59]:
# array([  7.02753142e-02,   1.21382436e-01,   6.86715724e-02,
#          3.84836585e-06,   6.94508367e-02,   2.81402918e-01,
#          3.88813075e-01])

# To check for NaN/Null:
# pd.isnull(df).sum() > 0
# df.loc[:, df.isnull().any()]
