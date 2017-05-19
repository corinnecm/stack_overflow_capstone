import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, f1_score

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner


if __name__ == '__main__':
    q = create_questions_df(1000000)
    q_train_dc = DataCleaner(q)
    X, y = q_train_dc.get_clean()

    default_models = [RandomForestRegressor, GradientBoostingRegressor]

    param_dict = {'rf': {'n_estimators': [50, 100, 5000], 'max_depth':
                  [2, 3, 5]},
                  'gbr': {'learning_rate': [.001, .01, .1, .2], 'max_depth':
                          [2, 3, 5], 'n_estimators': [50, 100, 5000]}}

    finder = FindOptimalModels(X, y, question=True, time_split=True)
    finder.baseline_model()
    fitted_models = finder.run_default_models(default_models)
    opt_params = finder.run_grid_search(fitted_models, param_dict)
