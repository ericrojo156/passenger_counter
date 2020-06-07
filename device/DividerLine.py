import json

# represents the divider line used as the threshold in the computer vision module, to detect onboarding or outboarding passenger events
class DividerLine:
    def __init__(self, serialized):
        if (len(serialized) == 0):
            raise Exception("Failed to load serialized data for the divider line from the device configuration file.")
        line_dict = json.loads(serialized)
        line_equation = self._getLineEquation(line_dict)

        self.onboarding_direction_vector = self._getOnBoardingDirection(line_dict)
        self.slope = line_equation.get("a", 1)
        self.intercept = line_equation.get("b", 0)
        self.order = line_equation.get("order", 1)

    def to_dict(self):
        return {
            "equation": {
                "a": self.slope,
                "b": self.intercept,
                "order": self.order
            },
            "onBoardingDirection": self.onboarding_direction_vector
        }

    def _getOnBoardingDirection(self, line_dict):
        onboarding_direction_vector = line_dict.get("onBoardingDirection", [1, 1])
        return onboarding_direction_vector

    def _getLineEquation(self, line_dict):
        return line_dict.get("equation")