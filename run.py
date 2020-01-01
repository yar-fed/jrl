#!./python3env/bin/python3
import wx
import gui.MyTabArt
import gui.Window

def main():
    app = wx.App()
    art = gui.MyTabArt.JRLTabArt()
    art.SetSelectedFont(art.GetNormalFont())
    win = gui.Window.MainFrame(None, "JRL", art=art)
    win.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
