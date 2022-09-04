from RobotEntities.Defender import Defender
from RobotEntities.GoalKeeper import GoalKeeper
from bridge import (NUM_BOTS, Entity)


class Strategy:
    def __init__(self, matchParameters, selectedStrategy: str):
        self.matchParameters = matchParameters
        self.defenderRobotCanAttack = False if selectedStrategy == "default" else True

    def main_strategy(self):
        robots = [Entity(index=i) for i in range(NUM_BOTS)]
        robots[0] = GoalKeeper(self.matchParameters).setGoalKeeperCoordinates()
        robots[1] = Defender(self.matchParameters, 1, self.defenderRobotCanAttack).setDefenderCoordinates()
        robots[2] = self.setRobotToBallCoordinates(robots[2])

        return robots

    def setAllBotsToBallCoordinates(self):
        objectives = [Entity(index=i) for i in range(NUM_BOTS)]
        for obj in objectives:
            obj.x = self.matchParameters.ballValues.x
            obj.y = self.matchParameters.ballValues.y

        return objectives

    def setRobotToBallCoordinates(self, robot):
        robot.x = self.matchParameters.ballValues.x
        robot.y = self.matchParameters.ballValues.y

        return robot

