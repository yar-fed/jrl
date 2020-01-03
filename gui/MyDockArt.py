from wx.lib.agw.aui.dockart import ModernDockArt
import wx
from wx.lib.agw.aui.aui_constants import AUI_DOCKART_PANE_BORDER_SIZE

class JRLDockart(ModernDockArt):
    def __init__(self, win):
        """ Default class constructor. """

        ModernDockArt.__init__(self, win)

        self.Init()

    def Init(self):
        """ Initializes the dock art. """

        ModernDockArt.Init(self)

    def DrawSashGripper(self, dc, orient, rect):
        """
        Draws a sash gripper on a sash between two windows.

        :param `dc`: a :class:`wx.DC` device context;
        :param integer `orient`: the sash orientation;
        :param wx.Rect `rect`: the sash rectangle.
        """

        dc.SetBrush(self._gripper_brush)
        print("SSSS")
        if orient == wx.HORIZONTAL:  # horizontal sash

            x = rect.x + int((1.0/4.0)*rect.width)
            xend = rect.x + int((3.0/4.0)*rect.width)
            y = rect.y + (rect.height//2) - 1

            while 1:
                # dc.SetPen(self._gripper_pen3)
                dc.SetPen( wx.TRANSPARENT_PEN ) 
                dc.DrawRectangle(x, y, 2, 2)
                # dc.SetPen(self._gripper_pen2)
                dc.SetPen( wx.TRANSPARENT_PEN ) 
                dc.DrawPoint(x+1, y+1)
                x = x + 5

                if x >= xend:
                    break

        else:

            y = rect.y + int((1.0/4.0)*rect.height)
            yend = rect.y + int((3.0/4.0)*rect.height)
            x = rect.x + (rect.width//2) - 1

            while 1:
                # dc.SetPen(self._gripper_pen3)
                dc.SetPen( wx.TRANSPARENT_PEN ) 
                dc.DrawRectangle(x, y, 2, 2)
                # dc.SetPen(self._gripper_pen2)
                dc.SetPen( wx.TRANSPARENT_PEN ) 
                dc.DrawPoint(x+1, y+1)
                y = y + 5

                if y >= yend:
                    break
    
    def DrawGripper(self, dc, window, rect, pane):
        """
        Draws a gripper on the pane.

        :param `dc`: a :class:`wx.DC` device context;
        :param `window`: an instance of :class:`wx.Window`;
        :param wx.Rect `rect`: the pane caption rectangle;
        :param `pane`: the pane for which the gripper is drawn.
        """

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self._gripper_brush)
        print("ss")

        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

        if not pane.HasGripperTop():
            y = 4
            while 1:
                # dc.SetPen(self._gripper_pen1)
                dc.SetPen(wx.TRANSPARENT_PEN)
                dc.DrawPoint(rect.x+3, rect.y+y)
                # dc.SetPen(self._gripper_pen2)
                dc.DrawPoint(rect.x+3, rect.y+y+1)
                dc.DrawPoint(rect.x+4, rect.y+y)
                # dc.SetPen(self._gripper_pen3)
                dc.DrawPoint(rect.x+5, rect.y+y+1)
                dc.DrawPoint(rect.x+5, rect.y+y+2)
                dc.DrawPoint(rect.x+4, rect.y+y+2)
                y = y + 4
                if y > rect.GetHeight() - 4:
                    break
        else:
            x = 4
            while 1:
                # dc.SetPen(self._gripper_pen1)
                dc.SetPen(wx.TRANSPARENT_PEN)
                dc.DrawPoint(rect.x+x, rect.y+3)
                # dc.SetPen(self._gripper_pen2)
                dc.DrawPoint(rect.x+x+1, rect.y+3)
                dc.DrawPoint(rect.x+x, rect.y+4)
                # dc.SetPen(self._gripper_pen3)
                dc.DrawPoint(rect.x+x+1, rect.y+5)
                dc.DrawPoint(rect.x+x+2, rect.y+5)
                dc.DrawPoint(rect.x+x+2, rect.y+4)
                x = x + 4
                if x > rect.GetWidth() - 4:
                    break
    
    def DrawBorder(self, dc, window, rect, pane):
        """
        Draws the pane border.

        :param `dc`: a :class:`wx.DC` device context;
        :param `window`: an instance of :class:`wx.Window`;
        :param wx.Rect `rect`: the border rectangle;
        :param `pane`: the pane for which the border is drawn.
        """

        drect = wx.Rect(*rect)

        # dc.SetPen(self._border_pen)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        border_width = self.GetMetric(AUI_DOCKART_PANE_BORDER_SIZE)

        if pane.IsToolbar():

            for ii in range(0, border_width):

                dc.SetPen(wx.WHITE_PEN)
                dc.DrawLine(drect.x, drect.y, drect.x+drect.width, drect.y)
                dc.DrawLine(drect.x, drect.y, drect.x, drect.y+drect.height)
                dc.SetPen(self._border_pen)
                dc.DrawLine(drect.x, drect.y+drect.height-1,
                            drect.x+drect.width, drect.y+drect.height-1)
                dc.DrawLine(drect.x+drect.width-1, drect.y,
                            drect.x+drect.width-1, drect.y+drect.height)
                drect.Deflate(1, 1)

        else:

            for ii in range(0, border_width):

                dc.DrawRectangle(drect.x, drect.y, drect.width, drect.height)
                drect.Deflate(1, 1)