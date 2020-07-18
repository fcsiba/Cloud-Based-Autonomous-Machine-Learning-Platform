# import libraries
import pandas as pd
from sklearn.model_selection import train_test_split

import sklearn.datasets
import sklearn.metrics

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB

from tpot import TPOTClassifier
from tpot import TPOTClassifier
import os


def tpot_run(df, target_col):
    target = df[target_col]
    df = df.drop(target_col, axis=1)
    data = df.to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        data, target, train_size=0.75, test_size=0.25)

    tpot = TPOTClassifier(generations=100,
                          population_size=100,
                          offspring_size=None,  # this gets set to population_size
                          mutation_rate=0.9,
                          crossover_rate=0.1,
                          # scoring= "Accuracy",  # for Classification
                          cv=5,
                          subsample=1.0,
                          n_jobs=1,
                          max_time_mins=20,
                          max_eval_time_mins=5,
                          random_state=None,
                          config_dict=None,
                          warm_start=False,
                          memory=None,
                          periodic_checkpoint_folder=None,
                          early_stop=None,
                          verbosity=2,
                          disable_update_check=False)

    tpot.fit(X_train, y_train)

    tpot.export(os.getcwd()+"\\FYP\\static\\files\\datasets\\pipeline.py")
    return "done"
