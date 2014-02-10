#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import *
from maxent import me_classify
import math

class CDocument:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words


def productCombined(trains,tests,classifies):
    resultsList=[]
    for classify in classifies:
        resultsList.append(classify(trains,tests)[1])
    
    results=[]
    p=n=tp=tn=fp=fn=0
    for i in range(len(tests)):
        multPos=multNeg=1
        for j in range(len(resultsList)):
            posProb=resultsList[j][i]
            if posProb>0:
                negProb=1-posProb
            elif posProb<0:
                negProb=abs(posProb)
                posProb=1-negProb
            else:
                negProb=posProb=1
            multPos*=posProb
            multNeg*=negProb
        score=multPos-multNeg
        
        if tests[i].polarity==True:
            p+=1
            if score>0:
                tp+=1
            else:
                fn+=1
        else:
            n+=1
            if score<0:
                tn+=1
            else:
                fp+=1
        if score>0:
            results.append(multPos/(multPos+multNeg))
        else:
            results.append(-multNeg/(multPos+multNeg))
    acc=(tp+tn)/(p+n)
    precisionP=tp/(tp+fp)
    precisionN=tn/(tn+fn)
    recallP=tp/(tp+fn)
    recallN=tn/(tn+fp)
    gmean=math.sqrt(recallP*recallN)
    f_p=2*precisionP*recallP/(precisionP+recallP)
    f_n=2*precisionN*recallN/(precisionN+recallN)
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(gmean,recallP,recallN,precisionP,precisionN,f_p,f_n,acc)
    return gmean,results


def stackingCombined(trains,tests,classifies,fold=10):
    subLen=len(trains)//fold
    vectors=[]
    for i in range(fold):
        resultsList=[]
        subTrains=[]
        subTests=[]
        for j in range(fold):
            if j==i:
                subTests+=trains[j*subLen:(j+1)*subLen]
            else:
                subTrains+=trains[j*subLen:(j+1)*subLen]

        for classify in classifies:
            resultsList.append(classify(subTrains,subTests)[1])
        
        for i,subTest in enumerate(subTests):
            vector=CDocument(subTest.polarity,{})
            for j in range(len(resultsList)):
                posProb=resultsList[j][i]
                if posProb>0:
                    negProb=1-posProb
                elif posProb<0:
                    negProb=abs(posProb)
                    posProb=1-negProb
                else:
                    negProb=posProb=0
                vector.words[str(j*2)]=posProb
                vector.words[str(j*2+1)]=negProb
            vectors.append(vector)
    vTrains=vectors
    
    resultsList=[]
    for classify in classifies:
        resultsList.append(classify(trains,tests)[1])
    vTests=[]
    for i,test in enumerate(tests):
        vector=CDocument(test.polarity,{})
        for j in range(len(resultsList)):
            posProb=resultsList[j][i]
            if posProb>0:
                negProb=1-posProb
            elif posProb<0:
                negProb=abs(posProb)
                posProb=1-negProb
            else:
                negProb=posProb=0
            vector.words[str(j*2)]=posProb
            vector.words[str(j*2+1)]=negProb
        vTests.append(vector)
    acc,results=me_classify(vTrains,vTests)
    
    print 'combined results: %f' % acc
    return acc,results
