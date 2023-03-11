import sys

from Controllers.MatchParameters import MatchParameters
from Strategies.MainStrategy import Strategy

from bridge import (Actuator, Replacer, Vision, Referee)

if __name__ == "__main__":

    PENALTY = 1
    GOAL_KICK = 2
    FREEBALL = 3
    KICKOFF = 4
    GAME_STOPPED = 5
    # FOUL_SECRET = 6
    GAME_HALTED = 7

    try:
        team = sys.argv[1]

        if team != "yellow" and team != "blue":
            sys.exit()
    except:
        print("Selecione time corretamente")
        sys.exit()

    if team == "yellow":
        isYellowTeam = True
    else:
        isYellowTeam = False

    # Initialize all clients
    actuator = Actuator(isYellowTeam, "127.0.0.1", 20011)
    replacement = Replacer(isYellowTeam, "224.5.23.2", 10004)
    vision = Vision(isYellowTeam, "224.0.0.1", 10002)
    referee = Referee(isYellowTeam, "224.5.23.2", 10003)

    while True:
        referee.update()
        ref_data = referee.get_data()
        vision.update()

        teamsParameters = MatchParameters(vision.get_field_data())

        if ref_data["game_on"]:
            objectives = Strategy(teamsParameters, "default").main_strategy()
            actuator.send_all(teamsParameters.controller(teamsParameters.yellowRobotValues
                                                         if teamsParameters.isYellowTeam
                                                         else teamsParameters.blueRobotValues,
                                                         objectives))

        elif ref_data["foul"] != GAME_HALTED:
            # foul behaviour
            if ref_data["foul"] == GOAL_KICK and not ref_data["yellow"]:
                replacement.place(0, -75, 0, 90)
                replacement.place(1, -65, -40 if teamsParameters.ballValues.y < 0 else 40, 30 if teamsParameters.ballValues.y < 0 else -30)
                replacement.place(2, -40, -10, 0)
                replacement.send()
            if ref_data["foul"] == KICKOFF:
                replacement.place(0, -75, 0, 90)
                replacement.place(1, -25, -5, 15)
                replacement.place(2, -40, -30, 0)
                replacement.send()
            if ref_data["foul"] == PENALTY:
                if not ref_data["yellow"]:
                    replacement.place(0, -75, 0, 90)
                    replacement.place(1, 25, -5, 25)
                    replacement.place(2, -40, -30, 0)
                else:
                    replacement.place(0, -75, 0, 90)
                    replacement.place(1, 10, 30, 0)
                    replacement.place(2, 20, -30, 0)
                replacement.send()

            actuator.stop()

        else:
            # halt behavior
            actuator.stop()
