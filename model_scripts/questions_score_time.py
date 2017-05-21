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
    numrows = 1e6
    print("Connecting and getting ~{}".format(numrows))
    q = create_questions_df(numrows)
    print("Got rows, cleaning data")
    q_train_dc = DataCleaner(q, questions=True, training=True,
                             simple_regression=True, time_split=True,
                             normalize=False)
    X, y = q_train_dc.get_clean()

    default_models = [RandomForestRegressor, GradientBoostingRegressor]

    param_dict = {'rf': {'n_estimators': [50, 100, 5000], 'max_depth':
                  [2, 3, 5]},
                  'gbr': {'learning_rate': [.001, .01, .1, .2], 'max_depth':
                          [2, 3, 5], 'n_estimators': [50, 100, 5000]}}
    print('Finding optimal models')
    finder = FindOptimalModels(X, y, question=True, time_split=True)
    finder.baseline_model()
    fitted_models = finder.run_default_models(default_models)
    print("starting grid search")
    opt_params = finder.run_grid_search(fitted_models, param_dict)
    opt_results = finder.run_optimized_models()
