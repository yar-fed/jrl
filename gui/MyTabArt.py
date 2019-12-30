import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui.aui_constants import *
from wx.lib.agw.aui.aui_utilities import BitmapFromBits, StepColour, IndentPressedBitmap, ChopText
from wx.lib.agw.aui.aui_utilities import GetBaseColour, DrawMACCloseButton, LightColour, TakeScreenShot
from wx.lib.agw.aui.aui_utilities import CopyAttributes
from wx.lib.agw.aui.tabart import AuiCommandCapture
from wx.lib.agw.aui.tabart import AuiDefaultTabArt

class VC71TabArt(AuiDefaultTabArt):
    """ A class to draw tabs using the Visual Studio 2003 (VC71) style. """

    def __init__(self):
        """ Default class constructor. """

        AuiDefaultTabArt.__init__(self)
        butBitmap = wx.Bitmap()
        butBitmap.LoadFile("assets/close.png")
        butBitmap_h = wx.Bitmap()
        butBitmap_h.LoadFile("assets/close_hover.png")
        if wx.Platform != "__WXMAC__":
            self._active_close_bmp = butBitmap
            self._disabled_close_bmp = butBitmap
            self._hover_close_bmp = butBitmap_h

        self.vertical_border_padding = 0
        self._selected_font = self._normal_font


    def Clone(self):
        """ Clones the art object. """

        art = type(self)()
        art.SetNormalFont(self.GetNormalFont())
        art.SetSelectedFont(self.GetSelectedFont())
        art.SetMeasuringFont(self.GetMeasuringFont())

        art = CopyAttributes(art, self)
        return art


    def DrawTab(self, dc, wnd, page, in_rect, close_button_state, paint_control=False):
        """
        Draws a single tab.
        :param `dc`: a :class:`wx.DC` device context;
        :param `wnd`: a :class:`wx.Window` instance object;
        :param `page`: the tab control page associated with the tab;
        :param wx.Rect `in_rect`: rectangle the tab should be confined to;
        :param integer `close_button_state`: the state of the close button on the tab;
        :param bool `paint_control`: whether to draw the control inside a tab (if any) on a :class:`MemoryDC`.
        """

        # Visual studio 7.1 style
        # This code is based on the renderer included in FlatNotebook

        # figure out the size of the tab

        control = page.control
        if close_button_state==aui.AUI_BUTTON_STATE_HIDDEN:
            close_button_state = aui.AUI_BUTTON_STATE_NORMAL
        tab_size, x_extent = self.GetTabSize(dc, wnd, page.caption, page.bitmap, False,#page.active,
                                             close_button_state, control)

        # tab_size = list(tab_size)
        # tab_size[0] -= 2
        tab_height = self._tab_ctrl_height
        tab_width = tab_size[0]
        tab_x = in_rect.x
        tab_y = in_rect.y + in_rect.height - tab_height
        clip_width = tab_width

        if tab_x + clip_width > in_rect.x + in_rect.width - 4:
            clip_width = (in_rect.x + in_rect.width) - tab_x - 4

        dc.SetClippingRegion(tab_x, tab_y, clip_width + 1, tab_height - 3)   ###### + "+5"
        agwFlags = self.GetAGWFlags()

        if agwFlags & AUI_NB_BOTTOM:
            tab_y -= 1

        dc.SetPen((page.active and [wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHIGHLIGHT))] or \
                   [wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW))])[0])
        dc.SetBrush((page.active and [wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))] or \
                     [wx.TRANSPARENT_BRUSH])[0])

        if page.active:
            tabH = tab_height - 2
            dc.DrawRectangle(tab_x, tab_y, tab_width, tabH)   ######## + "-5"

            rightLineY1 = (agwFlags & AUI_NB_BOTTOM and [self.vertical_border_padding - 2] or \
                           [self.vertical_border_padding - 1])[0]
            rightLineY2 = tabH
            dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)))
            # dc.DrawLine(tab_x + tab_width - 1, rightLineY1+2, tab_x + tab_width - 1, rightLineY2)

            if agwFlags & AUI_NB_BOTTOM:
                dc.DrawLine(tab_x + 1, rightLineY2 - 3 , tab_x + tab_width - 1, rightLineY2 - 3)

            dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW)))
            # dc.DrawLine(tab_x + tab_width, rightLineY1, tab_x + tab_width, rightLineY2)

            if agwFlags & AUI_NB_BOTTOM:
                dc.DrawLine(tab_x, rightLineY2 - 2, tab_x + tab_width, rightLineY2 - 2)

        else:

            # We dont draw a rectangle for non selected tabs, but only
            # vertical line on the right
            blackLineY1 = (agwFlags & AUI_NB_BOTTOM and [self.vertical_border_padding + 2] or \
                           [self.vertical_border_padding + 1])[0]
            blackLineY2 = tab_height - 5
            dc.DrawLine(tab_x + tab_width, blackLineY1, tab_x + tab_width, blackLineY2)

        border_points = [0, 0]

        if agwFlags & AUI_NB_BOTTOM:

            border_points[0] = wx.Point(tab_x, tab_y)
            border_points[1] = wx.Point(tab_x, tab_y + tab_height - 6) ####

        else: # if (agwFlags & AUI_NB_TOP)

            border_points[0] = wx.Point(tab_x, tab_y + tab_height - 4)
            border_points[1] = wx.Point(tab_x, tab_y + 2)

        drawn_tab_yoff = border_points[1].y
        drawn_tab_height = border_points[0].y - border_points[1].y

        text_offset = tab_x + 8
        close_button_width = 0

        if close_button_state != AUI_BUTTON_STATE_HIDDEN:
            close_button_width = self._active_close_bmp.GetWidth()
            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT:
                text_offset += close_button_width - 5

        if not page.enabled:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
            pagebitmap = page.dis_bitmap
        else:
            dc.SetTextForeground(page.text_colour)
            pagebitmap = page.bitmap

        shift = 0
        if agwFlags & AUI_NB_BOTTOM:
            shift = (page.active and [1] or [2])[0]

        bitmap_offset = 0
        if pagebitmap.IsOk():
            bitmap_offset = tab_x + 8
            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT and close_button_width:
                bitmap_offset += close_button_width - 5

            # draw bitmap
            dc.DrawBitmap(pagebitmap, bitmap_offset,
                          drawn_tab_yoff + (drawn_tab_height/2) - (pagebitmap.GetHeight()/2) + shift,
                          True)

            text_offset = bitmap_offset + pagebitmap.GetWidth()
            text_offset += 3 # bitmap padding

        else:
            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT == 0 or not close_button_width:
                text_offset = tab_x + 8

        # if the caption is empty, measure some temporary text
        caption = page.caption

        if caption == "":
            caption = "Xj"

        if page.active:
            dc.SetFont(self._normal_font)
            textx, texty, dummy = dc.GetFullMultiLineTextExtent(caption)
        else:
            dc.SetFont(self._normal_font)
            textx, texty, dummy = dc.GetFullMultiLineTextExtent(caption)

        draw_text = ChopText(dc, caption, tab_width - (text_offset-tab_x) - close_button_width)

        ypos = drawn_tab_yoff + (drawn_tab_height)/2 - (texty/2) - 1 + shift

        offset_focus = text_offset

        if control:
            if control.GetPosition() != wx.Point(text_offset+1, ypos):
                control.SetPosition(wx.Point(text_offset+1, ypos))

            if not control.IsShown():
                control.Show()

            if paint_control:
                bmp = TakeScreenShot(control.GetScreenRect())
                dc.DrawBitmap(bmp, text_offset+1, ypos, True)

            controlW, controlH = control.GetSize()
            text_offset += controlW + 4
            textx += controlW + 4

        # draw tab text
        rectx, recty, dummy = dc.GetFullMultiLineTextExtent(draw_text)
        dc.DrawLabel(draw_text, wx.Rect(text_offset, ypos, rectx, recty))

        out_button_rect = wx.Rect()

        # draw focus rectangle
        if (agwFlags & AUI_NB_NO_TAB_FOCUS) == 0:
            self.DrawFocusRectangle(dc, page, wnd, draw_text, offset_focus, bitmap_offset, drawn_tab_yoff+shift,
                                    drawn_tab_height+shift, rectx, recty)

        # draw 'x' on tab (if enabled)
        if close_button_state != AUI_BUTTON_STATE_HIDDEN:
            close_button_width = self._active_close_bmp.GetWidth()

            bmp = self._disabled_close_bmp

            if close_button_state == AUI_BUTTON_STATE_HOVER:
                bmp = self._hover_close_bmp
            elif close_button_state == AUI_BUTTON_STATE_PRESSED:
                bmp = self._pressed_close_bmp

            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT:
                rect = wx.Rect(tab_x + 4,
                               drawn_tab_yoff + (drawn_tab_height / 2) - (bmp.GetHeight() / 2) + shift,
                               close_button_width, tab_height)
            else:
                rect = wx.Rect(tab_x + tab_width - close_button_width - 3,
                               drawn_tab_yoff + (drawn_tab_height / 2) - (bmp.GetHeight() / 2) + shift,
                               close_button_width, tab_height)

            # Indent the button if it is pressed down:
            rect = IndentPressedBitmap(rect, close_button_state)
            dc.DrawBitmap(bmp, rect.x-5, rect.y, True)

            out_button_rect = rect

        out_tab_rect = wx.Rect(tab_x, tab_y, tab_width, tab_height)
        dc.DestroyClippingRegion()

        return out_tab_rect, out_button_rect, x_extent
    
    def DrawBackground(self, dc, wnd, rect):
        """
        Draws the tab area background.
        :param `dc`: a :class:`wx.DC` device context;
        :param `wnd`: a :class:`wx.Window` instance object;
        :param wx.Rect `rect`: the tab control rectangle.
        """

        self._buttonRect = wx.Rect()

        # draw background
        agwFlags = self.GetAGWFlags()
        if agwFlags & AUI_NB_BOTTOM:
            r = wx.Rect(rect.x, rect.y, rect.width+2, rect.height)

        # TODO: else if (agwFlags & AUI_NB_LEFT)
        # TODO: else if (agwFlags & AUI_NB_RIGHT)
        else: #for AUI_NB_TOP
            r = wx.Rect(rect.x, rect.y, rect.width+2, rect.height-3)

        dc.GradientFillLinear(r, self._background_top_colour, self._background_top_colour, wx.ALL)

        # draw base lines

        dc.SetPen(self._border_pen)
        y = rect.GetHeight()
        w = rect.GetWidth()

        if agwFlags & AUI_NB_BOTTOM:
            dc.SetBrush(wx.Brush(self._background_bottom_colour))
            dc.DrawRectangle(-1, 0, w+2, 4)

        # TODO: else if (agwFlags & AUI_NB_LEFT)
        # TODO: else if (agwFlags & AUI_NB_RIGHT)

        else: # for AUI_NB_TOP
            dc.SetBrush(self._base_colour_brush)
            dc.DrawRectangle(-1, y-4, w+2, 4)

    def DrawFocusRectangle(self, dc, page, wnd, draw_text, text_offset, bitmap_offset, drawn_tab_yoff, drawn_tab_height, textx, texty):
        """
        Draws the focus rectangle on a tab.
        :param `dc`: a :class:`DC` device context;
        :param `page`: the page associated with the tab;
        :param `wnd`: a :class:`Window` instance object;
        :param string `draw_text`: the text that has been drawn on the tab;
        :param integer `text_offset`: the text offset on the tab;
        :param integer `bitmap_offset`: the bitmap offset on the tab;
        :param integer `drawn_tab_yoff`: the y offset of the tab text;
        :param integer `drawn_tab_height`: the height of the tab;
        :param integer `textx`: the x text extent;
        :param integer `texty`: the y text extent.
        """

        if self.GetAGWFlags() & AUI_NB_NO_TAB_FOCUS:
            return
        
        if page.active and wx.Window.FindFocus() == wnd:
        
            focusRectText = wx.Rect(text_offset, (drawn_tab_yoff + (drawn_tab_height)/2 - (texty/2)),
                                    textx, texty)

            if page.bitmap.IsOk():
                focusRectBitmap = wx.Rect(bitmap_offset, drawn_tab_yoff + (drawn_tab_height/2) - (page.bitmap.GetHeight()/2),
                                          page.bitmap.GetWidth(), page.bitmap.GetHeight())

            if page.bitmap.IsOk() and draw_text == "":
                focusRect = wx.Rect(*focusRectBitmap)
            elif not page.bitmap.IsOk() and draw_text != "":
                focusRect = wx.Rect(*focusRectText)
            elif page.bitmap.IsOk() and draw_text != "":
                focusRect = focusRectText.Union(focusRectBitmap)

            # focusRect.Inflate(2, 2)

            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(self._focusPen)
            # dc.DrawRoundedRectangleRect(focusRect, 2)
    
    