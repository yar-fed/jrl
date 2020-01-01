import wx
from wx.lib.agw.aui.aui_constants import *
from wx.lib.agw.aui.auibook import AuiNotebook, AuiTabContainerButton, AuiTabCtrl, AuiTabContainer
wxEVT_COMMAND_AUINOTEBOOK_BUTTON = wx.NewEventType()
EVT_AUINOTEBOOK_BUTTON = wx.PyEventBinder(wxEVT_COMMAND_AUINOTEBOOK_BUTTON, 1)


class JRLNotebook(AuiNotebook):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=AUI_NB_DEFAULT_STYLE, name="AuiNotebook"):
        """
        Default class constructor.

        :param wx.Window `parent`: the :class:`AuiNotebook` parent;
        :param integer `id`: an identifier for the control: a value of -1 is taken to mean a default;
        :param wx.Point `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param wx.Size `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the underlying :class:`Panel` window style;
        :param integer `agwStyle`: the AGW-specific window style. This can be a combination of the following bits:

         ==================================== ==================================
         Flag name                            Description
         ==================================== ==================================
         ``AUI_NB_TOP``                       With this style, tabs are drawn along the top of the notebook
         ``AUI_NB_LEFT``                      With this style, tabs are drawn along the left of the notebook. Not implemented yet.
         ``AUI_NB_RIGHT``                     With this style, tabs are drawn along the right of the notebook. Not implemented yet.
         ``AUI_NB_BOTTOM``                    With this style, tabs are drawn along the bottom of the notebook
         ``AUI_NB_TAB_SPLIT``                 Allows the tab control to be split by dragging a tab
         ``AUI_NB_TAB_MOVE``                  Allows a tab to be moved horizontally by dragging
         ``AUI_NB_TAB_EXTERNAL_MOVE``         Allows a tab to be moved to another tab control
         ``AUI_NB_TAB_FIXED_WIDTH``           With this style, all tabs have the same width
         ``AUI_NB_SCROLL_BUTTONS``            With this style, left and right scroll buttons are displayed
         ``AUI_NB_WINDOWLIST_BUTTON``         With this style, a drop-down list of windows is available
         ``AUI_NB_CLOSE_BUTTON``              With this style, a close button is available on the tab bar
         ``AUI_NB_CLOSE_ON_ACTIVE_TAB``       With this style, a close button is available on the active tab
         ``AUI_NB_CLOSE_ON_ALL_TABS``         With this style, a close button is available on all tabs
         ``AUI_NB_MIDDLE_CLICK_CLOSE``        Allows to close :class:`AuiNotebook` tabs by mouse middle button click
         ``AUI_NB_SUB_NOTEBOOK``              This style is used by :class:`~wx.lib.agw.aui.framemanager.AuiManager` to create automatic AuiNotebooks
         ``AUI_NB_HIDE_ON_SINGLE_TAB``        Hides the tab window if only one tab is present
         ``AUI_NB_SMART_TABS``                Use Smart Tabbing, like ``Alt`` + ``Tab`` on Windows
         ``AUI_NB_USE_IMAGES_DROPDOWN``       Uses images on dropdown window list menu instead of check items
         ``AUI_NB_CLOSE_ON_TAB_LEFT``         Draws the tab close button on the left instead of on the right (a la Camino browser)
         ``AUI_NB_TAB_FLOAT``                 Allows the floating of single tabs. Known limitation: when the notebook is more or less full screen,
                                              tabs cannot be dragged far enough outside of the notebook to become floating pages
         ``AUI_NB_DRAW_DND_TAB``              Draws an image representation of a tab while dragging (on by default)
         ``AUI_NB_ORDER_BY_ACCESS``           Tab navigation order by last access time for the tabs
         ``AUI_NB_NO_TAB_FOCUS``              Don't draw tab focus rectangle
         ==================================== ==================================

         Default value for `agwStyle` is:
         ``AUI_NB_DEFAULT_STYLE`` = ``AUI_NB_TOP`` | ``AUI_NB_TAB_SPLIT`` | ``AUI_NB_TAB_MOVE`` | ``AUI_NB_SCROLL_BUTTONS`` | ``AUI_NB_CLOSE_ON_ACTIVE_TAB`` | ``AUI_NB_MIDDLE_CLICK_CLOSE`` | ``AUI_NB_DRAW_DND_TAB``

        :param string `name`: the window name.
        """

        self._curpage = -1
        self._tab_id_counter = AuiBaseTabCtrlId
        self._dummy_wnd = None
        self._hide_tabs = False
        self._sash_dclick_unsplit = False
        self._tab_ctrl_height = 20
        self._requested_bmp_size = wx.Size(-1, -1)
        self._requested_tabctrl_height = -1
        self._textCtrl = None
        self._tabBounds = (-1, -1)

        wx.Panel.__init__(self, parent, id, pos, size, style|wx.BORDER_NONE|wx.TAB_TRAVERSAL, name=name)
        from wx.lib.agw.aui import framemanager
        self._mgr = framemanager.AuiManager()
        self._tabs = JRLTabContainer(self)

        self.InitNotebook(agwStyle)

class JRLTabContainer(AuiTabCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER|wx.WANTS_CHARS|wx.TAB_TRAVERSAL):
        """
        Default class constructor.
        Used internally, do not call it in your code!

        :param `parent`: the :class:`AuiNotebook` parent;
        :param integer `id`: an identifier for the control: a value of -1 is taken to mean a default;
        :param wx.Point `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param wx.Size `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the window style.
        """

        wx.Control.__init__(self, parent, id, pos, size, style, name="AuiTabCtrl")
        AuiTabContainer.__init__(self, parent)

        self._click_pt = wx.Point(-1, -1)
        self._is_dragging = False
        self._hover_button = None
        self._pressed_button = None
        self._drag_image = None
        self._drag_img_offset = (0, 0)
        self._on_button = False
        self._tooltip_timer = None
        self._tooltip_wnd = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnCaptureLost)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(EVT_AUINOTEBOOK_BUTTON, self.OnButton)

    def Render(self, raw_dc, wnd):
        """
        Renders the tab catalog to the specified :class:`wx.DC`.

        It is a virtual function and can be overridden to provide custom drawing
        capabilities.

        :param `raw_dc`: a :class:`wx.DC` device context;
        :param `wnd`: an instance of :class:`wx.Window`.
        """

        if not raw_dc or not raw_dc.IsOk():
            return

        dc = wx.MemoryDC()
        
        # use the same layout direction as the window DC uses to ensure that the
        # text is rendered correctly
        dc.SetLayoutDirection(raw_dc.GetLayoutDirection())

        page_count = len(self._pages)
        button_count = len(self._buttons)

        # create off-screen bitmap
        bmp = wx.Bitmap(self._rect.GetWidth(), self._rect.GetHeight())
        dc.SelectObject(bmp)

        if not dc.IsOk():
            return

        # prepare the tab-close-button array
        # make sure tab button entries which aren't used are marked as hidden
        for i in range(page_count, len(self._tab_close_buttons)):
            self._tab_close_buttons[i].cur_state = AUI_BUTTON_STATE_HIDDEN

        # make sure there are enough tab button entries to accommodate all tabs
        while len(self._tab_close_buttons) < page_count:
            tempbtn = AuiTabContainerButton()
            tempbtn.id = AUI_BUTTON_CLOSE
            tempbtn.location = wx.CENTER
            tempbtn.cur_state = AUI_BUTTON_STATE_HIDDEN
            self._tab_close_buttons.append(tempbtn)

        # find out if size of tabs is larger than can be
        # afforded on screen
        total_width = visible_width = 0
        tab_width = [0] * page_count

        for i in range(page_count):
            page = self._pages[i]

            if page.hidden:
                continue

            # determine if a close button is on this tab
            close_button = False
            if (self._agwFlags & AUI_NB_CLOSE_ON_ALL_TABS and page.hasCloseButton) or \
               (self._agwFlags & AUI_NB_CLOSE_ON_ACTIVE_TAB and page.active and page.hasCloseButton):

                close_button = True

            control = page.control
            if control:
                try:
                    control.GetSize()
                except RuntimeError:
                    page.control = None

            size, x_extent = self._art.GetTabSize(dc, wnd, page.caption, page.bitmap, page.active,
                                                  (close_button and [AUI_BUTTON_STATE_NORMAL] or \
                                                   [AUI_BUTTON_STATE_HIDDEN])[0], page.control)

            if i+1 < page_count:
                total_width += x_extent
                tab_width[i] = x_extent
            else:
                total_width += size[0]
                tab_width[i] = size[0]

            if i >= self._tab_offset:
                if i+1 < page_count:
                    visible_width += x_extent
                else:
                    visible_width += size[0]

        # Calculate the width of visible buttons
        buttons_width = 0

        for button in self._buttons:
            if not (button.cur_state & AUI_BUTTON_STATE_HIDDEN):
                buttons_width += button.rect.GetWidth()

        total_width += buttons_width

        if (total_width > self._rect.GetWidth() and page_count > 1) or self._tab_offset != 0:

            # show left/right buttons
            for button in self._buttons:
                if button.id == AUI_BUTTON_LEFT or \
                   button.id == AUI_BUTTON_RIGHT:

                    button.cur_state &= ~AUI_BUTTON_STATE_HIDDEN

        else:

            # hide left/right buttons
            for button in self._buttons:
                if button.id == AUI_BUTTON_LEFT or \
                   button.id == AUI_BUTTON_RIGHT:

                    button.cur_state |= AUI_BUTTON_STATE_HIDDEN

        # Re-calculate the width of visible buttons (may have been hidden/shown)
        buttons_width = 0
        for button in self._buttons:
            if not (button.cur_state & AUI_BUTTON_STATE_HIDDEN):
                buttons_width += button.rect.GetWidth()

        # Shift the tab offset down to make use of available space
        available_width = self._rect.GetWidth() - buttons_width
        while self._tab_offset > 0 and visible_width + tab_width[self._tab_offset - 1] < available_width:
            self._tab_offset -= 1
            visible_width += tab_width[self._tab_offset]

        # determine whether left button should be enabled

        # draw background
        self._art.DrawBackground(dc, wnd, self._rect)

        # draw buttons
        right_buttons_width = 0

        # draw the buttons on the right side
        # offset = self._rect.x + self._rect.width

        offset = 0

        # draw the buttons on the left side
        

        # buttons before the tab offset must be set to hidden
        for i in range(self._tab_offset):
            self._tab_close_buttons[i].cur_state = AUI_BUTTON_STATE_HIDDEN
            if self._pages[i].control:
                if self._pages[i].control.IsShown():
                    self._pages[i].control.Hide()

        # draw tab before tab offset
        if self._tab_offset > 0:
            page = self._pages[self._tab_offset - 1]
            tab_button = self._tab_close_buttons[self._tab_offset - 1]
            size, x_extent = self._art.GetTabSize(dc, wnd, page.caption, page.bitmap, page.active, tab_button.cur_state, page.control)

            rect = wx.Rect(offset - x_extent, 0, self._rect.width - right_buttons_width - offset - x_extent - 2, self._rect.height)
            clip_rect = wx.Rect(*self._rect)
            clip_rect.x = offset

            dc.SetClippingRegion(clip_rect)
            self._art.DrawTab(dc, wnd, page, rect, tab_button.cur_state)
            dc.DestroyClippingRegion()

        # draw the tabs
        active = 999
        active_offset = 0

        rect = wx.Rect(*self._rect)
        rect.y = 0
        rect.height = self._rect.height

        for i in range(self._tab_offset, page_count):

            page = self._pages[i]

            if page.hidden:
                continue

            tab_button = self._tab_close_buttons[i]

            # determine if a close button is on this tab
            if (self._agwFlags & AUI_NB_CLOSE_ON_ALL_TABS and page.hasCloseButton) or \
               (self._agwFlags & AUI_NB_CLOSE_ON_ACTIVE_TAB and page.active and page.hasCloseButton):

                if tab_button.cur_state == AUI_BUTTON_STATE_HIDDEN:

                    tab_button.id = AUI_BUTTON_CLOSE
                    tab_button.cur_state = AUI_BUTTON_STATE_NORMAL
                    tab_button.location = wx.CENTER

            else:

                tab_button.cur_state = AUI_BUTTON_STATE_HIDDEN

            rect.x = offset
            rect.width = self._rect.width - right_buttons_width - offset - 2

            if rect.width <= 0:
                break

            page.rect, tab_button.rect, x_extent = self._art.DrawTab(dc, wnd, page, rect, tab_button.cur_state)

            if page.active:
                active = i
                active_offset = offset
                active_rect = wx.Rect(*rect)

            offset += x_extent

        print("----------")
        ###
        for i in range(button_count):
            button = self._buttons[button_count - i - 1]

            if button.location != wx.RIGHT:
                continue
            if button.cur_state & AUI_BUTTON_STATE_HIDDEN:
                continue
            
            print(offset)
            button_rect = wx.Rect(*self._rect)
            button_rect.SetY(1)
            button_rect.SetWidth(offset)

            button.rect = self._art.DrawButton(dc, wnd, button_rect, button, wx.RIGHT)

            offset -= button.rect.GetWidth()
            right_buttons_width += button.rect.GetWidth()
        ###

        lenPages = len(self._pages)
        # make sure to deactivate buttons which are off the screen to the right
        
        # for j in range(i+1, len(self._tab_close_buttons)):
        #     self._tab_close_buttons[j].cur_state = AUI_BUTTON_STATE_HIDDEN
        #     if j > 0 and j <= lenPages:
        #         if self._pages[j-1].control:
        #             if self._pages[j-1].control.IsShown():
        #                 self._pages[j-1].control.Hide()

        # draw the active tab again so it stands in the foreground
        if active >= self._tab_offset and active < len(self._pages):

            page = self._pages[active]
            tab_button = self._tab_close_buttons[active]

            rect.x = active_offset
            dummy = self._art.DrawTab(dc, wnd, page, active_rect, tab_button.cur_state)

        raw_dc.Blit(self._rect.x, self._rect.y, self._rect.GetWidth(), self._rect.GetHeight(), dc, 0, 0)

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`AuiTabCtrl`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.PaintDC(self)
        dc.SetFont(self.GetFont())

        if self.GetPageCount() > 0:
            self.Render(dc, self)