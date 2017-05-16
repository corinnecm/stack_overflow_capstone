import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner


class TestModels(object):

    def __init__(self):
        pass

    def baseline_model(self):
        '''
        Predicts the score for a post, always predicts the average of the
        normalized scores.
        '''
        avg_normed_score = X_test['normed_score'].mean
        y_prediction = [avg_normed_score for row in xrange(len(df))]
        return y_prediction, r2_score(X_test['normed_score'], y_prediction)

    def random_forest(self):
        pass

    def linear_regression(self):
        pass
