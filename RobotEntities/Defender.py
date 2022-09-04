from Geometry.Triangle import Triangle
from bridge import Entity
from Controllers.TeamsParameters import TeamsParameters

import math


class Defender:
    def __init__(self, matchParameters: TeamsParameters, robotIndex: int):
        self.matchParameters = matchParameters
        self.robotIndex = robotIndex

    def setDefenderCoordinates(self):
        defenderRobot = Entity()

        if self.__canMakeTableStrategy():
            return self.__tableStrategy(defenderRobot)

        defenderRobot.x = self.matchParameters.ballValues.x
        defenderRobot.y = self.matchParameters.ballValues.y
        return defenderRobot

    def __canMakeTableStrategy(self):
        if not self.matchParameters.ballValues.x > 0:
            return False

        if self.matchParameters.ballValues.x > 35:
            return False

        if 45 > self.matchParameters.ballValues.y > -45:
            return False

        return True

    def __tableStrategy(self, defenderRobot):
        defenderRobot.x = self.matchParameters.ballValues.x - 20
        isOnTheTopQuadrant = True if self.matchParameters.ballValues.y > 0 else False
        maximumVerticalValue = 65 if isOnTheTopQuadrant else -65

        smallTriangle = Triangle((60 - self.matchParameters.ballValues.x), (maximumVerticalValue - self.matchParameters.ballValues.y))
        defenderRobot.y = maximumVerticalValue - (smallTriangle.thalesTheoremVerticalValue(60 - (self.matchParameters.ballValues.x - 15)))

        defenderRobot.a = smallTriangle.verticalHypotenuseAngle
        isRobotInTheExpectedRange = self.__isRobotInTheExpectedRange(defenderRobot)

        if isRobotInTheExpectedRange:
            defenderRobot.x = self.matchParameters.ballValues.x
            defenderRobot.y = self.matchParameters.ballValues.y

        return defenderRobot

    def __isRobotInTheExpectedRange(self, defenderRobot):
        return (self.matchParameters.blueRobotValues[self.robotIndex].x > defenderRobot.x - 10) \
               and (self.matchParameters.blueRobotValues[self.robotIndex].y > defenderRobot.y - 10) \
               and (self.matchParameters.blueRobotValues[self.robotIndex].y < defenderRobot.y + 10)
