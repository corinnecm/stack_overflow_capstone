from sklearn.metrics import r2_score


def baseline(X_test):
    '''
    Predicts the score for a post, always predicts the average of the normalized scores.
    '''
    avg_normed_score = X_test['normed_score'].mean
    y_prediction = [avg_normed_score for row in xrange(len(df))]
    return y_prediction, r2_score(X_test['normed_score'], y_prediction)
