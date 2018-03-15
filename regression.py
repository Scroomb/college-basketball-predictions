from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoCV, ElasticNetCV
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_optimal_alpha(mean_cv_errors_test):
    alphas = mean_cv_errors_test.index
    optimal_idx = np.argmin(mean_cv_errors_test.values)
    optimal_alpha = alphas[optimal_idx]
    return optimal_alpha

def train_at_various_alphas(X_trn, y_trn, model, alphas, n_folds=10, **kwargs):
    cv_errors_train = pd.DataFrame(np.empty(shape=(n_folds, len(alphas))),
                                     columns=alphas)
    cv_errors_test = pd.DataFrame(np.empty(shape=(n_folds, len(alphas))),
                                        columns=alphas)
    kf = KFold(n_splits=n_folds)
    for a in alphas:

        for idx, (train, test) in enumerate(kf.split(X_train)):

            # Split into train and test
            X_vals_train = X_trn[train]
            y_vals_train = y_trn[train]
            X_vals_test = X_trn[test]
            y_vals_test = y_trn[test]

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

def cv(X_trn, y_trn, base_estimator, n_folds=10):
    kf = KFold(n_splits=n_folds)
    test_cv_errors, train_cv_errors = np.empty(n_folds), np.empty(n_folds)

    for idx, (train, test) in enumerate(kf.split(X_train)):

        # Split into train and test
        X_vals_train = X_trn[train]
        y_vals_train = y_trn[train]
        X_vals_test = X_trn[test]
        y_vals_test = y_trn[test]

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

def make_coefficient_paths(alphas,models,Xtrain,ytrain,name):
    model_list = []
    for alpha in alphas:
        scaler = StandardScaler()
        scaler.fit(Xtrain)
        X_train_std = scaler.transform(Xtrain)

        scaler.fit(ytrain.values.reshape(-1,1))
        y_train_std = scaler.transform(ytrain.values.reshape(-1, 1)).flatten()
        model_nm = models(alpha=alpha)
        model_nm.fit(X_train_std, y_train_std)
        model_list.append(model_nm)

    paths = pd.DataFrame(np.empty(shape=(len(alphas), len(Xtrain.columns))),
                         index=alphas, columns=Xtrain.columns)

    for idx, model in enumerate(model_list):
        paths.iloc[idx] = model.coef_

    fig, ax = plt.subplots(figsize=(14, 4))
    for column in Xtrain.columns:
        path = paths.loc[:, column]
        ax.plot(np.log10(alphas), path, label=column)
    ax.legend(loc='lower right')
    ax.set_title(name + " Regression, Standardized Coefficient Paths")
    ax.set_xlabel(r"$\log(\alpha)$")
    ax.set_ylabel("Standardized Coefficient")
    plt.show()

if __name__ == '__main__':
    data = pd.read_csv('data/all_test_data.csv')
    data.drop(['Unnamed: 0'],axis=1,inplace=True)
    X_dat = data.drop(['PT_DIFF'],axis=1)
    #X_dat = data.loc[:,['PER_x','PER_y']]
    y_dat = data['PT_DIFF']
    X_train, X_test, y_train, y_test = train_test_split(X_dat, y_dat, test_size=0.2)

    # lin_pipeline = Pipeline([
    #     ('standardize',StandardScaler()),
    #     ('linregression',LinearRegression())
    # ])
    #
    # lin_pipeline.fit(X_train,y_train)
    # pred = lin_pipeline.predict(X_test)

    las_pipeline = Pipeline([
        ('standardize',StandardScaler()),
        ('lasregression',LassoCV())
    ])

    # las_pipeline.fit(X_train,y_train)
    # pred = lin_pipeline.predict(X_test)

    lasso_alphas = np.logspace(-3, 3, num=250)
    num_al = len(lasso_alphas)
    #
    # lasso_cv_errors_train, lasso_cv_errors_test = train_at_various_alphas(
    #     X_train.values, y_train.values, Lasso, lasso_alphas, max_iter=5000)
    #
    # lasso_mean_cv_errors_train = lasso_cv_errors_train.mean(axis=0)
    # lasso_mean_cv_errors_test = lasso_cv_errors_test.mean(axis=0)
    #
    # lasso_optimal_alpha = get_optimal_alpha(lasso_mean_cv_errors_test)
    #
    # fig, ax = plt.subplots(figsize=(14, 4))
    # ax.plot(np.log10(lasso_alphas), lasso_mean_cv_errors_train)
    # ax.plot(np.log10(lasso_alphas), lasso_mean_cv_errors_test)
    # ax.axvline(np.log10(lasso_optimal_alpha), color='grey')
    # ax.set_title("LASSO Regression Train and Test MSE")
    # ax.set_xlabel(r"$\log(\alpha)$")
    # ax.set_ylabel("MSE")
