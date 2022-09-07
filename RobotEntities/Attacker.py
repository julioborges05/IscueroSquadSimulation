from Controllers.MatchParameters import MatchParameters
from Geometry.Triangle import Triangle
from bridge import Entity

import math


class Attacker:
    def __init__(self, matchParameters: MatchParameters, robotIndex: int):
        self.matchParameters = matchParameters
        self.currentRobotLocation = matchParameters.blueRobotValues[robotIndex]

    def setAttackerCoordinates(self):
        attackerRobot = Entity()

        if self.matchParameters.ballValues.x > 0:
            if self.matchParameters.ballValues.y > 0:
                triangle = Triangle((85 - self.currentRobotLocation.x), (10 - self.currentRobotLocation.y))
                attackerRobot.x = self.matchParameters.ballValues.x
                attackerRobot.y = self.currentRobotLocation.y + triangle\
                    .thalesTheoremVerticalValue(self.matchParameters.ballValues.x - self.currentRobotLocation.x)
            if self.matchParameters.ballValues.y < 0:
                triangle = Triangle((85 - self.currentRobotLocation.x), (-10 - self.currentRobotLocation.y))
                attackerRobot.x = self.matchParameters.ballValues.x
                attackerRobot.y = self.currentRobotLocation.y + triangle\
                    .thalesTheoremVerticalValue(self.matchParameters.ballValues.x - self.currentRobotLocation.x)
        else:
            attackerRobot.y = -1 * (self.matchParameters.ballValues.y / 2)
            attackerRobot.x = 10


        return attackerRobot
