from Geometry.Triangle import Triangle
from bridge import Entity
from Controllers.MatchParameters import MatchParameters

import math


class Defender:
    def __init__(self, matchParameters: MatchParameters, robotIndex: int, canAttack: bool):
        self.matchParameters = matchParameters
        self.robotIndex = robotIndex
        self.canAttack = canAttack
        self.currentRobotLocation = self.matchParameters.yellowRobotValues[self.robotIndex] \
            if self.matchParameters.isYellowTeam else self.matchParameters.blueRobotValues[self.robotIndex]

    def setDefenderCoordinates(self):
        defenderRobot = Entity()

        if not self.matchParameters.isYellowTeam:
            if self.matchParameters.ballValues.x < 0:
                self.__sendBallToAttackQuadrantStrategy(defenderRobot)
            else:
                if self.__canMakeTableStrategy():
                    return self.__tableStrategy(defenderRobot)
                self.__sendBallToAttackQuadrantStrategy(defenderRobot)
        else:
            if self.matchParameters.ballValues.x > 0:
                self.__sendBallToAttackQuadrantStrategy(defenderRobot)
            else:
                if self.__canMakeTableStrategy():
                    return self.__tableStrategy(defenderRobot)
                self.__sendBallToAttackQuadrantStrategy(defenderRobot)

        return defenderRobot

    def __sendBallToAttackQuadrantStrategy(self, defenderRobot):
        defenderRobot = self.sendDefenderRobotToInitialPosition(defenderRobot, self.currentRobotLocation)

        if not self.isOutOfTheRange(defenderRobot) and self.matchParameters.ballValues.x > self.currentRobotLocation.x:
            defenderRobot.x = self.matchParameters.ballValues.x
            defenderRobot.y = self.matchParameters.ballValues.y

        return defenderRobot

    def isOutOfTheRange(self, defenderRobot):
        if defenderRobot.y - 5 < self.currentRobotLocation.y < defenderRobot.y + 5:
            return False
        return True

    def sendDefenderRobotToInitialPosition(self, defenderRobot, currentRobotLocation):
        goalParameter = -75 if not self.matchParameters.isYellowTeam else 75
        ballTriangle = Triangle(goalParameter - self.matchParameters.ballValues.x, self.matchParameters.ballValues.y)

        defenderRobot.y = self.prepareRobotVerticalPosition(ballTriangle, currentRobotLocation)
        defenderRobot.x = goalParameter - ballTriangle.thalesTheoremHorizontalValue(defenderRobot.y)

        if not self.matchParameters.isYellowTeam:
            if self.matchParameters.ballValues.x > 0:
                defenderRobot.x = -30
                defenderRobot.y = self.matchParameters.ballValues.y

            if defenderRobot.x < -60 and (-35 < defenderRobot.y < 35):
                if defenderRobot.x < -60:
                    defenderRobot.x = -57
                    defenderRobot.y = self.currentRobotLocation.y + ballTriangle.thalesTheoremVerticalValue(-15)
                elif -35 < defenderRobot.y:
                    defenderRobot.y = -38
                else:
                    defenderRobot.y = 38
        else:
            if self.matchParameters.ballValues.x < 0:
                defenderRobot.x = 30
                defenderRobot.y = self.matchParameters.ballValues.y

            if currentRobotLocation.x > 60 and (-35 < defenderRobot.y < 35):
                if currentRobotLocation.x > 60:
                    defenderRobot.x = 57
                    defenderRobot.y = self.currentRobotLocation.y + ballTriangle.thalesTheoremVerticalValue(15)
                elif -35 < defenderRobot.y:
                    defenderRobot.y = -38
                else:
                    defenderRobot.y = 38

        return defenderRobot

    def prepareRobotVerticalPosition(self, ballTriangle: Triangle, currentRobotLocation):
        goalParameter = -75 if not self.matchParameters.isYellowTeam else 75
        firstHorizontalPoint = goalParameter - ballTriangle.thalesTheoremHorizontalValue(currentRobotLocation.y)
        firstHorizontalValue = firstHorizontalPoint - currentRobotLocation.x
        finalHypotenuseValue = math.sin(ballTriangle.verticalHypotenuseAngle) * firstHorizontalValue
        finalVerticalValue = math.cos(ballTriangle.verticalHypotenuseAngle) * finalHypotenuseValue
        return currentRobotLocation.y + finalVerticalValue

    def __canMakeTableStrategy(self):
        if not self.canAttack:
            return False

        if not self.matchParameters.isYellowTeam:
            if 0 > self.matchParameters.ballValues.x > 35:
                return False
        else:
            if 0 < self.matchParameters.ballValues.x < -35:
                return False

        if 45 > self.matchParameters.ballValues.y > -45:
            return False

        return True

    def __tableStrategy(self, defenderRobot):
        defenderRobot.x = self.matchParameters.ballValues.x - (20 if not self.matchParameters.isYellowTeam else -20)
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
