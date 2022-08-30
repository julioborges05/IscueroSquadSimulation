from bridge import (NUM_BOTS, Entity)


class Strategy:
    def main_strategy(self, teamsParameters):
        self.teamsParameters = teamsParameters


        """Sets all objetives to ball coordinates."""
        objectives = [Entity(index=i) for i in range(NUM_BOTS)]
        for obj in objectives:
            obj.x = self.teamsParameters.ballValues.x
            obj.y = self.teamsParameters.ballValues.y

        return objectives
