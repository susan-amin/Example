'''
Created on Oct 17, 2016

@author: Maziar Gomorkchi and Susan Amin
'''
import random
import copy
import numpy as np 
import math
import random
# from graphics import *
from envParams import envParams
from argparse import Action

class QLearner(object):
    '''
    This is the function approximation implementation of QLearning algorithm
    '''


    def __init__(self, learningRate, epsilon, actionSamplingDensity, polyExplorer):
        #Should initialize the weight vector
        self.envparams = envParams()
        self.weightVectorDim=self.envparams.stateFeatureDim+self.envparams.actionFeatureDim
        self.actionMatrix=np.zeros((self.envparams.stateFeatureDim,self.envparams.actionFeatureDim))
        self.spaceVector=[0]*self.envparams.stateFeatureDim
        self.weightVector=[]
        self.epsilon= epsilon
        self.stepSize=1
        self.persistenceLength=200
        self.polyexp= polyExplorer
        self.LearningRate= learningRate
        self.actionSamplingDensity= actionSamplingDensity
        self.exploitFlag=0
        self.puddleFlag=0
        self.goalRegion=0
        self.stateRegionXLength=(self.envparams.stateSpaceRange[0][1]-self.envparams.stateSpaceRange[0][0])/self.envparams.stateFeatureDimX
        self.stateRegionYLength=(self.envparams.stateSpaceRange[1][1]-self.envparams.stateSpaceRange[1][0])/self.envparams.stateFeatureDimY
        self.numPolyRLMov=1
        self.numRandomWalkMov=0
#         self.weightHeatMap=np.zeros((self.envparams.stateSpaceRange[0][1]-self.envparams.stateSpaceRange[0][0],self.envparams.stateSpaceRange[1][1]-self.envparams.stateSpaceRange[1][0]))

    def goalBorders(self):
        yMod=self.goalRegion%self.envparams.stateFeatureDimX
        if yMod==0:
            yBorderL=(math.floor(self.goalRegion/self.envparams.stateFeatureDimX)-1)*self.stateRegionYLength+self.envparams.stateSpaceRange[1][0]
        else:       
            yBorderL=math.floor(self.goalRegion/self.envparams.stateFeatureDimX)*self.stateRegionYLength+self.envparams.stateSpaceRange[1][0]
        yBorderU=yBorderL+self.stateRegionYLength
        xMod=self.goalRegion%self.envparams.stateFeatureDimX
        if xMod==0:
            xBorderL=(self.goalRegion-1-(math.floor(self.goalRegion/self.envparams.stateFeatureDimX)-1)*self.envparams.stateFeatureDimX)*self.stateRegionXLength+self.envparams.stateSpaceRange[0][0]
        else:
            xBorderL=(self.goalRegion-1-math.floor(self.goalRegion/self.envparams.stateFeatureDimX)*self.envparams.stateFeatureDimX)*self.stateRegionXLength+self.envparams.stateSpaceRange[0][0]
        xBorderU=xBorderL+self.stateRegionXLength
        point1=Point(xBorderL,yBorderL)
        point2=Point(xBorderU,yBorderU)
        return [point1,point2]
        
    def setEpsilon(self, epsilon):
        self.epsilon=epsilon
        
    def phi(self, state, action) :
#         phiVec=np.zeros(self.envparams.stateFeatureDim+self.envparams.actionFeatureDim)
        phiVec=np.zeros(self.envparams.actionFeatureDim)
        #actionWidth=math.floor(((self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.envparams.actionFeatureDim))
#         actionRegion= math.floor(action*self.envparams.actionFeatureDim/(self.envparams.angleRange[1]-self.envparams.angleRange[0]))
        actionRegion= math.floor((action-self.envparams.angleRange[0])*self.envparams.actionFeatureDim/(self.envparams.angleRange[1]-self.envparams.angleRange[0]))+1
        if (action-self.envparams.angleRange[0])*self.envparams.actionFeatureDim%(self.envparams.angleRange[1]-self.envparams.angleRange[0])==0:
            actionRegion=actionRegion-1
#         phiVec[actionRegion+self.envparams.stateFeatureDim-1]=1
        phiVec[actionRegion-1]=1
#         gridDiag= math.floor((self.envparams.gridXLength**2+self.envparams.gridXLength**2)**0.5)
#         x=int(state[0])
#         y=int(state[1])
#         stateWidth = math.floor(gridDiag/self.envparams.stateFeatureDim)
#         stateRegion= math.floor(((x**2+y**2)**0.5)/stateWidth)
#         phiVec[self.spaceRegion(state)]=1
        return phiVec
        #returns a vector in self.weightVector Dim
    def  spaceRegion(self,state): 
        xRegionNumber=math.floor((state[0]-self.envparams.stateSpaceRange[0][0])/self.stateRegionXLength)+1
        if state[0]==self.envparams.stateSpaceRange[0][1]:
            xRegionNumber=xRegionNumber-1
        yRegionNumber=math.floor((state[1]-self.envparams.stateSpaceRange[1][0])/self.stateRegionYLength)+1
        if state[1]==self.envparams.stateSpaceRange[1][1]:
            yRegionNumber=yRegionNumber-1
        regionNumber=(yRegionNumber-1)*self.envparams.stateFeatureDimX+xRegionNumber
        if regionNumber==self.envparams.stateFeatureDim+1:
            regionNumber-=1
        phiIndex=regionNumber-1
        return phiIndex    
    
    def getQValue(self, state , action):
        qValue=np.dot(self.setWeightVector(state, action),self.phi(state,action))
        return qValue
    
#     def actionRange(self,state): 
#         wallIndicator=self.polyexp.isOnWall(state)
#         if not wallIndicator:
#             lower=self.envparams.angleRange[0]
#             upper=self.envparams.angleRange[1]
#         elif state[0]==self.envparams.stateSpaceRange[0][0]:
#             if state[1]==self.envparams.stateSpaceRange[1][0]:
#                 lower=0
#                 upper=90
#             elif state[1]==self.envparams.stateSpaceRange[1][1]:
#                 lower=-90
#                 upper=0
#             else:
#                 lower=-90
#                 upper=90
#         elif state[0]==self.envparams.stateSpaceRange[0][1]:
#             if state[1]==self.envparams.stateSpaceRange[1][0]:
#                 lower=90
#                 upper=180
#             elif state[1]==self.envparams.stateSpaceRange[1][1]:
#                 lower=180
#                 upper=270
#             else:
#                 lower=90
#                 upper=270
#         elif state[1]==self.envparams.stateSpaceRange[1][0]:
#                 lower=0
#                 upper=180
#         elif state[1]==self.envparams.stateSpaceRange[1][1]:
#                 lower=180
#                 upper=360
#         return [lower,upper]
    def sampleActionSet(self,state):
        sampledActionSet=[]
#         for i in range(self.actionSamplingDensity):
#             temp=random.choice(range(lower+(i)*step, lower+(i+1)*step))
#             if temp in sampledActionSet:
#                 i-=1
#                 continue
#             else:
#                 sampledActionSet.append(temp)
        for i in range(self.actionSamplingDensity):
            sampledActionSet.append(self.envparams.angleRange[0]+(i+1)*((self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.actionSamplingDensity))
        
        
        return sampledActionSet
        
    
    def getValue(self, state):
        sampledActionSet =self.sampleActionSet(state)
        maxTemp= self.getQValue(state, sampledActionSet[0])
        actionSameQ=[]
        actionSameQFlag=0
        for action in sampledActionSet:
            s=self.getQValue(state, action)
            if self.getQValue(state, action)>maxTemp:
                actionSameQFlag=0
                maxTemp=self.getQValue(state, action)
                actionSameQ=[]
                actionSameQ.append(action)
            elif self.getQValue(state, action)==maxTemp:
                actionSameQ.append(action)
                actionSameQFlag=1
            else:
                continue
        if actionSameQFlag==1 and self.getQValue(state, actionSameQ[0])>=maxTemp:
            maxTemp=self.getQValue(state,random.choice(actionSameQ))
        return maxTemp
    
    def getPolicy(self, state):
        sampledActionSet= self.sampleActionSet(state)
        maxTemp= self.getQValue(state, sampledActionSet[0])
#         action= self.polyexp.theta_base
#         maxTemp=self.getQValue(state, action)
        actionSameQ=[]
        actionSameQFlag=0
        for act in sampledActionSet:
            s=self.getQValue(state, act)
            if self.getQValue(state, act)>maxTemp:
                actionSameQFlag=0
                maxTemp=self.getQValue(state, act)
                actionSameQ=[]
                actionSameQ.append(act)
                action=act
            elif self.getQValue(state, act)==maxTemp:
                actionSameQ.append(act)
                actionSameQFlag=1
            else:
                continue
        if actionSameQFlag==1 and self.getQValue(state, actionSameQ[0])>=maxTemp:
            action=random.choice(actionSameQ)
        actionRegion= math.floor((action-self.envparams.angleRange[0])*self.envparams.actionFeatureDim/(self.envparams.angleRange[1]-self.envparams.angleRange[0]))+1
        if (action-self.envparams.angleRange[0])*self.envparams.actionFeatureDim%(self.envparams.angleRange[1]-self.envparams.angleRange[0])==0:
            actionRegion=actionRegion-1
        meanOfActionRegion=self.envparams.angleRange[0]+((2*actionRegion-1)*(self.envparams.angleRange[1]-self.envparams.angleRange[0])/(2*self.envparams.actionFeatureDim))
        action=random.normalvariate(meanOfActionRegion,self.envparams.actionSTD)
        while action>self.envparams.angleRange[0]+actionRegion*(self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.envparams.actionFeatureDim or action<=self.envparams.angleRange[0]+(actionRegion-1)*(self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.envparams.actionFeatureDim:
            action=random.normalvariate(meanOfActionRegion,self.envparams.actionSTD)
        return action
    
    def goalZone(self):
        goalRegion=random.randint(1,self.envparams.stateFeatureDim)
        self.goalRegion=goalRegion
        return goalRegion
    
    def isInGoalZone(self,state):
        if state[0]>=self.envparams.goalPoint[0][0] and state[0]<=self.envparams.goalPoint[1][0] and state[1]>=self.envparams.goalPoint[0][1] and state[1]<=self.envparams.goalPoint[1][1]:
#         if self.spaceRegion(state)+1==self.goalRegion:
            return True
        else:
            return False
    def isInPuddleZone(self,state):
        if state[0]>=self.envparams.puddlePoint[0][0] and state[0]<=self.envparams.puddlePoint[1][0] and state[1]>=self.envparams.puddlePoint[0][1] and state[1]<=self.envparams.puddlePoint[1][1]:
#         if self.spaceRegion(state)+1==self.goalRegion:
            return True
        else:
            return False
    def findMinTimeStep(self,state):
        if self.getReward(state)==self.envparams.goalReward:
            return 0
        else:
            if state[0]<=self.envparams.goalPoint[1][0] and state[0]>=self.envparams.goalPoint[0][0]:
                Ly1=abs(state[1]-self.envparams.goalPoint[0][1])
                Ly2=abs(state[1]-self.envparams.goalPoint[1][1])
                return min(Ly1,Ly2)
            elif state[1]<=self.envparams.goalPoint[1][1] and state[1]>=self.envparams.goalPoint[0][1]: 
                Lx1=abs(state[0]-self.envparams.goalPoint[0][0])
                Lx2=abs(state[0]-self.envparams.goalPoint[1][0])
                return min(Lx1,Lx2)
            else:
                Lr1=(math.sqrt((state[0]-self.envparams.goalPoint[0][0])**2+(state[1]-self.envparams.goalPoint[0][1])**2)).real
                Lr2=(math.sqrt((state[0]-self.envparams.goalPoint[1][0])**2+(state[1]-self.envparams.goalPoint[0][1])**2)).real
                Lr3=(math.sqrt((state[0]-self.envparams.goalPoint[0][0])**2+(state[1]-self.envparams.goalPoint[1][1])**2)).real
                Lr4=(math.sqrt((state[0]-self.envparams.goalPoint[1][0])**2+(state[1]-self.envparams.goalPoint[1][1])**2)).real
                return min(Lr1,Lr2,Lr3,Lr4)
    def getReward(self, state):
        if self.puddleFlag==1:
            if self.isInPuddleZone(state):
                return self.envparams.puddleReward
        if self.isInGoalZone(state):
            return self.envparams.goalReward
        elif self.polyexp.isOnWall(state):
            return self.envparams.wallReward
        else:
            return self.envparams.regularReward
    def decision(self):
        self.exploitFlag=0
        if random.uniform(0, 1)<self.epsilon:
            return 0 #Explore
        else:
            return 1  #Exploit
    
    def getAction(self,state):
        if self.decision()==0:
            #Exploration only
            self.polyexp.directionFlag=1
            self.polyexp.exploit=0
            action= self.polyexp.move(state)
            self.polyexp.directionFlag=0
        else:
            self.exploitFlag=1
            self.polyexp.exploit=1
            action= self.getPolicy(state)
            self.polyexp.theta_base=action
            self.polyexp.wallVisitFlag=0
            self.polyexp.cornerIndex=0
        return action
    
    def setWeightVector(self,state,action):
        regionIndex=self.spaceRegion(state)
#         weightVector=copy.copy(self.spaceVector)
#         weightVector.extend(self.actionMatrix[regionIndex,])
        weightVector=copy.copy(self.actionMatrix[regionIndex,])
        self.weightVector=weightVector
        return self.weightVector
        
    
    def update(self, state, action, nextState, reward,ExpQError,randomWalkFlag,num1):
        qError= reward + self.envparams.discountFactor*self.getValue(nextState)-self.getQValue(state, action)
        if randomWalkFlag==0:
            self.numPolyRLMov+=1
        else:
            self.numRandomWalkMov+=1
        if qError<=abs(ExpQError):
            randomWalkFlag=0
        else:
            randomWalkFlag=1
        ExpQError=(ExpQError*(num1)+qError)/(num1+1)
        self.weightVector=self.setWeightVector(state, action) + self.LearningRate*qError*self.phi(state,action)
#         for i in range(self.envparams.stateFeatureDim):
#             self.spaceVector[i]=self.weightVector[i]
#         for i in range(self.envparams.actionFeatureDim):
#             self.actionMatrix[self.spaceRegion(state)][i]=self.weightVector[self.envparams.stateFeatureDim+i]
        for i in range(self.envparams.actionFeatureDim):
            self.actionMatrix[self.spaceRegion(state)][i]=self.weightVector[i]
        return [self.weightVector,ExpQError,randomWalkFlag,self.numPolyRLMov,self.numRandomWalkMov]
    
            
 #Changes                     
    
        
        
        
