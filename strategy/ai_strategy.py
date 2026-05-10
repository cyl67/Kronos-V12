class PositionManager:

    def calc_position(self, confidence):

        if confidence > 0.8:
            return 1.0

        if confidence > 0.6:
            return 0.5

        return 0.2