from Geometry.Triangle import Triangle
from bridge import Entity
from Controllers.MatchParameters import MatchParameters

import math


class Defender:
    def __init__(self, matchParameters: MatchParameters, robotIndex: int, canAttack: bool):
        self.matchParameters = matchParameters
        self.robotIndex = robotIndex
        self.canAttack = canAttack
        self.currentRobotLocation = self.matchParameters.blueRobotValues[self.robotIndex]

    def setDefenderCoordinates(self):
        defenderRobot = Entity()

        if self.matchParameters.ballValues.x < 0:
            self.__sendBallToAttackQuadrantStrategy(defenderRobot)
        else:
            if self.__canMakeTableStrategy():
                return self.__tableStrategy(defenderRobot)
            self.__sendBallToAttackQuadrantStrategy(defenderRobot)

        return defenderRobot

    def __sendBallToAttackQuadrantStrategy(self, defenderRobot):

        self.sendDefenderRobotToPosition(defenderRobot, self.currentRobotLocation)

        return defenderRobot

    def sendDefenderRobotToPosition(self, defenderRobot, currentRobotLocation):
        ballTriangle = Triangle(-75 - self.matchParameters.ballValues.x, self.matchParameters.ballValues.y)

        defenderRobot.y = self.prepareRobotVerticalPosition(ballTriangle, currentRobotLocation)
        defenderRobot.x = -75 - ballTriangle.thalesTheoremHorizontalValue(defenderRobot.y)

        if defenderRobot.x < -60 and (-35 < defenderRobot.y < 35):
            if defenderRobot.x < -60:
                defenderRobot.x = -57
                defenderRobot.y = self.currentRobotLocation.y + ballTriangle.thalesTheoremVerticalValue(-15)
            elif -35 < defenderRobot.y:
                defenderRobot.y = -38
            else:
                defenderRobot.y = 38

        return defenderRobot

    def prepareRobotVerticalPosition(self, ballTriangle: Triangle, currentRobotLocation):
        firstHorizontalPoint = -75 - ballTriangle.thalesTheoremHorizontalValue(currentRobotLocation.y)
        firstHorizontalValue = firstHorizontalPoint - currentRobotLocation.x
        finalHypotenuseValue = math.sin(ballTriangle.verticalHypotenuseAngle) * firstHorizontalValue
        finalVerticalValue = math.cos(ballTriangle.verticalHypotenuseAngle) * finalHypotenuseValue
        return currentRobotLocation.y + finalVerticalValue

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
        isRobotInTheExpectedRange = (self.matchParameters.blueRobotValues[self.robotIndex].x > defenderRobot.x - 10) \
                                    and (self.matchParameters.blueRobotValues[self.robotIndex].y > defenderRobot.y - 10) \
                                    and (self.matchParameters.blueRobotValues[self.robotIndex].y < defenderRobot.y + 10)

        if isRobotInTheExpectedRange:
            defenderRobot.x = self.matchParameters.ballValues.x
            defenderRobot.y = self.matchParameters.ballValues.y

        return defenderRobot
