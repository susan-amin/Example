'''
Created on Nov 14, 2016

@author: Maziar
'''
from ExplorationPolicy import polyExplorer 
# import statistics
import math
import csv
from cycler import cycler
from graphics import *
from builtins import range
import numpy as np
from qLearner import QLearner
import time
from datetime import date
import matplotlib.pyplot as plt

if __name__ == '__main__':
    numIterations=5
    numberOfMoves=50000
    numberOfSteps=10000 #Number of steps during exploration/explore-exploit before we cut it and test the outcome
    numberOfPureExploreMoves=10000 #numberOfEpsilonGreedy would be "numberOfMoves-numberOfPureExploreMoves".
#     numberOfPureExploitMoves=20000
    numberOfTestEvents=5
#     numberOfRoundsExperiments=10
    n=int(numberOfMoves/numberOfSteps)  #Make sure it gives an integer
    timeStepUpperBound=20000
    stepSize=1
    ExpQError=0
    persistenceLengthList=[200]
    randomWalkFlagExploit=0
    randomWalkFlag=0
    puddleFlag=0
    epsilonList=[1]
    learningRateList= [0.01]
    epsilon_init=1
    num1=0
#     k=0
#     n=0
    expResults=[]
    
    for per in range(len(persistenceLengthList)):
        persistenceLength=persistenceLengthList[per]
        persistenceTempResult=[]
        for i in range(len(learningRateList)):
            tempResult=[]
            for j in range(len(epsilonList)):
                iterationAvgRewList=[]
                avgTimeStepList=[]
                avgNormalizedTimeStepList=[]
                successRatioAvgList=[]
                iterationSTDRewList=[]
                STDTimeStepList=[]
                STDNormalizedTimeStepList=[]
                successRatioSTDList=[]
                iterationSTD=0
                iterationAVG=0
                timeStepSTD=0
                timeStepAVG=0
                successAVG=0
                successSTD=0
                for iteration in range(numIterations):
                    averageReward=0
                    totalReward=0
#                     numberOfSuccessfulEvents=0
                    epsilon=epsilon_init
                    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
                    polyexp.setRandomWalkFlag(randomWalkFlag)
                    actionSamplingDensity=polyexp.envparams.actionFeatureDim
                    qAgent = QLearner(learningRateList[i], epsilon_init, actionSamplingDensity, polyexp)
                    weightVec= qAgent.weightVector
                    qAgent.puddleFlag=puddleFlag
                    initPosition=polyexp.drawInitState()
                    tempState=initPosition
                    angle=polyexp.theta_0
                    goalRegion=qAgent.goalZone()
                    win1 = GraphWin("GRID",  polyexp.envparams.stateSpaceRange[0][1]+10-polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]+10-polyexp.envparams.stateSpaceRange[1][0])
                    line1 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]))
                    line1.draw(win1)
                    line2 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]))
                    line2.draw(win1)
                    line3 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]))
                    line3.draw(win1)
                    line4 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]))
                    line4.draw(win1)
                    cir1 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), 5)
                    cir1.draw(win1)
                    cir2 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), 5)
                    cir2.draw(win1)
                    cir3 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), 5)
                    cir3.draw(win1)
                    cir4 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), 5)
                    cir4.draw(win1)
                #     goalPoint=qAgent.goalBorders()
                    goalPoint=[Point(polyexp.envparams.goalPoint[0][0],polyexp.envparams.goalPoint[0][1]),Point(polyexp.envparams.goalPoint[1][0],polyexp.envparams.goalPoint[1][1])]
                    rect = Rectangle(goalPoint[0],goalPoint[1])
                #     rect.setOutline('red')
                    rect.setFill('aquamarine')
                    rect.draw(win1)
                    if puddleFlag==1:
                        puddlePoint=[Point(polyexp.envparams.puddlePoint[0][0],polyexp.envparams.puddlePoint[0][1]),Point(polyexp.envparams.puddlePoint[1][0],polyexp.envparams.puddlePoint[1][1])]
                        rect2= Rectangle(puddlePoint[0],puddlePoint[1])
                        rect2.setFill('Misty Rose')
                        rect2.draw(win1)
                    for stopNumber in range(n):
                        num=stopNumber*numberOfSteps
                        if stopNumber>0:
                            tempState=newStateCut
                            polyexp.currentPosition=oldStateCut
                            polyexp.nextPosition=newStateCut
                            polyexp.cornerIndex=cornerIndexCut
                            polyexp.theta_base=thetaBaseCut
                            polyexp.numberOfsteps=numberOfStepsCut
                            polyexp.numberOfMoves=numberOfMovesCut
                            polyexp.wallVisitFlag=wallVisitFlagCut
                            polyexp.deflectFlag=deflectFlagCut
                            polyexp.actionTemp=actionTempCut
                        while num<((stopNumber+1)*numberOfSteps):
                            print(str(per+1)+":"+str(len(persistenceLengthList))+"--"+str(i+1)+":"+str(len(learningRateList))+"--"+str(j+1)+":"+str(len(epsilonList))+"--"+str(iteration+1)+":"+str(numIterations)+"--"+str(num+1)+"/"+str(numberOfMoves))
                            if qAgent.isInGoalZone(tempState):
                                num1=0
                                ExpQError=0
                                initPosition=polyexp.drawInitState()
                                tempState=initPosition
                                angle=polyexp.theta_0
#                                 if num>=numberOfPureExploreMoves:
#                                 n+=1
#                                 continue
                            if num<numberOfPureExploreMoves:
                                epsilon=epsilon_init
#                                 qAgent.setEpsilon(epsilon)
                            else:
                                epsilon=epsilonList[j]
                                polyexp.setRandomWalkFlag(randomWalkFlagExploit)
                                if i==numberOfPureExploreMoves:
                                    win1.getMouse()
                                    win1.postscript(file="imagePureExplore.eps", colormode='color')
                            qAgent.setEpsilon(epsilon)
                            action=qAgent.getAction(tempState)
        #                         print("action= "+str(action))
                            oldState=tempState
        #                         print("move #"+str(num)+ " = "+str(oldState))
                            tempState=polyexp.move(oldState)
                            newState=tempState
                            if polyexp.deflectFlag==1:
                                action=polyexp.actionTemp
                                polyexp.deflectFlag=0
                            reward=qAgent.getReward(newState)
                            [weightVec,ExpQError,randomWalkFlag,numPolyRLMov,numRandomWalkMov]=qAgent.update(oldState, action, newState, reward,ExpQError,randomWalkFlag,num1)
                            PercentRandomWalkMov=numRandomWalkMov/(numPolyRLMov+numRandomWalkMov)*100
                            print("Number of steps in the new trajectory= ",num1)
                            print("Percentage of Random Walk Moves= ",PercentRandomWalkMov)
                            polyexp.setRandomWalkFlag(randomWalkFlag)
                            num+=1
                            num1+=1
                            line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
                            if randomWalkFlag==1:
                                line.setOutline('red')
                            else:
                                line.setOutline('black')
                            line.draw(win1)
                            
                            win1.postscript(file="image.eps", colormode='color')
                        oldStateCut=oldState
                        newStateCut=newState
                        cornerIndexCut=polyexp.cornerIndex
                        thetaBaseCut=polyexp.theta_base
                        numberOfStepsCut=polyexp.numberOfsteps
                        numberOfMovesCut=polyexp.numberOfMoves
                        wallVisitFlagCut=polyexp.wallVisitFlag
                        deflectFlagCut=polyexp.deflectFlag
                        actionTempCut=polyexp.actionTemp
                         
                        epsilon=0
                        qAgent.setEpsilon(epsilon)
                        totalReward=0 
                        totalTimeStep=0
                        totalNormalizedTimeStep=0
                        number=numberOfTestEvents                 
                        for p in range(numberOfTestEvents):
                            initPosition=polyexp.drawInitState()
                            while qAgent.getReward(initPosition)==polyexp.envparams.goalReward:
                                initPosition=polyexp.drawInitState()
                            polyexp.nextPosition=initPosition
                            tempState=initPosition   
                            minimumTimeStep=qAgent.findMinTimeStep(initPosition)
                            angle=polyexp.theta_0
                            exploitReward=0
                            win2 = GraphWin("GRID",  polyexp.envparams.stateSpaceRange[0][1]+10-polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]+10-polyexp.envparams.stateSpaceRange[1][0])
                            line1 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]))
                            line1.draw(win2)
                            line2 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]))
                            line2.draw(win2)
                            line3 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]))
                            line3.draw(win2)
                            line4 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]))
                            line4.draw(win2)
                            cir1 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), 5)
                            cir1.draw(win2)
                            cir2 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), 5)
                            cir2.draw(win2)
                            cir3 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), 5)
                            cir3.draw(win2)
                            cir4 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), 5)
                            cir4.draw(win2)
                            goalPoint=[Point(polyexp.envparams.goalPoint[0][0],polyexp.envparams.goalPoint[0][1]),Point(polyexp.envparams.goalPoint[1][0],polyexp.envparams.goalPoint[1][1])]
                            #goalPoint=qAgent.goalBorders()
                            rect = Rectangle(goalPoint[0],goalPoint[1])
                            #rect.setOutline('red')
                            rect.setFill('aquamarine')
                            rect.draw(win2)
                            if puddleFlag==1:
                                puddlePoint=[Point(polyexp.envparams.puddlePoint[0][0],polyexp.envparams.puddlePoint[0][1]),Point(polyexp.envparams.puddlePoint[1][0],polyexp.envparams.puddlePoint[1][1])]
                                rect2= Rectangle(puddlePoint[0],puddlePoint[1])
                                rect2.setFill('Misty Rose')
                                rect2.draw(win2)
                            reward=polyexp.envparams.regularReward
                            timeStep=0
                            normalizedTimeStep=0
                            while reward!=polyexp.envparams.goalReward:
                                timeStep+=1
                                if timeStep==timeStepUpperBound:
                                    number-=1
                                    break
                                print(str(per+1)+":"+str(len(persistenceLengthList))+"--"+str(i+1)+":"+str(len(learningRateList))+"--"+str(j+1)+":"+str(len(epsilonList))+"--"+str(iteration+1)+":"+str(numIterations)+"--"+str(num)+"/"+str(numberOfMoves)+"("+str(p+1)+":"+str(numberOfTestEvents)+"--"+str(timeStep)+":"+"unknown"+")"+"StepNumber="+str(num))
                                action=qAgent.getAction(tempState) 
                                oldState=tempState
                                tempState=polyexp.move(oldState)
                                newState=tempState
                                if polyexp.deflectFlag==1:
                                    action=polyexp.actionTemp
                                    polyexp.deflectFlag=0
                                reward=qAgent.getReward(newState)
                                line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
                                line.setOutline('red')
                                line.draw(win2)
                                exploitReward+=reward
    #                         if timeStep!=timeStepUpperBound:
                            normalizedTimeStep=minimumTimeStep/timeStep
    #                             if reward==polyexp.envparams.goalReward:
    #                                 print("Accumulative Reward="+str(exploitReward))
    #                                 print("Reached goal!")
    #                                 numberOfSuccessfulEvents+=1
    #                                 break
    #                             if j==numberOfPureExploitMoves-1:
    #                                 print("Accumulative Reward="+str(exploitReward))
    #                                 print("Didn't reach goal!")
    #                         print("Accumulative Reward="+str(exploitReward))
    #                         print("Number of Steps="+str(timeStep))
                            totalReward=totalReward+exploitReward
                            totalTimeStep+=timeStep
                            totalNormalizedTimeStep+=normalizedTimeStep
                            print("Click on the graph window to continue...")
                            win2.getMouse() # pause for click in window
                            #input("Click on graph window to continue...")
                            win2.postscript(file="Exploit.eps",colormode='color')
                            win2.close()
                        averageReward=totalReward/numberOfTestEvents
                        averageTimeStep=totalTimeStep/numberOfTestEvents
                        averageNormalizedTimeStep=totalNormalizedTimeStep/numberOfTestEvents
                        successRatio=number/numberOfTestEvents
                        if iteration==0:
                            iterationAvgRewList.append(averageReward)
                            avgTimeStepList.append(averageTimeStep)
                            avgNormalizedTimeStepList.append(averageNormalizedTimeStep)
                            successRatioAvgList.append(successRatio)
                            iterationSTDRewList.append(0)
                            STDTimeStepList.append(0)
                            STDNormalizedTimeStepList.append(0)
                            successRatioSTDList.append(0)
    #                     successRatio=numberOfSuccessfulEvents/numberOfTestEvents
                        else:
                            iterationSTDRewList[stopNumber]=math.sqrt(((iteration-1)/iteration)*(iterationSTDRewList[stopNumber]**2)+((averageReward-iterationAvgRewList[stopNumber])**2)/(iteration+1))
                            STDTimeStepList[stopNumber]=math.sqrt(((iteration-1)/iteration)*(STDTimeStepList[stopNumber]**2)+((averageTimeStep-avgTimeStepList[stopNumber])**2)/(iteration+1))
                            STDNormalizedTimeStepList[stopNumber]=math.sqrt(((iteration-1)/iteration)*(STDNormalizedTimeStepList[stopNumber]**2)+((averageNormalizedTimeStep-avgNormalizedTimeStepList[stopNumber])**2)/(iteration+1))
                            successRatioSTDList[stopNumber]=math.sqrt(((iteration-1)/iteration)*(successRatioSTDList[stopNumber]**2)+((successRatio-successRatioAvgList[stopNumber])**2)/(iteration+1))
                            iterationAvgRewList[stopNumber]=(iterationAvgRewList[stopNumber]*iteration+averageReward)/(iteration+1)
                            avgTimeStepList[stopNumber]=(avgTimeStepList[stopNumber]*iteration+averageTimeStep)/(iteration+1)
                            avgNormalizedTimeStepList[stopNumber]=(avgNormalizedTimeStepList[stopNumber]*iteration+averageNormalizedTimeStep)/(iteration+1)
                            successRatioAvgList[stopNumber]=(successRatioAvgList[stopNumber]*iteration+successRatio)/(iteration+1)
                        
                        exploreTimeStep=num
                    
#                     iterationSTD=np.std(iterationAvgRewList)/math.sqrt(len(iterationAvgRewList))*math.sqrt(len(iterationAvgRewList)/(len(iterationAvgRewList)-1))
#                     iterationAVG=np.mean(iterationAvgRewList)
#                     timeStepSTD=np.std(avgTimeStepList)/math.sqrt(len(avgTimeStepList))*math.sqrt(len(avgTimeStepList)/(len(avgTimeStepList)-1))
#                     timeStepAVG=np.mean(avgTimeStepList)
#                     normalizedTimeStepSTD=np.std(avgNormalizedTimeStepList)/math.sqrt(len(avgNormalizedTimeStepList))*math.sqrt(len(avgNormalizedTimeStepList)/(len(avgNormalizedTimeStepList)-1))
#                     normalizedTimeStepAVG=np.mean(avgNormalizedTimeStepList)
#                     successAVG=np.mean(successRatioAvgList)
#                     successSTD=np.std(successRatioAvgList)/math.sqrt(len(successRatioAvgList))*math.sqrt(len(successRatioAvgList)/(len(successRatioAvgList)-1))
#                     bldu = iterationAVG+iterationSTD
#                     bldl = iterationAVG-iterationSTD
                for cutNumber in range(n):
                    tempResult.append([iterationAvgRewList[cutNumber],iterationSTDRewList[cutNumber],avgTimeStepList[cutNumber],STDTimeStepList[cutNumber],avgNormalizedTimeStepList[cutNumber],STDNormalizedTimeStepList[cutNumber],successRatioAvgList[cutNumber],successRatioSTDList[cutNumber],epsilonList[j], learningRateList[i], persistenceLength,(cutNumber+1)*numberOfSteps])
            persistenceTempResult.append(tempResult)
        expResults.append(persistenceTempResult)
#     finalResult=open('Final Result','w')
#     finalResult.write(str(expResults))
    with open('finalResult.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        fieldnames =['Average Reward','Reward STD','Average Time-Step','Time-Step STD','Average Normalized Time-Step','Normalized Time-Step STD','Average Success Ratio','Success Ratio STD','Epsilon','Learning Rate','Persistence Length','Number Of Steps']
        writer.writerow(fieldnames)
        for per in range(len(persistenceLengthList)):
            for alpha in range(len(learningRateList)):
                [writer.writerow(r) for r in expResults[per][alpha]]
            
    
    information=open('information.txt','w')
    information.write('Date: '+str(date.today())+'\n\n\n')
    if randomWalkFlag==0:
        information.write('Pure Explore: Persistence Length\n')
    else:
        information.write('Pure Explore: Random Walk\n')
    if randomWalkFlagExploit==0:
        information.write('Epsilon Greedy Explore: Persistence Length\n')
    else:
        information.write('Epsilon Greedy Explore: Random Walk\n')
    information.write('Region Corner Coordinates: '+str(polyexp.envparams.goalPoint)+'\n\n\n')
    
    information.write('#Pure Explore: '+str(numberOfPureExploreMoves)+'\n')
    information.write('#Epsilon Greedy: '+str(numberOfMoves-numberOfPureExploreMoves)+'\n')
    information.write('#Moves in Each Step'+str(numberOfSteps)+'\n')
#     information.write('#Pure Exploit: '+str(numberOfPureExploitMoves)+'\n')
    
    if polyexp.randomWalkFlag==0 or randomWalkFlagExploit==0:
        information.write('Persistence Length: '+str(persistenceLengthList)+'\n')
    else:
        information.write('Persistence Length: N/A\n')
    information.write('Learning Rate: '+str(learningRateList)+'\n')
    information.write('Epsilon: '+str(epsilonList)+'\n')
    information.write('Discount Factor: '+str(polyexp.envparams.discountFactor)+'\n')
    information.write('Theta STD: '+str(polyexp.STD)+'\n')
    information.write('#Space Regions: '+str(polyexp.envparams.stateFeatureDim)+' (X: '+str(polyexp.envparams.stateFeatureDimX)+', Y: '+str(polyexp.envparams.stateFeatureDimY)+')\n')
    information.write('Environment Corner Coordinates: '+str(polyexp.envparams.stateSpaceRange)+'\n')
    information.write('Angle Range: '+str(polyexp.envparams.angleRange)+'\n')
    information.write('#Action Regions: '+str(polyexp.envparams.actionFeatureDim)+'\n')
    information.write('Action STD: '+str(polyexp.envparams.actionSTD)+'\n\n\n')
    information.write('Regular Reward: '+str(polyexp.envparams.regularReward)+'\n')
    information.write('Wall Reward: '+str(polyexp.envparams.wallReward)+'\n')
    information.write('Goal Reward: '+str(polyexp.envparams.goalReward)+'\n')
    information.write('#Test Events: '+str(numberOfTestEvents)+'\n')
    information.write('#Iterations on Whole Experiment: '+str(numIterations))

#     print(expResults)
    #for i in range(len(learningRateList)):
    #    for j in range(len(epsilonList)):
#     plt.figure()
# #     ax = plt.gca()
# #     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
#     plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
#             
#     avgReward=[]
#     std=[]
#     #Plot average reward as a function of learning rate for a certain persistence length 
#     for k in range(len(epsilonList)):
#         for j in range(len(learningRateList)):
#             avgReward.append(expResults[0][j][k][0])
#             std.append(expResults[0][j][k][1])
#         print(avgReward)
#         print(std)
#         plt.errorbar(learningRateList, avgReward, yerr=std, fmt='o')   
#         avgReward=[]
#         std=[]
#             
#     
#     print(expResults)
#     
# #     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
#     
# #     plt.xlim(0,1)
# #     plt.ylim(-100,100)
#     plt.ylabel('Average Reward')
#     plt.xlabel('Learning Rate')
#     plt.legend(["epsilon=0.1","epsilon=0.4", "epsilon=0.7" ],loc=0)
#     plt.title("Average Reward for P=200")
#     plt.savefig('1.png')
#     
#     plt.figure()
# #     ax1 = plt.gca()
# #     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
#     plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
#     avgTimeStep=[]
#     std=[]
#     for k in range(len(epsilonList)):
#         for j in range(len(learningRateList)):
#             avgTimeStep.append(expResults[0][j][k][2])
#             std.append(expResults[0][j][k][3])
#         print(avgTimeStep)
#         print(std)
#         plt.errorbar(learningRateList, avgTimeStep, yerr=std, fmt='o')   
#         avgTimeStep=[]
#         std=[]
#             
#     
#     print(expResults)
#     
# #     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
#     
# #     plt.xlim(0,1)
# #     plt.ylim(-0.5,1)
#     plt.ylabel('Average Time Steps')
#     plt.xlabel('Learning Rate')
#     plt.legend(["epsilon=0.1","epsilon=0.4", "epsilon=0.7" ],loc=0)
#     plt.title("Average Time Steps for P=200")
#     plt.savefig('2.png')
#     
#     plt.figure()
# #     ax2 = plt.gca()
# #     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
#     plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
#             
#     avgReward=[]
#     std=[]
#     #Plot average reward as a function of learning rate for a certain persistence length 
#     for j in range(len(learningRateList)):
#         for i in range(len(persistenceLengthList)):
#             avgReward.append(expResults[i][j][0][0])
#             std.append(expResults[i][j][0][1])
#         print(avgReward)
#         print(std)
#         plt.errorbar(persistenceLengthList, avgReward, yerr=std, fmt='o')   
#         avgReward=[]
#         std=[]
#             
#     
#     print(expResults)
#     
# #     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
#     
# #     plt.xlim(0,1000)
# #     plt.ylim(-100,100)
#     plt.ylabel('Average Reward')
#     plt.xlabel('Persistence Length')
#     plt.legend(["alpha=0.05","alpha=0.1", "alpha=0.2", "alpha=0.3", "alpha=0.4", "alpha=0.5"  ],loc=0)
#     plt.title("Average Reward for epsilon=0.1")
#     plt.savefig('3.png')
#     
#     plt.figure()
# #     ax3 = plt.gca()
# #     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
#     plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
#     avgTimeStep=[]
#     std=[]
#     for j in range(len(learningRateList)):
#         for i in range(len(persistenceLengthList)):
#             avgTimeStep.append(expResults[i][j][0][2])
#             std.append(expResults[i][j][0][3])
#         print(avgTimeStep)
#         print(std)
#         plt.errorbar(persistenceLengthList, avgTimeStep, yerr=std, fmt='o')   
#         avgTimeStep=[]
#         std=[]
#             
#     
#     print(expResults)
#     
# #     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
#     
# #     plt.xlim(0,1000)
# #     plt.ylim(-0.5,1)
#     plt.ylabel('Average Time Steps')
#     plt.xlabel('Persistence Length')
#     plt.legend(["alpha=0.05","alpha=0.1", "alpha=0.2", "alpha=0.3", "alpha=0.4", "alpha=0.5"  ],loc=0)
#     plt.title("Average Time Steps for epsilon=0.1")
#     plt.savefig('4.png')
#     plt.show()
#     
#     
#     
#     
#     
#     
    
    
    
    
    
    
#     mean_V_vs_LSW[j]=abs(numpy.average(temptemp))
#     std_V_vs_LSW[j] = numpy.std(temptemp)
#     V_vs_LSW_bldu[j] = math.log10(abs(mean_V_vs_LSW[j]+std_V_vs_LSW[j]))-math.log10(abs(mean_V_vs_LSW[j]))
#     V_vs_LSW_bldl[j] = -math.log10(abs(mean_V_vs_LSW[j]-std_V_vs_LSW[j]))+math.log10(abs(mean_V_vs_LSW[j]))
#     V_vs_LSW_blm[j] = math.log10(abs(mean_V_vs_LSW[j]))
    
