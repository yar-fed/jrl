from .Tab import *
import wx.lib.agw.aui.dockart as da

class MainFrame(wx.Frame):

    def __init__(self, parent, title, tabart):#, dockart):
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(800, 600))
        self.basecolor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        self.tabart = tabart
        self.dockart = da.AuiDefaultDockArt()
        self.dockart.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, aui.AUI_GRADIENT_NONE)
        self.dockart.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 3)
        self.dockart.SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)
        self.dockart.SetColor(aui.AUI_DOCKART_SASH_COLOUR, wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        # self.dockart.SetColor(aui.AUI_DOCKART_BORDER_COLOUR, wx.Colour(0,0,0,0))
        self.initUI()
    
    def initUI(self):
        self._nb = JRLNotebook(self)
        self._nb.SetArtProvider(self.tabart)
        self._nb.GetAuiManager().SetArtProvider(self.dockart)
        
        btm = wx.Bitmap()
        btm.LoadFile("assets/close.png")
        plusButton_btm = wx.Bitmap()
        plusButton_btm.LoadFile("assets/tab_new.png")
        self._nb.AddPage(Tab(self._nb, wx.NewIdRef()), caption="Что-то очень длинное", select=False, bitmap=btm)
        self._nb.AddPage(Tab(self._nb, wx.NewIdRef()), caption="漢字できますか？", select=False)
        self._nb.AddPage(Tab(self._nb, wx.NewIdRef()), caption="ハイ、デキマス", select=True)
        self._nb.AddTabAreaButton(wx.ID_ANY, wx.CENTER, normal_bitmap=plusButton_btm, name="Add")
        self._nb.Bind(aui.EVT_AUINOTEBOOK_BUTTON, self.OnAddButton)
        self._nb.Bind(aui.EVT_AUINOTEBOOK_BG_MIDDLE_UP, self.OnAddButton)


    def OnExit(self,event):
        self.Close(True)  # Close the frame.
    
    def OnAddButton(self, event):
        if event.GetInt() == aui.AUI_BUTTON_CLOSE:
            event.Skip()
            return
        tctrl = self._nb.FindWindow(event.GetId())
        page = tctrl.GetPage(tctrl.GetActivePage())
        self._nb.SetSelectionToPage(page)
        self._nb.AddPage(Tab(self._nb, wx.NewIdRef()), "LOL", select=True)
