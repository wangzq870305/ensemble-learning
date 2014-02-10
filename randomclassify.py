#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import random
from document import *
from combined import *
from maxent import me_classify

class CDocument:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words


def classify_feature(trains,tests,features,classify=me_classify):
    trains_feature=[]
    for document in trains:
        trains_feature.append(CDocument(document.polarity,dict([(word,document.words[word])for word in document.words if word in features])))
    
    tests_feature=[]
    for document in tests:
        tests_feature.append(CDocument(document.polarity,dict([(word,document.words[word])for word in document.words if word in features])))
    
    return classify(trains_feature,tests_feature)


def randomClassify(trains,tests,combind=productCombined):
    features=[]
    for document in trains:
        features+=document.words.keys()
    features=set(features)  
    features0=[];features1=[]
    
    for feature in features:
        if random.random()<0.5:
            features0.append(feature)
        else:
            features1.append(feature)
    features0=set(features0)
    features1=set(features1)
    
    return combind(trains,tests,[lambda trains,tests:classify_feature(trains,tests,features0),lambda trains,tests:classify_feature(trains,tests,features1)])