import wx

class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title = 'ISSpy')
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        menu = wx.FlexGridSizer(2,2, 9, 25)

        loc_text = wx.TextCtrl(panel)
        pass_text = wx.TextCtrl(panel)
        current_loc = wx.Button(panel, label="Current")
        pass_time = wx.Button(panel, label="Pass Times")

        menu.AddMany([(current_loc), (loc_text, 1, wx.EXPAND),
                      (pass_time), (pass_text, 1, wx.EXPAND)])

        menu.AddGrowableRow(0,0)
        menu.AddGrowableRow(1,0)
        menu.AddGrowableCol(1,0)

        

        
        hbox.Add(menu, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
        self.Show()





if __name__ == '__main__':
    app = wx.App()
    fram = MyFrame()
    app.MainLoop()
