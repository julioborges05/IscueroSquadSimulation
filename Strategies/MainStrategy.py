from Parameters.Triangle import Triangle
from bridge import (NUM_BOTS, Entity)
from math import atan, tan


class Strategy:
    def __init__(self, matchParameters):
        self.matchParameters = matchParameters

    def main_strategy(self):
        objectives = [Entity(index=i) for i in range(NUM_BOTS)]
        self.setGoalKeeperCoordinates(objectives[0])
        objectives[1] = self.setRobotToBallCoordinates(objectives[1])
        objectives[2] = self.setRobotToBallCoordinates(objectives[2])

        return objectives

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

    def setGoalKeeperCoordinates(self, goalKeeperRobot):
        goalKeeperRobot.x = 75 if self.matchParameters.isYellowTeam else -75
        try:
            isBallGoingDown = self.matchParameters.ballValues.vy < 0
            bigTriangle = self.__getBigTriangleValues(isBallGoingDown)
            smallTriangle = self.__getSmallTriangleValues(bigTriangle)

            goalKeeperRobot.y = self.__getGoalKeeperVerticalValue(isBallGoingDown, smallTriangle.verticalValue)
            return goalKeeperRobot
        except ZeroDivisionError:
            return goalKeeperRobot

    def __getBigTriangleValues(self, isBallGoingDown):
        ballVelocityAngle = atan(self.matchParameters.ballValues.vx / self.matchParameters.ballValues.vy)

        bigTriangleVerticalValue = self.matchParameters.ballValues.y + (20 if isBallGoingDown else -20)
        bigTriangleHorizontalValue = tan(ballVelocityAngle) * bigTriangleVerticalValue
        return Triangle(bigTriangleHorizontalValue, bigTriangleVerticalValue)

    def __getSmallTriangleValues(self, bigTriangle):
        smallTriangleHorizontalValue = -75 - (self.matchParameters.ballValues.x - bigTriangle.horizontalValue)
        smallTriangleVerticalValue = (smallTriangleHorizontalValue * bigTriangle.verticalValue) / bigTriangle.horizontalValue

        return Triangle(smallTriangleHorizontalValue, smallTriangleVerticalValue)

    def __getGoalKeeperVerticalValue(self, isBallGoingDown, smallTriangleVerticalValue):
        robotVerticalPosition = self.matchParameters.ballValues.y if self.matchParameters.ballValues.vx > 0\
            else (smallTriangleVerticalValue - 20) if isBallGoingDown else (smallTriangleVerticalValue + 20)

        if robotVerticalPosition > 20:
            return 16.5
        if robotVerticalPosition < -20:
            return -16.5
        return robotVerticalPosition
