import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_diabetes
from sklearn.datasets import load_digits
from sklearn.datasets import load_iris
from sklearn.datasets import load_linnerud
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import make_regression

from xtoy.toys import Toy
from xtoy import Featurizer


def apply_toy_on(X, y, cl_or_reg=None):
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.DataFrame):
        y = pd.DataFrame(y)
    toy = Toy(cl_or_reg=cl_or_reg)
    toy.fit(X[0::2], y[0::2])
    return toy.score(X[1::2], y[1::2])


def test_date():
    X = [["2015-04"], ["2015-05"], ["2015-06"]] * 10
    y = [1, 1, 0] * 10
    assert apply_toy_on(X, y) > 0.5


def test_digits_data():
    X, y = load_digits(return_X_y=True)
    assert apply_toy_on(X, y) > 0.7


def test_iris_data():
    X, y = load_iris(return_X_y=True)
    assert apply_toy_on(X, y) > 0.1


def test_boston_data():
    X, y = load_boston(return_X_y=True)
    assert apply_toy_on(X, y)


def test_breast_cancer_data():
    X, y = load_breast_cancer(return_X_y=True)
    assert apply_toy_on(X, y) > 0.3


def test_diabetes_data():
    X, y = load_diabetes(return_X_y=True)
    assert apply_toy_on(X, y)


# problem with really small data, maybe multiply cases like that


def test_missing():
    X = np.array([1, 2, 3, 4, np.nan, 5, np.nan, np.nan, np.nan, np.nan] * 10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1] * 10)
    assert apply_toy_on(X, y) > 0.1


# has issue with O and float
def test_text_missing():
    X = np.array(["1", "2", "3", "4", None, None, "5", None, None, None, None] * 10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] * 10)
    assert apply_toy_on(X, y) > 0.1


def test_text_missing2():
    X = np.array(["1", "2", "3", "4", None, None, "5a", None, None, None, None] * 10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] * 10)
    assert apply_toy_on(X, y) > 0.1


# multi output regression
def test_linnerud_data():
    X, y = load_linnerud(return_X_y=True)
    assert apply_toy_on(X, y) > -3000


def test_date_missing_data():
    import os

    filename = None
    for fn in ["../data/nba_2016.csv", "data/nba_2016.csv"]:
        if os.path.exists(fn):
            filename = fn
    if filename is None:
        return
    data = pd.read_csv(filename)
    X, y = data.drop("PTS.1", axis=1), data["PTS.1"]
    assert apply_toy_on(X, y)


def test_make_reg():
    X, y = make_regression(1000)
    assert apply_toy_on(X, y)


def test_newsgroup_data():
    categories = ["alt.atheism", "talk.religion.misc", "comp.graphics", "sci.space"]

    newsgroups = fetch_20newsgroups(
        subset="train", remove=("headers", "footers", "quotes"), categories=categories
    )

    X, y = pd.DataFrame(newsgroups.data), newsgroups.target
    assert apply_toy_on(X, y, cl_or_reg="classification")
