#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import createDomain
from randomclassify import randomClassify

domain=createDomain('kitchen')
trains=domain[0][200:]+domain[1][200:]
tests=domain[0][:200]+domain[1][:200]
randomClassify(trains,tests)
