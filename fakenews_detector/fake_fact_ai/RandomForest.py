"""
    The Random Forest - classification version
    """
import numpy as np
from scipy import stats

import fakenews_detector.fake_fact_ai.RandomTree as rt


class RandomForest(object):
    # faster than sklearn

    def __init__(self, learner=rt.RandomTree, kwargs={"leaf_size": 1}, bags=20, boost=False, verbose=False):
        self.learner = learner
        self.leaf_size = kwargs["leaf_size"]
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.treelist = []  # use list to store trees

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        leaf_size = int(self.leaf_size)
        datanum = int(dataX.shape[0])  # how many data points
        featurenum = int(dataX.shape[1])  # how many features does each data point have
        ######SLOW

        for iter in range(int(1), int(self.bags + 1)):
            randidx = np.random.choice(datanum, int(datanum / 2), replace=True)
            x = np.take(dataX, randidx, axis=0)
            y = np.take(dataY, randidx)
            newlearner = self.learner(leaf_size, verbose=False)
            newlearner.addEvidence(x, y)
            self.treelist.append(newlearner)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        rowrange = int(points.shape[0])
        y = 9 * np.ones(rowrange);
        for iter in range(0, int(self.bags)):
            y = np.append(y, self.treelist[iter].query(points))
        # mean: axis=0
        y = y.reshape((int(self.bags) + 1, rowrange));
        yy = np.array(stats.mode(y)[0]).reshape(rowrange);
        return yy
