import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui.auibook import AuiNotebook as JRLNotebook
import wx.lib.agw.aui.aui_constants as aconst
import wx.richtext as rt

class Tab(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=wx.Size(100,75))
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.rtc = rt.RichTextCtrl(self, wx.ID_ANY, "CCC",
                    style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|rt.RE_MULTILINE)
        self._mgr.AddPane(self.rtc, aui.AuiPaneInfo().CenterPane())
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # self.sizer = wx.FlexGridSizer(1,0,0)
        # self.sizer.Add(self.rtc)
        # self.SetAutoLayout(True)
        # self.SetSizerAndFit(self.sizer)
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()


class MainFrame(wx.Frame):

    def __init__(self, parent, title, art):
        super(MainFrame, self).__init__(parent, title=title)
        self.art = art
        self.initUI()
    
    def initUI(self):
        self._nb = JRLNotebook(self)
        self._nb.SetArtProvider(self.art)

        # create several text controls
        # text3 = wx.TextCtrl(self._nb, wx.ID_ANY, "Main content window",
        #                     wx.DefaultPosition, wx.Size(200,150),
        #                     wx.NO_BORDER | wx.TE_MULTILINE)
        # text4 = wx.TextCtrl(self._nb, wx.ID_ANY, "Main content window",
        #                     wx.DefaultPosition, wx.Size(200,150),
        #                     wx.NO_BORDER | wx.TE_MULTILINE)
        # text5 = wx.TextCtrl(self._nb, wx.ID_ANY, "Main content window",
        #                     wx.DefaultPosition, wx.Size(200,150),
        #                     wx.NO_BORDER | wx.TE_MULTILINE)
        
        btm = wx.Bitmap()
        btm.LoadFile("assets/close.png")
        plusButton_btm = wx.Bitmap()
        plusButton_btm.LoadFile("assets/tab_new.png")
        self._nb.AddPage(Tab(self._nb), caption="Что-то очень длинное", select=False, bitmap=btm)
        self._nb.AddPage(Tab(self._nb), caption="漢字できますか？", select=False)
        self._nb.AddPage(Tab(self._nb), caption="ハイ、デキマス", select=True)
        self._nb.AddTabAreaButton(wx.ID_ANY, wx.CENTER, normal_bitmap=plusButton_btm, name="Add")
        self._nb.Bind(aui.EVT_AUINOTEBOOK_BUTTON, self.OnAddButton)

        # self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnExit(self,event):
        self.Close(True)  # Close the frame.
    
    def OnNewTab(self,event):
        newTab = Tab(buttonparent=self.tabSizer)
        self.tabs.append(newTab)

    def OnAddButton(self, event):
        if event.GetInt() == aui.AUI_BUTTON_CLOSE:
            event.Skip()
            return

        tctrl = self._nb.FindWindow(event.GetId())
        page = tctrl.GetPage(tctrl.GetActivePage())
        self._nb.SetSelectionToPage(page)
        self._nb.AddPage(wx.TextCtrl(self._nb, wx.ID_ANY, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE), "LOL", select=True)