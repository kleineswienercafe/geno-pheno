from sklearn.linear_model import LogisticRegression
import statsmodels.discrete.discrete_model as dm
import statsmodels.api as st
from lib.gploader import GpExperimentSheet
from lib.gputils import GpConfig
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn import metrics
import pandas as pd 
import numpy as np 

def logit(gpd, analysis = False, onehot = False, ncat = 2):

    data = gpd.pdata(categoryNames="group").dropna()
    X = data[gpd.header()]
    X = X[~data['category'].str.contains("B/My")] #exclude B/My for now

    if onehot:
        dummy = pd.DataFrame(np.outer(np.linspace(0, ncat-1, ncat,dtype = np.int64),np.ones((X.shape[1],),dtype = np.int64)))
        dummy.columns = X.columns
        X = pd.concat([X,dummy],axis = 0)
        X = X.astype(int).astype('category')
        X = pd.get_dummies(X)#,prefix = X.columns)
        X = X[:-ncat] # remove dummy rows
        X.columns = [each[:-2] for each in X.columns] # remove indexes from names
    
    y = data['category']
    y = y[~y.str.contains("B/My")] #exclude B/My for now
    clf = LogisticRegression(random_state=0, solver='saga', max_iter = 50000, penalty = 'l1', multi_class='multinomial').fit(X, y)
    coeff_df = pd.DataFrame(clf.coef_, columns = X.columns, index = clf.classes_)
    
    scores = 0
    if analysis:
        scores = cross_val_score(clf, X, y, cv=ShuffleSplit(n_splits=15, test_size=0.2, random_state=0))

    return [coeff_df, scores]