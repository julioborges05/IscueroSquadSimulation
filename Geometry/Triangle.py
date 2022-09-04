from math import atan

class Triangle:
    def __init__(self, horizontalValue, verticalValue):
        self.horizontalValue = horizontalValue
        self.verticalValue = verticalValue
        self.verticalHypotenuseAngle = atan(horizontalValue / verticalValue)

    def thalesTheoremVerticalValue(self, horizontalValue):
        return (horizontalValue * self.verticalValue) / self.horizontalValue
