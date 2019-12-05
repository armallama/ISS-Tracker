#Import the necessary libraries
import requests
import json
import time
import sys
import wx
from geopy.geocoders import Nominatim
from datetime import datetime

#Dictionary variable for inputting coordinates for ISS passtimes
parameters = {
	'lat': None,
	'lon': None,
	'alt': None
}

geolocator = Nominatim(user_agent="BBISS")

class MainMenu(wx.Frame):

	def __init__(self):
		super().__init__(parent=None, title = 'ISSpy')
		panel = wx.Panel(self)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		menu = wx.FlexGridSizer(2,2, 9, 25)

		self.loc_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE|wx.TE_READONLY)
		pass_text = wx.TextCtrl(panel)
		current_loc = wx.Button(panel, label="Current")
		pass_time = wx.Button(panel, label="Pass Times")

		menu.AddMany([(current_loc), (self.loc_text, 1, wx.EXPAND),
					  (pass_time), (pass_text, 1, wx.EXPAND)])

		menu.AddGrowableRow(0,0)
		menu.AddGrowableRow(1,0)
		menu.AddGrowableCol(1,0)

		current_loc.Bind(wx.EVT_BUTTON, self.locPrint)

		hbox.Add(menu, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
		panel.SetSizer(hbox)
		self.Show() 
		
	def locPrint(self, event):

		responseLoc = requests.get("http://api.open-notify.org/iss-now.json")

		current_time = datetime.fromtimestamp(responseLoc.json()['timestamp']).strftime("%x %X")
		current_lat = responseLoc.json()['iss_position']['latitude']
		current_lon = responseLoc.json()['iss_position']['longitude']

		geo_location = geolocator.reverse(current_lat + "," + current_lon, language = "en")

		if geo_location.raw == {'error': 'Unable to geocode'}:
			current_location = current_lat +" "+ current_lon +" "+current_time + "-- No Address"
		else:
			current_location = current_lat +" "+ current_lon +" "+current_time + "--" + geo_location.raw['display_name']

		self.loc_text.WriteText(current_location+"\n")


	def passPrint(self):

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
	app = wx.App()
	frame = MainMenu()
	app.MainLoop()


if __name__ == '__main__':
	main()




