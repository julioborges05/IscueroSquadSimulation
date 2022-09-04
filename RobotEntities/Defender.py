from Geometry.Triangle import Triangle
from bridge import Entity
from Controllers.MatchParameters import MatchParameters

import math


class Defender:
    def __init__(self, matchParameters: MatchParameters, robotIndex: int, canAttack: bool):
        self.matchParameters = matchParameters
        self.robotIndex = robotIndex
        self.canAttack = canAttack

    def setDefenderCoordinates(self):
        defenderRobot = Entity()

        if self.matchParameters.ballValues.x < 0:
            self.__sendBallToAttackQuadrantStrategy(defenderRobot)

        if self.__canMakeTableStrategy():
            return self.__tableStrategy(defenderRobot)

        return defenderRobot

    def __sendBallToAttackQuadrantStrategy(self, defenderRobot):
        currentRobotLocation = self.matchParameters.blueRobotValues[self.robotIndex]
        self.sendDefenderRobotToPosition(defenderRobot, currentRobotLocation)

        return defenderRobot

    def sendDefenderRobotToPosition(self, defenderRobot, currentRobotLocation):
        if self.matchParameters.ballValues.y > 20:
            bigTriangle = Triangle(-75 - self.matchParameters.ballValues.x, self.matchParameters.ballValues.y - 20)
            defenderRobot.y = 20 + bigTriangle.thalesTheoremVerticalValue((-75 - self.matchParameters.ballValues.x) / 2)
            defenderRobot.x = (-75 + self.matchParameters.ballValues.x) / 2
            return defenderRobot

        elif self.matchParameters.ballValues.y < -20:
            bigTriangle = Triangle(-75 - self.matchParameters.ballValues.x, self.matchParameters.ballValues.y + 20)
            defenderRobot.y = -20 + bigTriangle.thalesTheoremVerticalValue((-75 - self.matchParameters.ballValues.x) / 2)
            defenderRobot.x = (-75 + self.matchParameters.ballValues.x) / 2
            return defenderRobot

        return defenderRobot

    def __canMakeTableStrategy(self):
        if not self.canAttack:
            return False

        if 0 > self.matchParameters.ballValues.x > 35:
            return False

        if 45 > self.matchParameters.ballValues.y > -45:
            return False

        return True

    def __tableStrategy(self, defenderRobot):
        defenderRobot.x = self.matchParameters.ballValues.x - 20
        isOnTheTopQuadrant = True if self.matchParameters.ballValues.y > 0 else False
        maximumVerticalValue = 65 if isOnTheTopQuadrant else -65

        smallTriangle = Triangle((60 - self.matchParameters.ballValues.x),
                                 (maximumVerticalValue - self.matchParameters.ballValues.y))
        defenderRobot.y = maximumVerticalValue - (
            smallTriangle.thalesTheoremVerticalValue(60 - (self.matchParameters.ballValues.x - 15)))

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
