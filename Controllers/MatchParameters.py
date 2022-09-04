from bridge import (NUM_BOTS, convert_angle)
from math import pi, fmod, atan2, fabs


class MatchParameters:
    def __init__(self, field):
        self.__field = field
        self.blueRobotValues = field["blue"]
        self.yellowRobotValues = field["yellow"]
        self.ballValues = field["ball"]
        self.isYellowTeam = field["mray"]

    def controller(self, our_bots, objectives):
        """
            Basic PID controller that sets the speed of each motor
            sends robot to objective coordinate
            Courtesy of RoboCin
        """

        speeds = [{"index": i} for i in range(NUM_BOTS)]

        # for each bot
        for i, s in enumerate(speeds):
            Kp = 20
            Kd = 2.5

            try:
                self.lastError
            except AttributeError:
                self.lastError = 0

            right_motor_speed = 0
            left_motor_speed = 0

            reversed = False

            objective = objectives[i]
            our_bot = our_bots[i]

            angle_rob = our_bot.a

            angle_obj = atan2(objective.y - our_bot.y,
                              objective.x - our_bot.x)

            error = self.smallestAngleDiff(angle_rob, angle_obj)

            if (fabs(error) > pi / 2.0 + pi / 20.0):
                reversed = True
                angle_rob = convert_angle(angle_rob + pi)
                error = self.smallestAngleDiff(angle_rob, angle_obj)

            # set motor speed based on error and K constants
            error_speed = (Kp * error) + (Kd * (error - self.lastError))

            self.lastError = error

            baseSpeed = 30

            # normalize
            error_speed = error_speed if error_speed < baseSpeed else baseSpeed
            error_speed = error_speed if error_speed > -baseSpeed else -baseSpeed

            if (error_speed > 0):
                left_motor_speed = baseSpeed
                right_motor_speed = baseSpeed - error_speed
            else:
                left_motor_speed = baseSpeed + error_speed
                right_motor_speed = baseSpeed

            if (reversed):
                if (error_speed > 0):
                    left_motor_speed = -baseSpeed + error_speed
                    right_motor_speed = -baseSpeed
                else:
                    left_motor_speed = -baseSpeed
                    right_motor_speed = -baseSpeed - error_speed

            s["left"] = left_motor_speed
            s["right"] = right_motor_speed
        return speeds

    def smallestAngleDiff(self, target, source):
        """Gets the smallest angle between two points in a arch"""
        a = fmod(target + 2 * pi, 2 * pi) - fmod(source + 2 * pi, 2 * pi)

        if (a > pi):
            a -= 2 * pi
        else:
            if (a < -pi):
                a += 2 * pi

        return a
