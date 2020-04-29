import wx
import wx.lib.agw.aui as aui
import wx.html2 as html
from wx.lib.agw.aui.auibook import AuiNotebook as JRLNotebook
from .PageFactory import PageFactory
import urllib.parse 

class Tab(wx.Panel):
    
    def __init__(self, parent : JRLNotebook, wid=wx.NewId()):
        wx.Panel.__init__(self, parent, wid)
        
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetMasterManager(self.GetParent().GetAuiManager())
        self._mgr.SetArtProvider(parent.GetParent().dockart)
        
        self.pf = PageFactory(self)
        self._wordwin = html.WebView.New(self)
        self._dictwin = html.WebView.New(self)
        self._dictwin.SetPage(self.pf.GetPage(),f"file://{self.GetId()}/index.html")
        
        self._tc = wx.TextCtrl(self, wx.ID_ANY, "食べる漢字",
                    style=wx.TE_BESTWRAP|wx.NO_BORDER|wx.TE_MULTILINE)
        
        self._mgr.AddPane(self._tc, aui.AuiPaneInfo().CenterPane())
        self._mgr.AddPane(self._dictwin, aui.AuiPaneInfo().CenterPane().Bottom())
        self._mgr.AddPane(self._wordwin, aui.AuiPaneInfo().Hide())
        
        self._tc.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus, self._tc)
        self._tc.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus, self._tc)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnAccelReturnDown, self._tc)
        self._dictwin.Bind(html.EVT_WEBVIEW_NAVIGATING, self.OnURL)
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()

    def OnAccelReturnDown(self, event):
        if not ( event.GetKeyCode() == wx.WXK_RETURN and event.AltDown() ):
            event.Skip()
            return
        self.process(self._tc)
        self.OnKillFocus(event)
        self._dictwin.SetFocus()
    
    # def OnPageLoaded(self, event):
    #     self._dictwin.RunScript(self.script)

    def OnURL(self, event):
        url = event.GetURL()
        if f"file://{self.GetId()}/words/" in url:
            self.OnURLClick(url)
            event.Veto()
            return
        event.Allow()
        return

    def OnKillFocus(self, event):
        print("OnKillFocus")
        self._mgr.GetPaneByWidget(self._tc).Top()
        self._mgr.GetPaneByWidget(self._dictwin).Center()
        self._mgr.Update()
    
    def OnSetFocus(self, event):
        print("OnSetFocus")
        self._mgr.GetPaneByWidget(self._tc).Center()
        self._mgr.GetPaneByWidget(self._dictwin).Bottom()
        self._mgr.Update()
    
    def OnURLClick(self, url):
        pane = self._mgr.GetPaneByWidget(self._wordwin)
        if not pane.IsShown():
            pane.Left().MinSize2(400, 0).Show()
        self._mgr.Update()
        word = urllib.parse.unquote(url.rpartition("/")[-1])
        self._wordwin.SetPage(self.pf.GetPage(word, word, True), url)
    
    def process(self, textctrl : wx.TextCtrl):
        text = textctrl.GetValue()
        p = self.pf.GetPage(text=text)
        print(p)
        self._dictwin.SetPage(p,f"file://{self.GetId()}/index.html")
        