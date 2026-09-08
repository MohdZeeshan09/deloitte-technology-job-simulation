# Import the necessary modules and libraries
import json
import unittest
import datetime


# Open and read the three JSON files using UTF-8 encoding
with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


# Convert JSON data from format 1 to the expected unified format
def convertFromFormat1(jsonObject):

    # Split the location into separate parts
    locationParts = jsonObject["location"].split("/")

    # Create a new dictionary in the unified format
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# Convert JSON data from format 2 to the expected unified format
def convertFromFormat2(jsonObject):

    # Convert ISO 8601 timestamp to milliseconds since epoch
    data = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    timestamp = round(
        (data - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    )

    # Create a new dictionary in the unified format
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": jsonObject["data"]
    }

    return result


# Main function
def main(jsonObject):

    result = {}

    # Format 1 does not have a "device" object
    if jsonObject.get("device") is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


# Test cases using unittest
class TestSolution(unittest.TestCase):

    # Sanity test
    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))

        self.assertEqual(
            result,
            jsonExpectedResult
        )


    # Test conversion from Format 1
    def test_dataType1(self):

        result = main(jsonData1)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 1 failed"
        )


    # Test conversion from Format 2
    def test_dataType2(self):

        result = main(jsonData2)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 2 failed"
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()