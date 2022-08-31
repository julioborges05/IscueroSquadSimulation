from bridge import (NUM_BOTS, Entity)

from math import pi

class Strategy:
    def main_strategy(self, teamsParameters):
        self.teamsParameters = teamsParameters

        objectives = [Entity(index=i) for i in range(NUM_BOTS)]
        objectives[0].x = -70
        objectives[0].y = 0
        objectives[0].a = pi

        objectives[1] = self.setRobotToBallCordinates(objectives[1])
        objectives[2] = self.setRobotToBallCordinates(objectives[2])

        return objectives

    def setAllBotsToBallCordinates(self):
        objectives = [Entity(index=i) for i in range(NUM_BOTS)]
        for obj in objectives:
            obj.x = self.teamsParameters.ballValues.x
            obj.y = self.teamsParameters.ballValues.y

        return objectives

    def setRobotToBallCordinates(self, robot):
        robot.x = self.teamsParameters.ballValues.x
        robot.y = self.teamsParameters.ballValues.y

        return robot
