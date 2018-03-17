import pandas as pd
import numpy as np
import datetime

import json
import collections

def iterate_samples():
    with open('sample.json') as json_data:
        d = json.load(json_data)
        for n, sample in enumerate(d["data"]):
            # process one image description
            # print x["labelAnnotations"]
            yield sample
            if (n+1) % 10 == 0:
                print 'Processed %d image samples' % (n+1)

def extract_match_features(sample):

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

    return collections.OrderedDict(feats)

def create_table():
    df = {}
    fields = None
    for sample in iterate_samples():
        features = extract_match_features(sample)
        if fields is None:
            fields = features.keys()
            df = {key: [] for key in fields}
        for key, value in features.iteritems():
            df[key].append(value)
    df = pd.DataFrame.from_records(df).ix[:, fields]
    return df

features_table = create_table()
features_table.to_csv("features_%s.csv" % datetime.datetime.now().strftime("%H.%M.%S").__str__())
# features_train = pd.read_csv("Data/features.csv", index_col=0)
# df = features_train.sample(frac = 1).reset_index(drop=True)
# df.to_csv("shuffled_%s.csv" % datetime.datetime.now().strftime("%H.%M.%S").__str__())


