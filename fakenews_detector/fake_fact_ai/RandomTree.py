"""
    The Random Tree Learner: Implemented By Shiyi Li (GTID:903260643)
    citation:
    Adele Cutler's paper on Random Tree:
    PERT - Perfect Random Tree Ensembles, Adele Cutler, Guohua Zhao
    """
import numpy as np
from scipy import stats


class RandomTree(object):
    def __init__(self, leaf_size=1, verbose=False):
        """
            constructor, but dont actually build the tree, the tree will be built in addEvidence
            leaf_size: max number of Ys in one leaf
            verbose: if true, print info for debugging; if false, no
            """
        self.leaf_size = int(leaf_size)
        pass

    def addEvidence(self, Xtrain, Ytrain):
        """
            in this function we actually build the tree
            Xtrain: ndarray
            Ytrain: 1-d ndarray
            """
        self.tree = self.buildtree(Xtrain, Ytrain)

    def buildtree(self, x, y):
        featurenum = int(x.shape[1])  # how many features does each data point have
        datanum = int(x.shape[0])  # how many data points
        if (datanum <= self.leaf_size):
            return [-1, stats.mode(y)[0], 0, 0]
        Ymax = np.max(y)
        Ymin = np.min(y)
        if (Ymax == Ymin):  # if y.same
            return [-1, Ymax, 0, 0]
        randfeatures = np.random.choice(featurenum, int(featurenum / 2 + 1), replace=False)  # int(featurenum/2+1)
        findthepair = False  # wether we have found the data pair to calculate the SplitVal
        for fea in np.nditer(randfeatures):
            Fmax = np.max(x[:, int(fea)])  # the max value of this feature
            Fmin = np.min(x[:, int(fea)])  # the min value of this feature
            if (Fmax == Fmin):
                continue  # the values of this feature are the same
            for i in range(int(1), int(3)):
                randnodeidx = np.random.choice(datanum, 2, replace=False)
                SplitVal = (x[int(randnodeidx[0]), int(fea)] + x[int(randnodeidx[1]), int(fea)]) / 2
                if (SplitVal == Fmax):
                    continue
                else:
                    findthepair = True
                    break
            if (findthepair == True):
                break
            else:
                findthepair = True
                SplitVal = (Fmax + Fmin) / 2
                break
        if (findthepair == True):
            leftrange = (x[:, int(fea)] <= SplitVal)
            rightrange = ~leftrange
            left = self.buildtree(np.compress(leftrange, x, axis=0), np.compress(leftrange, y, axis=0))
            right = self.buildtree(np.compress(rightrange, x, axis=0), np.compress(rightrange, y, axis=0))
            root = [fea, SplitVal, 1, int(len(left) / 4) + 1]
            return root + left + right
        else:
            leaf = self.makeMandatoryLeaf(y)
            return leaf

    def makeMandatoryLeaf(self, y):
        """
            in this function we will make the data to be a leaf, even though the size is larger than leaf_size
            this is to avoid infinity loop and over-fitting
        """
        leaf = [-1, stats.mode(y)[0], 0, 0]
        return leaf

    def query(self, Xtest):
        """
            Xtest: ndarray
            output: Y (1-d ndarray)
            """
        tree = np.resize(self.tree, (int(len(self.tree) / 4), 4))
        fac = tree[:, 0]
        spv = tree[:, 1]
        lidx = tree[:, 2].astype(np.int)
        ridx = tree[:, 3].astype(np.int)
        datanum = int(Xtest.shape[0])
        feanum = int(Xtest.shape[1])
        # Y=np.empty(nodenum)#####
        nodes = np.zeros(datanum)
        nodes.dtype = np.int
        done = nodes < nodes
        t = done == done
        values = np.empty(datanum)
        auxexp = np.tile(np.arange(0, feanum), datanum)  # [0123...0123....0123]

        while not np.all([done, t]):
            factors = np.take(fac, nodes)  # .astype(np.int)
            l = np.take(lidx, nodes)
            r = np.take(ridx, nodes)
            splitval = np.take(spv, nodes)
            nodeexp = np.repeat(factors, feanum)  # (nodetheyneed,nodenum)
            res = np.resize(nodeexp == auxexp, (datanum, feanum))
            vbyfac = np.sum(res * Xtest, axis=1)
            # vbyfac=np.diag(np.take(Xtest,factors,axis=1))
            values = values * done + ~done * vbyfac  # *Xtest xiang ying de yi hang men
            goright = values > splitval
            nodes += ~goright * l + goright * r
            done = factors == -1
        return splitval
