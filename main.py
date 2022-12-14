import sys

from Controllers.MatchParameters import MatchParameters
from Strategies.MainStrategy import Strategy

from bridge import (Actuator, Replacer, Vision, Referee)

if __name__ == "__main__":

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

        # ref_data["game_on"] = True

        if ref_data["game_on"]:
            objectives = Strategy(teamsParameters, "default").main_strategy()
            actuator.send_all(teamsParameters.controller(teamsParameters.yellowRobotValues
                                                         if teamsParameters.isYellowTeam
                                                         else teamsParameters.blueRobotValues,
                                                         objectives))

        elif ref_data["foul"] != 7:
            # foul behaviour
            actuator.stop()

        else:
            # halt behavior
            actuator.stop()
