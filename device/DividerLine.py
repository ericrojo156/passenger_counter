import json

# represents the divider line used as the threshold in the computer vision module, to detect onboarding or outboarding passenger events
class DividerLine:
    def __init__(self, serialized):
        if (len(serialized) == 0):
            raise Exception("Failed to load serialized data for the divider line from the device configuration file.")
        line_dict = json.loads(serialized)
        self.onboarding_direction_vector = self.getOnBoardingDirection(line_dict)
        line_equation = self.getLineEquation(line_dict)
        self.slope = line_equation.get("a", 1)
        self.intercept = line_equation.get("b", 0)
        self.order = line_equation.get("order", 1)

    def getOnBoardingDirection(self, line_dict):
        onboarding_direction_vector = line_dict.get("onBoardingDirection", [1, 1])
        return onboarding_direction_vector

    def getLineEquation(self, line_dict):
        return line_dict.get("equation")