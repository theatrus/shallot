#----------------------------------------------------------------------
# A very simple wxPython example.  Just a wx.Frame, wx.Panel,
# wx.StaticText, wx.Button, and a wx.BoxSizer, but it shows the basic
# structure of any wxPython application.
#----------------------------------------------------------------------

import wx
import thread
import Pyro.core
import Pyro.naming
import time
import sys

class NSLocThread:
    def __init__(self, a):
        self.a = a

    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def isRunning(self):
        return self.running

    def Run(self):
        
        
        try:
            locator = Pyro.naming.NameServerLocator()
            self.a.NS = locator.getNS()
            self.a.Player = Pyro.core.getAttrProxyForURI(self.a.NS.resolve('player'))
            

            
            self.running = False
        except:
            self.a.NS = None
            self.running = False

class ShRemFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(350, 200),
                            style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)






        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_ABOUT, "&About", "Information")
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit ShallotRemote")
        
        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(panel, -1, "ShallotRemote 0.32")
        self.title = wx.StaticText(panel, -1, "Song title goes here")
        #text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        pause = wx.Button(panel, -1, "Pause")
        next = wx.Button(panel, -1, "Next")
        repeat = wx.Button(panel, -1, "Repeat")

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        self.Bind(wx.EVT_BUTTON, self.OnNext, next)
        self.Bind(wx.EVT_BUTTON, self.OnRepeat, repeat)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        size_but = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer.Add(text, 0, wx.ALL, 10)
        sizer.Add(self.title, 0, wx.ALL, 10)
        size_but.Add(pause, 0, wx.ALL)
        size_but.Add(next, 0, wx.ALL)
        size_but.Add(repeat, 0, wx.ALL)
        sizer.Add(size_but, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
        panel.Layout()

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self)
        self.timer.Start(500)



    def OnPause(self, evt):
        app.Player.pause()
        self.timer.Enable()
    def OnNext(self, evt):
        app.Player.next()
    def OnRepeat(self, evt):
        app.Player.repeat()
        
    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        
        self.Close()

    def OnFunButton(self, evt):
        """Event handler for the button click."""

    def OnTimer(self, evt):
        song = app.Player.current_song()
        self.title.SetLabel(song['artist'] + " - " + song['title'])
        
class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        #bmp = wx.StaticText(self, -1, "ShallotRemote 0.32")
        wx.SplashScreen.__init__(self, wx.EmptyBitmap(100,100,-1),
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 3, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        self.Hide()
        self.busy = wx.BusyInfo("One moment please, finding the Pyro nameserver...")
        wait = wx.BusyCursor()
        frame = ShRemFrame(None, "Shallot Remote")
        
        t = NSLocThread(app)
        t.Start()
        while t.isRunning():
            time.sleep(0.1)
            
        if app.NS is None:
            dlg = wx.MessageDialog(frame, "Couldn't find the Pyro name server. Quiting.",
                               'Error',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            sys.exit()
        
        
        app.SetTopWindow(frame)

        frame.Show(True)
     
        
        evt.Skip()  # Make sure the default handler runs too...

        

class ShRem(wx.App):
    def OnInit(self):
        
        
        a = MySplashScreen()
        a.Show()
        
      
        #print "Print statements go to this stdout window by default."

        wx.Yield()
        
 
        return True
        
Pyro.core.initClient(banner=0)        
app = ShRem(redirect=False)



app.MainLoop()

