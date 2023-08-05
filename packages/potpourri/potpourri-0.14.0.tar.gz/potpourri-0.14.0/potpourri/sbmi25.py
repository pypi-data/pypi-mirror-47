
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', LogisticRegression(
        penalty = 'l2',
        solver = 'sag',  # large
        multi_class = 'ovr',  # binary
        random_state = 42,
        fit_intercept = True,
        max_iter = 100,
        warm_start = True,  # reuse previous solution
    ))
])

hyper = {
    'lin__C': ss.gamma(a=2.5, loc=1e-5, scale=0.75),
    # 'lin__fit_intercept': [True, False]
}

meta = {
    'id': "sbmi25",
    'name': 'Logistic Ridge',
    'descriptions': (
        "Logistic Regression, L2 penalty (Ridge), SAG solver, standard-normal "
        "transformed features."),
    'solver': 'Stochastic Average Gradient descent (SAG)',
    'active': True,
    'keywords': [
        'binary classification', 'linear regression', 'LogisticRegression'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
