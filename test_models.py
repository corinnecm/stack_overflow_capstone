import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner


class FindOptimalModels(object):
    """

    """

    def __init__(self, test_models, X, y, train=True):
        self.test_models = test_models
        self.X = X
        self.y = y


def run_all():
    '''
    Runs the whole shebang: creates dataframes, cleans data,
    compares models.
    '''
    pass


if __name__ == '__main__':
    run_all()
