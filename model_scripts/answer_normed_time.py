import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, f1_score

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner
from model_tester import FindOptimalModels


if __name__ == '__main__':
    a = create_answers_df(1000000)
    a_train_dc = DataCleaner(a, questions=False, training=True,
                             simple_regression=True, time_split=True,
                             normalize=True)
    A, b = a_train_dc.get_clean()

    default_models = [RandomForestRegressor, GradientBoostingRegressor]

    param_dict = {'rf': {'n_estimators': [50, 100, 5000], 'max_depth':
                  [2, 3, 5]},
                  'gbr': {'learning_rate': [.001, .01, .1, .2], 'max_depth':
                          [2, 3, 5], 'n_estimators': [50, 100, 5000]}}

    finder = FindOptimalModels(A, b, question=False, time_split=True)
    finder.baseline_model()
    fitted_models = finder.run_default_models(default_models)
    opt_params = finder.run_grid_search(fitted_models, param_dict)