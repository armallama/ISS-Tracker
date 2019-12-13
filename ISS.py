#Import the necessary libraries
import requests
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


passTimeLog = [] #List variable for adding the passtimes

geolocator = Nominatim(user_agent="BBISS") #geolocator accessing class Nominatim for location support

class MainMenu(wx.Frame):


    #Main Menu GUI setup
    def __init__(self):
        super(MainMenu, self).__init__(parent=None, title = 'ISSpy', size=(750,400))
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        menu = wx.FlexGridSizer(2,2, 9, 25)

        self.loc_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE|wx.TE_READONLY) 
        self.pass_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE|wx.TE_READONLY)
        current_loc = wx.Button(panel, label="Current Location")
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

    #Define the output for current location    
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

    #Define the output for next passtimes
    def passPrint(self, event):
        PassTimeDialog(self).ShowModal()
        for x in range(len(passTimeLog)):
            self.pass_text.WriteText(passTimeLog[x]+"\n")
        passTimeLog.clear()


#Dialog GUI for entering coordinates for passtinmes
class PassTimeDialog(wx.Dialog):

    #Menu setup
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

    #If cancel is pressed
    def onCancel(self, event):
        self.Destroy()
    
    #If coordinates are entered
    def onOk(self, event):
        if self.latitude.GetValue() == "" and self.longitude.GetValue() == "":
            passTimeLog.append("No entry\n")
        elif float(self.latitude.GetValue()) > 90 or float(self.latitude.GetValue()) < -90:
            passTimeLog.append("Enter the latitude between -90 and 90\n")
        elif float(self.longitude.GetValue()) > 180 or float(self.longitude.GetValue()) < -180:
            passTimeLog.append("Enter the longitude between -180 and 180\n")
        else:
            try:
                parameters = {'lat': float(self.latitude.GetValue()), 'lon': float(self.longitude.GetValue()), 'alt': float(self.altitude.GetValue())}
                passCoordinates = geolocator.reverse(self.latitude.GetValue() + "," + self.longitude.GetValue(), language = "en")

                responsePass = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

                if passCoordinates.raw != {'error': 'Unable to geocode'}:
                    passTimeLog.append(passCoordinates.raw['display_name']+"\n")
                else:
                    passTimeLog.append("No Address \n")

                passTimes = responsePass.json()['response']
                for x in passTimes:
                    time = datetime.fromtimestamp(x['risetime']).strftime("%x %X")
                    duration = str(x['duration'])
                    passTimeLog.append(time+" "+duration+" Seconds")
            except:
                passTimeLog.append("The ISS does not pass through this coordinate")
        self.Destroy()


def main():
    app = wx.App()
    MainMenu()
    app.MainLoop()


if __name__ == '__main__':
    main()




