#!./python3env/bin/python3
import wx
import gui.JRLTabArt
import wx.lib.agw.aui.dockart as da
import gui.Window
import json, os

def main():
    os.environ["GDK_BACKEND"]="x11"
    app = wx.App()
    tabart = gui.JRLTabArt.JRLTabArt()
    tabart.SetSelectedFont(tabart.GetNormalFont())
    win = gui.Window.MainFrame(None, "JRL", tabart=tabart)
    win.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
