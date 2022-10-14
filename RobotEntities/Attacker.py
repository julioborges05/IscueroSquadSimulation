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
        if self.matchParameters.isYellowTeam:
            if self.matchParameters.ballValues.x < 0 and self.currentRobotLocation.x > self.matchParameters.ballValues.x:
                attackerRobot.x = self.matchParameters.ballValues.x
                attackerRobot.y = self.matchParameters.ballValues.y
                return attackerRobot
        else:
            if self.matchParameters.ballValues.x > 0 and self.currentRobotLocation.x < self.matchParameters.ballValues.x:
                attackerRobot.x = self.matchParameters.ballValues.x
                attackerRobot.y = self.matchParameters.ballValues.y
                return attackerRobot

        return self.defaultAttack()

    def defaultAttack(self):
        attackerRobot = Entity()

        if not self.matchParameters.isYellowTeam:
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
                attackerRobot.y = (self.matchParameters.ballValues.y * 1.25)
                attackerRobot.x = 10
        else:
            if self.matchParameters.ballValues.x < 0:
                if self.matchParameters.ballValues.y > 0:
                    triangle = Triangle((-85 - self.currentRobotLocation.x), (10 - self.currentRobotLocation.y))
                    attackerRobot.x = self.matchParameters.ballValues.x
                    attackerRobot.y = self.currentRobotLocation.y + triangle\
                        .thalesTheoremVerticalValue(self.matchParameters.ballValues.x - self.currentRobotLocation.x)
                if self.matchParameters.ballValues.y < 0:
                    triangle = Triangle((-85 - self.currentRobotLocation.x), (-10 - self.currentRobotLocation.y))
                    attackerRobot.x = self.matchParameters.ballValues.x
                    attackerRobot.y = self.currentRobotLocation.y + triangle\
                        .thalesTheoremVerticalValue(self.matchParameters.ballValues.x - self.currentRobotLocation.x)
            else:
                attackerRobot.y = (self.matchParameters.ballValues.y * 1.25)
                attackerRobot.x = -10

        return attackerRobot