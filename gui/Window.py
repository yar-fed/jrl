import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui.auibook import AuiNotebook as JRLNotebook
import wx.richtext as rt
import wx.html2 as html

class Tab(wx.Panel):
    
    def __init__(self, parent : JRLNotebook):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=wx.Size(100,75))
        

        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetArtProvider(parent.GetParent().dockart)

        # self.dictwin = rt.RichTextCtrl(self, wx.ID_ANY, "CCC",
        #             style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|rt.RE_MULTILINE|rt.RE_READONLY)
        # self.dictwin.WriteText("sdfsd")
        self.dictwin = html.WebView.New(self)
        self.dictwin.SetPage("""<div class="article-main__body article-body" id="js-article-body">
                <p><ruby>星<rt>ほし</rt></ruby>の<ruby>研究<rt>けんきゅう</rt></ruby>をしている<ruby>人<rt>ひと</rt></ruby>などが<ruby>集<rt>あつ</rt></ruby>まる<span class='colorC'><ruby>国際<rt>こくさい</rt></ruby></span><span class='colorC'><ruby>天文学<rt>てんもんがく</rt></ruby></span><span class='colorC'><ruby>連合<rt>れんごう</rt></ruby></span>は、まだ<ruby>名前<rt>なまえ</rt></ruby>がない<ruby>星<rt>ほし</rt></ruby>の<ruby>名前<rt>なまえ</rt></ruby>を<ruby>世界<rt>せかい</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>たちに<ruby>考<rt>かんが</rt></ruby>えてもらうことにしました。</p>
<p><span class='colorL'><ruby>日本<rt>にっぽん</rt></ruby></span>では、<ruby>日本人<rt>にっぽんじん</rt></ruby>などが<ruby>見<rt>み</rt></ruby>つけた２つの<ruby>星<rt>ほし</rt></ruby>の<ruby>名前<rt>なまえ</rt></ruby>をみんなで<ruby>考<rt>かんが</rt></ruby>えることにしました。<ruby>集<rt>あつ</rt></ruby>まった１４００ぐらいの<ruby>名前<rt>なまえ</rt></ruby>の<ruby>中<rt>なか</rt></ruby>から、１つの<ruby>星<rt>ほし</rt></ruby>は「Ｋａｍｕｉ」に<ruby>決<rt>き</rt></ruby>まりました。<span class='colorL'><ruby>北海道<rt>ほっかいどう</rt></ruby></span>などに<ruby>昔<rt>むかし</rt></ruby>から<ruby>住<rt>す</rt></ruby>んでいるアイヌの<ruby>人<rt>ひと</rt></ruby>たちの<ruby>言葉<rt>ことば</rt></ruby>で「<a href='javascript:void(0)' class='dicWin' id='id-0000'><ruby><span class="under">神</span><rt>かみ</rt></ruby></a>」という<ruby>意味<rt>いみ</rt></ruby>です。もう１つの<ruby>星<rt>ほし</rt></ruby>は「Ｃｈｕｒａ」に<ruby>決<rt>き</rt></ruby>まりました。<span class='colorL'><ruby>沖縄<rt>おきなわ</rt></ruby></span>の<ruby>言葉<rt>ことば</rt></ruby>で「<ruby>美<rt>うつく</rt></ruby>しい」という<ruby>意味<rt>いみ</rt></ruby>です。これから<ruby>世界<rt>せかい</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>がこの<ruby>名前<rt>なまえ</rt></ruby>を<ruby>使<rt>つか</rt></ruby>います。</p>
<p><ruby>星<rt>ほし</rt></ruby>を<ruby>見<rt>み</rt></ruby>つけた<span class='colorC'><ruby>東京工業大学<rt>とうきょうこうぎょうだいがく</rt></ruby></span>の<span class='colorN'><ruby>佐藤<rt>さとう</rt></ruby></span><span class='colorN'><ruby>文衛<rt>ぶんえい</rt></ruby></span><ruby>先生<rt>せんせい</rt></ruby>は「とても<a href='javascript:void(0)' class='dicWin' id='id-0001'><span class="under">すてき</span></a>な<ruby>名前<rt>なまえ</rt></ruby>になってうれしいです。<ruby>美<rt>うつく</rt></ruby>しい<ruby>星<rt>ほし</rt></ruby>によく<ruby>合<rt>あ</rt></ruby>っていると<ruby>思<rt>おも</rt></ruby>います」と<ruby>話<rt>はな</rt></ruby>しました。</p>
<p></p>
<p></p>
            </div>""", "fff")
        self.rtc = rt.RichTextCtrl(self, wx.ID_ANY, "CCC",
                    style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|rt.RE_MULTILINE)
        self.Bind(rt.EVT_RICHTEXT_RETURN, self.OnAccelReturn, self.rtc)
        self._mgr.AddPane(self.rtc, aui.AuiPaneInfo().CenterPane())
        self._mgr.AddPane(self.dictwin, aui.AuiPaneInfo().CenterPane())
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.rtc.Bind(wx.EVT_TEXT_URL, self.OnURL)
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()

    def OnAccelReturn(self, event):
        if event.GetFlags() & rt.RICHTEXT_ALT_DOWN:
            print("OnAccelAltReturn")
            self.rtc.Remove(event.GetPosition(), event.GetPosition()+1)
            self.GetParent().GetParent().process(self.rtc)
        elif event.GetFlags() & rt.RICHTEXT_CTRL_DOWN:
            print("OnAccelCtrlReturn")
            self.rtc.Remove(event.GetPosition(), event.GetPosition()+1)
            self._mgr.ShowPane(self.rtc, False)
        elif event.GetFlags() & rt.RICHTEXT_SHIFT_DOWN:
            print("OnAccelShiftReturn")
            self.rtc.Remove(event.GetPosition(), event.GetPosition()+1)
            self.GetParent().GetParent().process(self.rtc)
    
    def OnURL(self, event):
        # self.GetCaret().GetSize()SetSize(0,0)
        self.dictwin.MoveEnd()
        self.dictwin.WriteText("sdfsd")
        print(event.GetString())



class MainFrame(wx.Frame):

    def __init__(self, parent, title, tabart, dockart):
        super(MainFrame, self).__init__(parent, title=title)
        self.tabart = tabart
        self.dockart = dockart.JRLDockart(self)
        self.initUI()
    
    def initUI(self):
        self._nb = JRLNotebook(self)
        self._nb.SetArtProvider(self.tabart)
        self._nb.GetAuiManager().SetArtProvider(self.dockart)
        
        btm = wx.Bitmap()
        btm.LoadFile("assets/close.png")
        plusButton_btm = wx.Bitmap()
        plusButton_btm.LoadFile("assets/tab_new.png")
        self._nb.AddPage(Tab(self._nb), caption="Что-то очень длинное", select=False, bitmap=btm)
        self._nb.AddPage(Tab(self._nb), caption="漢字できますか？", select=False)
        self._nb.AddPage(Tab(self._nb), caption="ハイ、デキマス", select=True)
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
        self._nb.AddPage(Tab(self._nb), "LOL", select=True)
    
    def process(self, textctrl : rt.RichTextCtrl):
        textctrl.Clear()
        for token in text.split():
            textctrl.BeginURL(token)
            textctrl.WriteText(token)
            textctrl.EndURL()
            textctrl.WriteText(" ")
        textctrl.Undo()