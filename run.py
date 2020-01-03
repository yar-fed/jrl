#!./python3env/bin/python3
import wx
import gui.MyTabArt
import gui.MyDockArt
import gui.Window
import json

def main():
    json
    app = wx.App()
    tabart = gui.MyTabArt.JRLTabArt()
    tabart.SetSelectedFont(tabart.GetNormalFont())
    dockart = gui.MyDockArt
    win = gui.Window.MainFrame(None, "JRL", tabart=tabart, dockart=dockart)
    win.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
