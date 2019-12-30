import wx
import wx.lib.agw.aui as aui
import MyTabArt as mta
import wx.lib.agw.aui.aui_constants as aconst

class Tab(wx.Panel):
    
    def __init__(self, *args, buttonparent, **kw):
        super().__init__(*args, **kw)
        self.switchButton = wx.Button(buttonparent)

class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title)
        self.initUI()
    
    def initUI(self):
        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)
        self._nb = aui.auibook.AuiNotebook(self)
        custom_art = mta.VC71TabArt()

        custom_art.SetSelectedFont(custom_art.GetNormalFont())
        self._nb.SetArtProvider(custom_art)
        # create several text controls
        text3 = wx.TextCtrl(self._nb, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        text4 = wx.TextCtrl(self._nb, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        text5 = wx.TextCtrl(self._nb, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        text6 = wx.TextCtrl(self._nb, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        
        self._nb.AddPage(text3, "Что-то очень длинное", select=True)
        self._nb.AddPage(text4, "漢字できますか？", select=True)
        self._nb.AddPage(text5, "ハイ、デキマス", select=True)
        self._nb.AddPage(text6, "LOL", select=True)
        self._mgr.AddPane(self._nb, aui.AuiPaneInfo().CenterPane())
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
    
    def OnNewTab(self,e):
        newTab = Tab(buttonparent=self.tabSizer)
        self.tabs.append(newTab)


def main():
    app = wx.App()
    win = MainFrame(None, "JRL")
    win.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()