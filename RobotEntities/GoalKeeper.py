from Geometry.Triangle import Triangle
from bridge import Entity
from math import (atan, tan)


class GoalKeeper:
    def __init__(self, matchParameters):
        self.matchParameters = matchParameters

    def setGoalKeeperCoordinates(self):
        goalKeeperRobot = Entity()
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
        goalHorizontalPosition = -75 if not self.matchParameters.isYellowTeam else 75
        smallTriangleHorizontalValue = goalHorizontalPosition - (self.matchParameters.ballValues.x - bigTriangle.horizontalValue)
        smallTriangleVerticalValue = (smallTriangleHorizontalValue * bigTriangle.verticalValue) / bigTriangle.horizontalValue

        return Triangle(smallTriangleHorizontalValue, smallTriangleVerticalValue)

    def __getGoalKeeperVerticalValue(self, isBallGoingDown, smallTriangleVerticalValue):
        isBallGoingToGoalInHorizontalDirection = self.matchParameters.ballValues.vx > 0 if not self.matchParameters.isYellowTeam else self.matchParameters.ballValues.vx < 0
        robotVerticalPosition = self.matchParameters.ballValues.y if isBallGoingToGoalInHorizontalDirection \
            else (smallTriangleVerticalValue - 20) if isBallGoingDown else (smallTriangleVerticalValue + 20)

        if robotVerticalPosition > 20:
            return 16.5
        if robotVerticalPosition < -20:
            return -16.5
        return robotVerticalPosition
