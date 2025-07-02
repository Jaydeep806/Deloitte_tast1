#Import the necessary modules(labraries)
import json, unittest, datetime

#use the open function to open read the three Json files

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)

#Convert Json data from format 1 to a unified format

def convertFromFormat1 (jsonObject):
#Spli the'location' field using the '/' as the delimiter
    locationParts=jsonObject['location']. split('/')
#Create a dictionary for the unified format
    result= {
        'deviceID': jsonObject['deviceID'],#Extract deviveID
        'deviceType': jsonObject['deviceType'],#Extract deviceType
        'timestamp': jsonObject['timestamp'], #Extract timestamp
        'location': {
            'country': locationParts[0],#Extract the country from location
            'city': locationParts[1], #Extract the city from location
            'area': locationParts[2],#Extract the area from location
            'factory': locationParts[3],#Extract the factory from location
            'section': locationParts[4]#Extract the section from location
        },
        'data': {
            'status': jsonObject['operationStatus'], # copy the opertaionStatus as status
            'temperature': jsonObject['temp'] #copy the temp as temperature
        }
    }

    return result

#Convert Json data from format 2 to the unified format
def convertFromFormat2 (jsonObject):
    #Convert the ISO timestamp to milliseconds since epoch
    date= datetime.datetime.strptime(jsonObject['timestamp'],#Extract the ISO timestamp
                                     '%Y-%m-%dT%H:%M:%S.%fZ')#ISO timestamp format
    timestamp=round((date-datetime.datetime(1970, 1, 1)).total_seconds()*1000)# convert to milliseconds

    #create a dictionary in the unified format
    result= {
        'deviceID': jsonObject['device']['id'],#Extract devive id
        'deviceType': jsonObject['device']['type'],#Extract device type
        'timestamp': timestamp, #copy the  converted timestamp
        'location': {
            'country': jsonObject['country'],#Extract country
            'city': jsonObject['city'], #Extract city
            'area': jsonObject['area'],#Extract area
            'factory': jsonObject['factory'],#Extract factory
            'section': jsonObject['section']#Extract section
        },
        'data': jsonObject['data'] #copy the entire 'data' field
    }
    return result

#main function to choose conversion method based on the Json data
def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject) #Convert from format 1
    else:
        result = convertFromFormat2(jsonObject) #Convert fro format 2

    return result

#Test cases using unitest
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        #Convert Json data to python objects using json.loads and checks if they match

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):
        #Convert the Json data from format 1 to unified formatand compare the to the expected result

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):
        # Convert the Json data from format 1 to unified formatand compare the to the expected result

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    #run the unitest
    unittest.main()
