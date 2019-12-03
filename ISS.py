import requests
import json
import time
import sys
from geopy.geocoders import Nominatim
from datetime import datetime

parameters = {
    'lat': None,
    'lon': None,
	'alt': None
}

geolocator = Nominatim(user_agent="BBISS")

def locPrint():
	try:
		print("Press Ctrl-C to go back to the Main Menu")
		while True:
			responseLoc = requests.get("http://api.open-notify.org/iss-now.json")
			print(responseLoc.json()['iss_position']['latitude'],
				  responseLoc.json()['iss_position']['longitude'],
				  datetime.fromtimestamp(responseLoc.json()['timestamp']))
			time.sleep(5)
	except KeyboardInterrupt:
		main()


def passPrint():

	print("Example coordinates are latitude: 40.71, Longitude: -74 (New York City)")
	lat = input("Enter latitude: ")
	lon = input("Enter longitude: ")
	alt = input("Enter Altitude (meters): ")
	try:
		coordinates = geolocator.reverse(lat + "," + lon, language = "en")
	except:
		print('Something went wrong')
		main()

	print("\n" +coordinates.raw['display_name']+"\n")


	parameters = {'lat': float(lat), 'lon': float(lon), 'alt': float(alt)}


	responsePass = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
	passTimes = responsePass.json()['response']
	for x in passTimes:
		time = datetime.fromtimestamp(x['risetime'])
		duration = x['duration']
		print(time, duration)


def main():
	while True:
		print("\nWelcome to the ISS tracker!")
		print("\nPick a # to do the following:")
		print("1. Check current location of the ISS")
		print("2. Check the next 5 passtimes of the ISS")
		print("3. Exit")
		userInput = input("Value: ")

		if userInput == '1':
			locPrint()
		elif userInput == '2':
			passPrint()
		elif userInput == '3':
			print("Good Bye!")
			time.sleep(3)
			sys.exit()
		else:
			print("\nSorry! Pick a number from the menu!\n\n")



if __name__ == '__main__':
	main()




