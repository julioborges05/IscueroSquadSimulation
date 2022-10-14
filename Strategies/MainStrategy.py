from RobotEntities.Attacker import Attacker
from RobotEntities.Defender import Defender
from RobotEntities.GoalKeeper import GoalKeeper
from bridge import (NUM_BOTS, Entity)


class Strategy:
    def __init__(self, matchParameters, selectedStrategy: str):
        self.matchParameters = matchParameters
        if selectedStrategy == "default":
            self.defenderRobotCanAttack = False
        else:
            self.defenderRobotCanAttack = True

    def main_strategy(self):
        robots = [Entity(index=i) for i in range(NUM_BOTS)]
        robots[0] = GoalKeeper(self.matchParameters).setGoalKeeperCoordinates()
        if self.matchParameters.isYellowTeam:
            if self.matchParameters.yellowRobotValues[1].x < self.matchParameters.yellowRobotValues[2].x:
                robots[1] = Attacker(self.matchParameters, 1).setAttackerCoordinates()
                robots[2] = Defender(self.matchParameters, 2, self.defenderRobotCanAttack).setDefenderCoordinates()
            else:
                robots[1] = Defender(self.matchParameters, 1, self.defenderRobotCanAttack).setDefenderCoordinates()
                robots[2] = Attacker(self.matchParameters, 2).setAttackerCoordinates()
        else:
            if self.matchParameters.blueRobotValues[1].x > self.matchParameters.blueRobotValues[2].x:
                robots[1] = Attacker(self.matchParameters, 1).setAttackerCoordinates()
                robots[2] = Defender(self.matchParameters, 2, self.defenderRobotCanAttack).setDefenderCoordinates()
            else:
                robots[1] = Defender(self.matchParameters, 1, self.defenderRobotCanAttack).setDefenderCoordinates()
                robots[2] = Attacker(self.matchParameters, 2).setAttackerCoordinates()

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

