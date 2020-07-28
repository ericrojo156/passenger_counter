import * as Immutable from "immutable";

export const configDataDefault = Immutable.Map<string, any>(
    {"isMaster": false, "otherDevicesOnLAN": [], "trackGPS": true, "allowedBoarding": ["IN", "OUT"], "dividerLine": {"equation": {"a": 1, "b": 0, "order": 1}, "onBoardingDirection": [1, 1]}}
)