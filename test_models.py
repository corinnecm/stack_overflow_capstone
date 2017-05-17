import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner


class CompareModels(object):
    """

    """

    def __init__(self, test_models, X, y, train=True):
        self.test_models = test_models
        self.X = X
        self.y = y


def baseline_model(y_train):
    '''
    Predicts the score for a post, always predicts the average of the
    normalized scores.

    RETURNS:
        r-squared score and MSE for the baseline predictions.
    '''
    avg_normed_score = y_train.mean()
    # make y_prediction into generator to save compute time?
    y_prediction = [y_train.mean() for row in xrange(len(y_train))]
    print('R-squared for Baseline: ' + r2_score(y_train,
          y_prediction))
    print('MSE for Baseline: ' + mean_squared_error(y_train, y_prediction))


def run_all():
    '''
    Runs the whole shebang: creates dataframes, cleans data,
    compares models.
    '''
    pass


if __name__ == '__main__':
    run_all()
