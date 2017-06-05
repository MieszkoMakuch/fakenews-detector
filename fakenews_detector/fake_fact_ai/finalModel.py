"""
    function:
    final model
    """

import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

import fakenews_detector.fake_fact_ai.RandomForest as rf  # bag learner
import fakenews_detector.fake_fact_ai.RandomTree as rt
import fakenews_detector.fake_fact_ai.feature as feature


class model(object):
    def __init__(self, fakeFile='./fake.txt', realFile='./real.txt', leafsize=5, bag=10):
        real = feature.constructMat(realFile, 1)
        fake = feature.constructMat(fakeFile, 0)
        data = np.append(real, fake, axis=0)
        X = data[:, 0:-1]
        Y = data[:, -1]
        # rand forest
        self.RF = rf.RandomForest(learner=rt.RandomTree, kwargs={"leaf_size": leafsize}, bags=bag, boost=False,
                                  verbose=False)
        self.RF.addEvidence(X, Y)
        # rand forest sklearn
        self.RFSklearn = RandomForestClassifier(n_estimators=bag)
        self.RFSklearn.fit(X, Y)
        # decision tree
        self.DT = tree.DecisionTreeClassifier()
        self.DT.fit(X, Y)
        # SVM
        self.SVM = SVC()
        self.SVM.fit(X, Y)
        # neural net
        self.MLP = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100,), random_state=1)
        self.MLP.fit(X, Y)

    def query(self, headline):
        '''

        :param headline: string, the headline to classify
        :return: 0/1: 0 - fake, 1 - real
        '''
        testX = feature.constructRealFea(headline)
        resRF = self.RF.query(testX)
        resRFSK = self.RFSklearn.predict(testX)
        resDT = self.DT.predict(testX)
        resSVM = self.SVM.predict(testX)
        resMLP = self.MLP.predict(testX)
        res = resRF + resRFSK + resDT + resSVM + resMLP
        if res > 2.5:
            return 1
        else:
            return 0

    # rand forest result
    def queryRF(self, headline):
        testX = feature.constructRealFea(headline)
        return self.RF.query(testX)

    # rand forest sklearn result
    def queryRFSK(self, headline):
        testX = feature.constructRealFea(headline)
        return self.RFSklearn.predict(testX)

    # decision tree result
    def queryDT(self, headline):
        testX = feature.constructRealFea(headline)
        return self.DT.predict(testX)

    # neural net result
    def queryMLP(self, headline):
        testX = feature.constructRealFea(headline)
        return self.MLP.predict(testX)

    # SVM result
    def querySVM(self, headline):
        testX = feature.constructRealFea(headline)
        return self.SVM.predict(testX)


if __name__ == "__main__":
    print("THIS IS A SAMPLE.")
    mod = model(fakeFile='./fake2.txt', realFile='./real2.txt')
    print(mod.query("ISIS claims responsibility for Palm Sunday church bombings in Egypt"))
