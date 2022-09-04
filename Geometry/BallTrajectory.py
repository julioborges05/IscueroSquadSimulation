from Controllers.MatchParameters import MatchParameters
from Geometry.Triangle import Triangle


class BallTrajectory:
    def __init__(self, matchParameters: MatchParameters):
        self.ballTrajectory = Triangle(matchParameters.ballValues.vx, matchParameters.ballValues.vy)
        self.initialX = matchParameters.ballValues.x
        self.initialY = matchParameters.ballValues.y
        self.velocityX = matchParameters.ballValues.vx
        self.velocityY = matchParameters.ballValues.vy
        self.__isYellowTeam = matchParameters.isYellowTeam

    def isBallGoingToGoal(self):
        if not self.__isYellowTeam:
            if self.velocityX >= 0:
                return False

        self.ballTrajectory.thalesTheoremVerticalValue(self.getBigTriangleHorizontalValue())

    def getBigTriangleHorizontalValue(self):
        if self.isBallDowning():
            return

    def isBallDowning(self):
        return self.velocityX < 0 and self.velocityY < 0
