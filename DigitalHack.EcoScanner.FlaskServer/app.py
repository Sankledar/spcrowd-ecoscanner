from flask import Flask
from flask import request
from flask import jsonify

import sys
sys.path.append('../DigitalHack.EcoScanner.VisionApiClient')

import api_client.methods as visionAPI

import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from scipy.sparse import coo_matrix, hstack
import json
import collections

#settings.py
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'Data')
APP_ULOAD = os.path.join(APP_ROOT, '_upload')

app = Flask(__name__)



textColumns = ['labelAnnotations','webDetection','logoAnnotations','textAnnotations','bestGuessLabels']

_vectorizers = []
for name in textColumns:
    _vectorizers += [(name,TfidfVectorizer())]

def get_feature_Tfidf(X, column, isTrain):
    vectorizer = np.nan
    for key, value in _vectorizers.__iter__():
        if key == column:
            vectorizer = value

            break
    X_pick = X[column]
    if (isTrain):
        X_pick = vectorizer.fit_transform(X_pick)
    else:
        X_pick = vectorizer.transform(X_pick)
    return X_pick


def getSparceX(X, isTrain):
    X_terms = X[['logo', 'text']]
    for name in textColumns:
        X_text = get_feature_Tfidf(X, name, isTrain)
        X_terms = hstack([coo_matrix(X_text),X_terms])
    return X_terms



def fincC_LogisticRegression(X, Y):
    for x in np.arange(-5,5):
        c = np.power(10.0,x)
        lr_cls = LogisticRegression(penalty='l2', C=c)
        kf = KFold(n_splits=5,shuffle=True,random_state=241)
        cvs = cross_val_score(lr_cls, X, Y, cv=kf, scoring="roc_auc")
        print ("roc_auc_score for Logistic Regression=%s and c=%f" % (format(cvs.mean(), ".5f") ,c))


# def logistic_Regression(X, Y):
#     lr_cls = LogisticRegression(penalty='l2', C=0.00001) #better quality for this C parameter.
#     start_time = datetime.datetime.now()
#     lr_cls.fit(X, Y)
#     print 'Time elapsed:', datetime.datetime.now() - start_time
#     kf = KFold(n_splits=5,shuffle=True,random_state=241)
#     cvs = cross_val_score(lr_cls, X, Y, cv=kf, scoring="roc_auc")
#     print "roc_auc_score for Logistic Regression=%s" % format(cvs.mean(), ".2f")
#
# def gradient_Boosting(X, Y, n_estimators):
#     start_time = datetime.datetime.now()
#     gb_cls = GradientBoostingClassifier(n_estimators=n_estimators, random_state=241, verbose=True) #max_depth=1
#     gb_cls.fit(X, Y)
#     print 'Time elapsed:', datetime.datetime.now() - start_time
#     kf = KFold(n_splits=5,shuffle=True,random_state=241)
#     cvs = cross_val_score(gb_cls, X, Y, cv=kf, scoring="roc_auc")
#     print "roc_auc_score for Gradient Boosting=%s and n_estimators=%d" % (format(cvs.mean(), ".2f"),n_estimators)

def extract_match_features(sample):
    print (sample)
    feats = [
        ('logo', 1 if 'logoAnnotations' in sample else 0),
        ('text', 1 if 'textAnnotations' in sample else 0)
    ]

    labels = np.array([])
    if ('labelAnnotations' in sample ):
        for label in sample["labelAnnotations"]:
            labels = np.append(labels,label["description"])
        feats += [('labelAnnotations', np.array_str(labels))]
    else:
        feats += [('labelAnnotations', np.nan)]

    if ('logoAnnotations' in sample ):
        logos = np.array([])
        for text in sample["logoAnnotations"]:
            words = np.append(logos,text["description"])
        feats += [('logoAnnotations', np.array_str(words))]
    else:
        feats += [('logoAnnotations', np.nan)]

    if 'textAnnotations' in sample:
        words = np.array([])
        for text in sample["textAnnotations"]:
            words = np.append(words,text["description"])
        feats += [('textAnnotations', np.array_str(words))]
    else:
        feats += [('textAnnotations', np.nan)]

    if ('webDetection' in sample):
         entities = np.array([])
         if ('webEntities' in sample['webDetection']):
             for x in sample['webDetection']['webEntities']:
                 entities = np.append(entities,x["description"])
             feats += [('webDetection', np.array_str(entities))]
         else:
             feats += [('webDetection', np.nan)]

         labels = np.array([])
         for label in sample['webDetection']['bestGuessLabels']:
             if 'label' not in label:
                 continue
             labels = np.append(labels,label["label"])

         feats += [('bestGuessLabels', np.array_str(labels))]
    else:
        feats += [('webDetection', np.nan)]
        feats += [('bestGuessLabels', np.nan)]
    print (feats)
    return collections.OrderedDict(feats)

features_train = pd.read_csv(os.path.join(APP_STATIC, "features.csv"), index_col=0)
X_train = features_train.iloc[:,:-1].fillna('nan')
Y_train = features_train["isRecycable"]

X_terms = getSparceX(X_train,True)
# fincC_LogisticRegression(X_terms, Y_train)
# logistic_Regression(X_terms, Y_train)
# gradient_Boosting(X_terms,Y_train,90)
perc = Perceptron(random_state=241)
start_time = datetime.datetime.now()
perc.fit(X_terms,Y_train)
print ('Time elapsed:', datetime.datetime.now() - start_time)

kf = KFold(n_splits=5,shuffle=True,random_state=241)
cvs = cross_val_score(perc, X_terms, Y_train, cv=kf, scoring="roc_auc")
print ("roc_auc_score for Perceptron=%s" % format(cvs.mean(), ".2f"))

@app.route('/predict', methods = ['POST'])

def postJsonHandler():
    print (request.is_json)
    d = request.get_json()

    return predict(d)

def predict(d):
    print (d)
    df = {}
    fields = None

    for i, sample in enumerate(d["data"]):
        print (sample)
        features = extract_match_features(sample)
        if fields is None:
            fields = features.keys()
            df = {key: [] for key in fields}
        for key, value in features.items():
            df[key].append(value)
    X_test = pd.DataFrame.from_records(df).ix[:, fields]

    X_test = X_test.fillna('nan')
    X_test_transformed = getSparceX(X_test,False)
    predict = perc.predict(X_test_transformed)
    predict_proba = perc._predict_proba_lr(X_test_transformed)
    print( predict)
    print (predict_proba)

    data = {}
    data['predict'] = np.array_str(predict)
    data['predict_proba'] = np.array_str(predict_proba[:,1])
    json_data = json.dumps(data)

    return jsonify(data)

# from flask import flash
# from flask import redirect

@app.route('/upload', methods = ['POST'])
def uploadImage():
    try:
        print(request)
        print(request.files)
        print(request.files['image'])
        if 'image' not in request.files:
            pass
            #flash('No file part')
            # return redirect(request.url)
        ff = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if ff.filename == '':
            pass
            # flash('No selected file')
            # return redirect(request.url)
        if ff:
            filename = ff.filename
            saveFilePath = os.path.join(APP_ULOAD, filename)
            ff.save(saveFilePath)
            ff.close()
            print( saveFilePath )
            visionResponse = visionAPI.annotate_image_for_prediction(saveFilePath)
            os.remove(saveFilePath)
            return predict(visionResponse)
        return ff.filename
    except Exception as e:
        print(e)
        return e
    

@app.route('/ping', methods = ['GET'])
def main():
    return "pong!"

if __name__ == "__main__":
   print("== Running in debug mode ==")
   app.run(host='0.0.0.0', port=8080, debug=True)
