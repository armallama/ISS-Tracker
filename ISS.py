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

passTimeLog = []
responsePass = None

geolocator = Nominatim(user_agent="BBISS")

class MainMenu(wx.Frame):

    def __init__(self):
        super(MainMenu, self).__init__(parent=None, title = 'ISSpy', size=(750,400))
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        menu = wx.FlexGridSizer(2,2, 9, 25)

        self.loc_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.pass_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE|wx.TE_READONLY)
        current_loc = wx.Button(panel, label="Current")
        pass_time = wx.Button(panel, label="Pass Times")

        menu.AddMany([(current_loc), (self.loc_text, 1, wx.EXPAND),
                      (pass_time), (self.pass_text, 1, wx.EXPAND)])

        menu.AddGrowableRow(0,0)
        menu.AddGrowableRow(1,0)
        menu.AddGrowableCol(1,0)

        
        current_loc.Bind(wx.EVT_BUTTON, self.locPrint)
        pass_time.Bind(wx.EVT_BUTTON, self.passPrint)

        hbox.Add(menu, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
        self.Show(True) 
        
    def locPrint(self, event):

        responseLoc = requests.get("http://api.open-notify.org/iss-now.json")

        current_time = datetime.fromtimestamp(responseLoc.json()['timestamp']).strftime("%x %X")
        current_lat = responseLoc.json()['iss_position']['latitude']
        current_lon = responseLoc.json()['iss_position']['longitude']

        geo_location = geolocator.reverse(current_lat + "," + current_lon, language = "en")

        if geo_location.raw == {'error': 'Unable to geocode'}:
            current_location = current_lat +" "+ current_lon +" "+current_time + "-- No Address"
        else:
            current_location = current_lat +" "+ current_lon +" "+current_time + "-- " + geo_location.raw['display_name']

        self.loc_text.WriteText(current_location+"\n")


    def passPrint(self, event):
        PassTimeDialog(self).ShowModal()
        for x in range(len(passTimeLog)):
            self.pass_text.WriteText(passTimeLog[x]+"\n")

        # print("Example coordinates are latitude: 40.71, Longitude: -74 (New York City)")
        # lat = input("Enter latitude: ")
        # lon = input("Enter longitude: ")
        # alt = input("Enter Altitude (meters): ")
        # try:
        # 	coordinates = geolocator.reverse(lat + "," + lon, language = "en")
        # except:
        # 	print('Something went wrong')
        # 	main()

        # print("\n" +coordinates.raw['display_name']+"\n")


        # parameters = {'lat': float(lat), 'lon': float(lon), 'alt': float(alt)}


        # responsePass = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
        # passTimes = responsePass.json()['response']
        # for x in passTimes:
        # 	time = datetime.fromtimestamp(x['risetime'])
        # 	duration = x['duration']
        # 	print(time, duration)


class PassTimeDialog(wx.Dialog):
    def __init__(self, parent):
        super(PassTimeDialog, self).__init__(parent, title = "Enter Coordinates", size = (250,250))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.latitude = wx.TextCtrl(panel)
        self.longitude = wx.TextCtrl(panel)
        self.altitude = wx.TextCtrl(panel)


        
        static_box = wx.StaticBox(panel, label = 'Coordinates')
        stat_els = wx.StaticBoxSizer(static_box, orient=wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label = 'Latitude'), wx.ALL)
        hbox1.Add(self.latitude, wx.ALL)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, label = 'Longitude'), wx.ALL)
        hbox2.Add(self.longitude, wx.ALL)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(panel, label = 'Altitude'), wx.ALL)
        hbox3.Add(self.altitude, wx.ALL)

        stat_els.Add(hbox1)
        stat_els.AddSpacer(10)
        stat_els.Add(hbox2)
        stat_els.AddSpacer(10)
        stat_els.Add(hbox3)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label = 'Ok')
        cancelButton = wx.Button(self, label = 'Cancel')
        hbox4.Add(okButton)
        hbox4.Add(cancelButton, flag = wx.LEFT, border =5)

        vbox.Add(panel, proportion = 1, flag=wx.ALL|wx.EXPAND,border =5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10)
        panel.SetSizer(stat_els)
        self.SetSizer(vbox)

        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
        okButton.Bind(wx.EVT_BUTTON, self.onOk)

    def onCancel(self, event):
        self.Destroy()
    
    def onOk(self, event):
        parameters = {'lat': float(self.latitude.GetValue()), 'lon': float(self.longitude.GetValue()), 'alt': float(self.altitude.GetValue())}
        passCoordinates = geolocator.reverse(self.latitude.GetValue() + "," + self.longitude.GetValue(), language = "en")

        responsePass = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

        passTimeLog.append(passCoordinates.raw['display_name']+"\n")

        passTimes = responsePass.json()['response']
        for x in passTimes:
            time = datetime.fromtimestamp(x['risetime']).strftime("%x %X")
            duration = str(x['duration'])
            passTimeLog.append(time+" "+duration+" Seconds")
        
        self.Destroy()


def main():
    app = wx.App()
    MainMenu()
    app.MainLoop()


if __name__ == '__main__':
    main()




