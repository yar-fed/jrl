import wx
import wx.lib.agw.aui as aui
import wx.html2 as html
from wx.lib.agw.aui.auibook import AuiNotebook as JRLNotebook
from .PageFactory import PageFactory

class Tab(wx.Panel):
    
    def __init__(self, parent : JRLNotebook, wid=wx.ID_ANY):
        wx.Panel.__init__(self, parent, wid)
        
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetMasterManager(self.GetParent().GetAuiManager())
        self._mgr.SetArtProvider(parent.GetParent().dockart)
        
        with open("/home/yaroslav/Documents/Git_Projects/JRL/gui/setuphoverlinks.js", mode="r") as js:
            self.script = js.read()
        self.pf = PageFactory()
        self._dictwin = html.WebView.New(self)
        self._dictwin.SetPage(self.pf.GetPage(),f"file:{self.GetId()}.html")
        self._dictwin.RunScript(self.script)
        
        self._tc = wx.TextCtrl(self, wx.ID_ANY, "CCC",
                    style=wx.TE_BESTWRAP|wx.NO_BORDER|wx.TE_MULTILINE)#|wx.TE_PROCESS_ENTER)
        
        self._mgr.AddPane(self._tc, aui.AuiPaneInfo().CenterPane())
        self._mgr.AddPane(self._dictwin, aui.AuiPaneInfo().CenterPane().Bottom())
        
        self._tc.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus, self._tc)
        self._tc.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus, self._tc)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnAccelReturnDown, self._tc)
        self._dictwin.Bind(html.EVT_WEBVIEW_LOADED, self.OnPageLoaded)
        self._dictwin.Bind(html.EVT_WEBVIEW_NAVIGATING, self.OnURLHoverStart)
        self._dictwin.Bind(html.EVT_WEBVIEW_NAVIGATING, self.OnURL)
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()

    def OnAccelReturnDown(self, event):
        if not ( event.GetKeyCode() == wx.WXK_RETURN and \
            (event.AltDown() or event.ControlDown() or event.ShiftDown()) ):
            print("skip")
            event.Skip()
            return
        self.OnAccelReturn(event)
        # self._tc.Remove(self._tc.GetInsertionPoint()-1, self._tc.GetInsertionPoint())
    def OnAccelReturn(self, event):
        if event.AltDown():
            print("OnAccelAltReturn")
            # self.process(self._tc)
        elif event.ControlDown():
            print("OnAccelCtrlReturn")
            self.OnKillFocus(event)
            self._dictwin.SetFocus()
        elif event.ShiftDown():
            print("OnAccelShiftReturn")
            # self.process(self._tc)
    
    def OnPageLoaded(self, event):
        self._dictwin.RunScript(self.script)

    def OnURL(self, event):
        url = event.GetURL()
        if "EVT/HOVER_EVENT_START/" in url:
            self.OnURLHoverStart(url)
            event.Veto()
        elif "EVT/HOVER_EVENT_END/" in url:
            self.OnURLHoverEnd(url)
            event.Veto()
        elif "file:" == url[:5]:
            self.OnURLClick(url)
            event.Veto()
        return

    def OnKillFocus(self, event):
        print("OnKillFocus")
        self._mgr.GetPaneByWidget(self._tc).Top()
        self._mgr.GetPaneByWidget(self._tc).BestSize2(800, 50)
        self._mgr.GetPaneByWidget(self._dictwin).Direction(aui.AUI_DOCK_CENTER)
        self._mgr.Update()
    
    def OnSetFocus(self, event):
        print("OnSetFocus")
        self._mgr.GetPaneByWidget(self._tc).CentrePane()
        self._mgr.GetPaneByWidget(self._dictwin).Bottom()
        self._mgr.Update()
    
    def OnURLClick(self, url):
        print("OnURLClick")
        self._dictwin.LoadURL("file:testframe.html")
    def OnURLHoverStart(self, url):
        print("OnURLHoverStart")
    def OnURLHoverEnd(self, url):
        print("OnURLHoverEnd")
    
    def process(self, textctrl : wx.TextCtrl):
        text = textctrl.GetValue()
        for token in text.split():
            textctrl.BeginURL(token)
            textctrl.WriteText(token)
            textctrl.EndURL()
            textctrl.WriteText(" ")
        textctrl.Undo()