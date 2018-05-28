'''
Created on Sep 7, 2016

@author: mgomrokchi
'''

class envParams(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.stateSpaceDim=2
        self.stateSpaceRange=[[5,405],[5,405]]
        self.angleRange=[0,360]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"   
        self.gridXscale=400
        self.gridYscale=400
        self.goalPoint=[[165,5],[205,85]]
        self.puddlePoint=[[245,165],[285,245]]
#         self.gridXLength=500
#         self.gridYLength=500
        self.stateFeatureDimX=10
        self.stateFeatureDimY=5
        self.stateFeatureDim=self.stateFeatureDimX*self.stateFeatureDimY
        self.actionFeatureDim=10
        self.goalReward=1000
        self.regularReward=0
        self.puddleReward=-100
        self.wallReward=-1
        self.discountFactor=0.9
        self.actionSTD=(self.angleRange[1]-self.angleRange[0])/(6*self.actionFeatureDim)
#         self.actionSTD=0
        