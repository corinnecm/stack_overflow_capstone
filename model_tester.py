import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, f1_score

from question_query import create_questions_df
from answer_query import create_answers_df
from data_cleaning import DataCleaner


class FindOptimalModels(object):
    def __init__(self, X_test, X_train, y_test, y_train, question=True):
        self.X_test = X_test
        self.X_train = X_train
        self.y_test = y_test
        self.y_train = y_train
        self.question = question

    def run_default_models(self, default_models):
        '''
        For a list of regression models, fits, predicts and scores for
        comparison purposes. Default parameters only.

        PARAMETERS:
            model_list: list of models/estimators, i.e. [RandomForestRegressor,
            etc]

        RETURNS:
            R-sqared score and MSE for each model in models.
        '''
        fitted_models = []
        for idx, model in enumerate(default_models):
            mod = model()
            mod.fit(self.X_train, self.y_train)
            rf_pred = mod.predict(self.X_test)
            if self.question:
                print('Questions DF, model {} R-sq: {}'.format(idx,
                       mod.score(self.X_test, self.y_test)),
                      'Questions DF, model {} MSE: {}'.format(idx,
                       mean_squared_error(self.y_test, rf_pred)))
            else:
                print('Answers DF, model {} R-sq: {}'.format(idx,
                       mod.score(self.X_test, self.y_test)),
                      'AnswersDF, model {} MSE: {}'.format(idx,
                       mean_squared_error(self.y_test, rf_pred)))
            fitted_models.append(mod)
        return fitted_models

    def run_grid_search(self, model_list, params_dict):
        '''
        Runs grid search for fitted models in model list for comparison
        of optimal models.

        PARAMETERS:
            model_list: list of already fitted models, i.e. [rf, gbr, etc.]
            param_dict: dictionary of dicts of the parameters to optimize,
                        i.e. {'rf': {'n_estimators': [10, 20, 50, 100, 5000],
                        'max_depth': [2, 3, 5]}, 'gbr': etc.}, MUST BE IN THE
                        SAME ORDER AS MODEL LIST.

        RETURNS:
            Best parameters for each model.
        '''
        output_msg = []
        optimal_params = []
        params = params_dict.keys()
        for idx, model in enumerate(model_list):
            gs = GridSearchCV(model, params_dict[params[idx]], n_jobs=1, cv=3)
            gs.fit(self.X_train, self.y_train)
            output_msg.append('Best parameters for {} are {}'.format(params[idx],
                              gs.best_params_))
            optimal_params.append(gs.best_params_)
        print output_msg
        return optimal_params


def run_optimized_models(model_list, optimal_params, X_test, X_train, y_test, y_train):
    '''
    Takes output from run_grid_search() and runs the optimal version of each
    model.

    PARAMETERS:
        model_list:
        optimal_params: a list of dicts, each dict contains the optimal
            parameters for a certain model
    '''
    for idx, mod in enumerate(model_list):
        model = mod(opt_params[idx])
    pass


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


if __name__ == '__main__':
    q = create_questions_df()
    q_train_dc = DataCleaner(q)
    X, y = q_train_dc.get_clean()
    X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.8,
                                                        random_state=123)
    # a = create_answers_df()
    # a_train_dc = DataCleaner(a)
    # A, b = a_train_dc.get_clean()
    # A_test, A_train, b_test, b_train = train_test_split(A, b, test_size=0.8,
    # random_state=123)

    default_models = [RandomForestRegressor, GradientBoostingRegressor]

    param_dict = {'rf': {'n_estimators': [10, 20, 50, 100, 5000], 'max_depth':
                  [2, 3, 5], 'criterion': ['mse', 'mae']},
                  'gbr': {'learning_rate': [.001, .01, .1, .2], 'max_depth':
                          [2, 3, 5], 'n_estimators': [10, 20, 50, 100, 5000]}}

    finder = FindOptimalModels(X_test, X_train, y_test, y_train, question=True)
    fitted_models = finder.run_default_models(default_models)
    opt_params = finder.run_grid_search(fitted_models, param_dict)

    baseline_model(y_train, y_test)
