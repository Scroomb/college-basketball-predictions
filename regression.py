from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

def train_at_various_alphas(X_train, y_train, model, alphas, n_folds=10, **kwargs):
    cv_errors_train = pd.DataFrame(np.empty(shape=(n_folds, len(alphas))),
                                     columns=alphas)
    cv_errors_test = pd.DataFrame(np.empty(shape=(n_folds, len(alphas))),
                                        columns=alphas)
    kf = KFold(n_splits=n_folds)
    for a in alphas:

        for idx, (train, test) in enumerate(kf.split(X_train)):

            # Split into train and test
            X_vals_train = X_train[train]
            y_vals_train = y_train[train]
            X_vals_test = X_train[test]
            y_vals_test = y_train[test]

            # Standardize data, fit on training set,
            #transform training and test.
            scaler = StandardScaler()
            scaler.fit(X_vals_train)
            scaler.transform(X_vals_train)

            scaler.fit(y_vals_train.reshape(-1,1))
            scaler.transform(y_vals_train.reshape(-1, 1)).flatten()

            # Fit ridge regression to training data.

            clf = model(alpha=a)
            clf.fit(X_vals_train, y_vals_train)

            # Make predictions.
            pred_train = clf.predict(X_vals_train)
            pred_test = clf.predict(X_vals_test)
            # Calclate MSE.
            mse_train = mean_squared_error(y_vals_train, pred_train)
            mse_test = mean_squared_error(y_vals_test, pred_test)
            # Record the MSE in a numpy array.
            cv_errors_train[a].loc[idx], cv_errors_test[a].loc[idx] = mse_train, mse_test

    return cv_errors_train, cv_errors_test

def cv(X_train, y_train, base_estimator, n_folds=10):
    kf = KFold(n_splits=n_folds)
    test_cv_errors, train_cv_errors = np.empty(n_folds), np.empty(n_folds)

    for idx, (train, test) in enumerate(kf.split(X_train)):

        # Split into train and test
        X_vals_train = X_train[train]
        y_vals_train = y_train[train]
        X_vals_test = X_train[test]
        y_vals_test = y_train[test]

        # Standardize data, fit on training set,
        #transform training and test.
        scaler = StandardScaler()
        scaler.fit(X_vals_train)
        scaler.transform(X_vals_train)

        scaler.fit(y_vals_train.reshape(-1,1))
        scaler.transform(y_vals_train.reshape(-1, 1)).flatten()

        # Fit ridge regression to training data.
        clf = base_estimator(alpha=.5)
        clf.fit(X_vals_train, y_vals_train)

        # Make predictions.
        pred_train = clf.predict(X_vals_train)
        pred_test = clf.predict(X_vals_test)
        # Calclate MSE.
        mse_train = mean_squared_error(y_vals_train, pred_train)
        mse_test = mean_squared_error(y_vals_test, pred_test)
        # Record the MSE in a numpy array.
        train_cv_errors[idx], test_cv_errors[idx] = mse_train, mse_test

    return (train_cv_errors, test_cv_errors)

if __name__ == '__main__':
    test_data = pd.read_csv('data/2006-2007_all_data.csv')
    X_dat = test_data.drop(['PT_DIFF'],axis=1)
    y_dat = test_data['PT_DIFF']
    X_train, X_test, y_train, y_test = train_test_split(X_dat, y_dat, test_size=0.2)
    #
    # lin_pipeline = Pipeline([
    #     ('standardize',StandardScaler()),
    #     ('linregression',LinearRegression())
    # ])
    #
    # lin_pipeline.fit(X_train,y_train)
    # pred = lin_pipeline.predict(X_test)
