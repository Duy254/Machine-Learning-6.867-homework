__author__ = 'peteflorence'
import numpy as np
from policySearch import PolicySearch

class PolicySearchREINFORCE(PolicySearch):

    def __init__(self, numInnerBins=4, numOuterBins=4, binCutoff=0.5, alphaStepSize=0.2,
                 useQLearningUpdate= False, **kwargs):

        PolicySearch.__init__(self, alphaStepSize=0.2, **kwargs)

        self.numInnerBins=numInnerBins
        self.numOuterBins=numOuterBins
        self.numBins=numInnerBins + numOuterBins
        self.binCutoff=binCutoff
        self.initializePolicyParams()

    def initializePolicyParams(self):
        np.random.seed(4)
        self.policyTheta = np.random.randn(self.numRays,1)

    def computeControlPolicy(self, S):
        raycastDistance = S[1]
        print "raycastDistance shape", np.shape(raycastDistance)
        u = np.dot(policyTheta.T, raycastDistance)
        print "dot product is", u

        return u

    def computeBetaControlPolicy(self, S):
        raycastDistance = S[1]
        feature = raycastDistance * 0.0

        for idx, i in enumerate(feature):
            feature[idx] = (1/raycast[idx]) **2

        theta_a = raycastDistance * 0.0
        theta_a[:len(theta_a)/2] = 1.0
        theta_a0 = 0

        theta_b = raycastDistance * 0.0
        theta_b[len(theta_b)/2:] = 1.0
        theta_b0 = 0

        a = np.dot(theta_a.T, feature) + theta_a0
        b = np.dot(theta_b.T, feature) + theta_b0

        u = np.random.beta(a, b) * 8 - 4

        return u


    def computeDummyControlPolicy(self, S, randomize=True, counter=None):
        actionIdx = 1                  # hardcoded to go straight, for debugging
        u = self.actionSet[actionIdx]

        if randomize:
            if counter is not None:
                epsilon = self.epsilonGreedyDecay(counter)
            else:
                epsilon = self.epsilonGreedy

            if np.random.uniform(0,1,1)[0] < epsilon:
                # otherActionIdx = np.setdiff1d(self.actionSetIdx, np.array([actionIdx]))
                # randActionIdx = np.random.choice(otherActionIdx)
                actionIdx = np.random.choice(self.actionSetIdx)
                u = self.actionSet[actionIdx]

        return u, actionIdx

    def policySearchUpdate(self, S_current, A_idx_current, R, S_next, A_idx_next):
        self.updated = True

    def computeFeatureVector(self, S):
        carState, raycastDistance = S
        featureVec = np.zeros(self.numFeatures)
        featureVec[0] = 1
        featureVec[1:] = utils.inverseTruncate(raycastDistance, self.cutoff, rayLength=self.rayLength,
                                               collisionThreshold=self.collisionThreshold)

        return featureVec



    def computeFeatureVectorFromCurrentFrame(self):
        raycastDistance = self.sensor.raycastAllFromCurrentFrameLocation()
        carState = 0
        S = (carState, raycastDistance)
        featureVec = self.computeFeatureVector(S)
        print ""
        print "innerBins ", featureVec[:self.numInnerBins]
        print "outerBins", featureVec[self.numInnerBins:]
        print ""
        return featureVec


    def computeQValueVectorFromCurrentFrame(self):
        QVec = np.zeros(3)
        fVec = self.computeFeatureVectorFromCurrentFrame()
        for aIdx in xrange(self.numActions):
            fVecTemp = fVec + (aIdx,)
            QVec[aIdx] = self.QValues[fVecTemp]


        print "QVec is", QVec
        aIdxMax = np.argmax(QVec)
        if QVec[aIdxMax] == 0.0:
            print "table value never updated"
        else:
            print "best action is", aIdxMax



