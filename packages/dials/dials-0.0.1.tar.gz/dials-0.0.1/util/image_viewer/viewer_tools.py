# coding: utf-8

"""
Various tools/controls used by the image viewer
"""

from __future__ import absolute_import, division, print_function

import collections

import wx
from orderedset import OrderedSet

WX3 = wx.VERSION[0] == 3


class ImageCollectionWithSelection(OrderedSet):
    """A Ordered-like object that tracks a 'currently selected item'"""

    def __init__(self, items=None):
        super(ImageCollectionWithSelection, self).__init__(items or [])
        self._selected_index = None

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, index):
        if index is not None:
            index = int(index)
            if index < 0 or index > len(self._items) - 1:
                raise IndexError("Out of index range")
        self._selected_index = int(index)

    @property
    def selected(self):
        if self._selected_index is None:
            return None
        return self[self._selected_index]

    @selected.setter
    def selected(self, item):
        self._selected_index = self.index(item)


class LegacyChooserAdapter(object):
    """Fake wx.Choice replacement for legacy upstream code.

    The design relies on a wx.Choice object being created by a subclass and
    stored on a frame.image_chooser attribute. This wx.Choice object is then
    used to control the current selected image and storing information about
    all the 'loaded' images. This class replaces the API minimally so that
    the upstream code still works, while letting us transition to something
    a little saner in our implementation.
    """

    def __init__(self, images, loader):
        """
        Create the fake wx.Choice object.
        :param images: The list-like object containing the image data
        :param loader: A function to call to load a specific entry as current
        """
        super(LegacyChooserAdapter, self).__init__()
        self._images = images
        self._loader = loader

    def GetCount(self):
        return len(self._images)

    def SetSelection(self, index):
        if self._images.selected_index != index:
            # self._images.selected_index = index
            # print("Posting event from fake choice")
            # wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHOICE.typeId, 1))
            self._loader(self._images[index])

    def GetSelection(self):
        return self._images.selected_index

    def GetClientData(self, index):
        return self._images[index]


class ImageChooserControl(wx.Control):
    """
    Convenience control to display a slider and accompanying label
    """

    def __init__(self, *args, **kwargs):
        kwargs["style"] = kwargs.get("style", 0) | wx.BORDER_NONE
        super(ImageChooserControl, self).__init__(*args, **kwargs)

        self._slider = wx.Slider(self, -1, style=wx.SL_AUTOTICKS)
        self._slider.SetMin(1)
        self._label = wx.StaticText(self, -1, "Some Text")

        # Work out the maximum size of the text so that we can cut off the slider to allow room
        if WX3:
            _, size_y = self._label.GetAdjustedBestSize()
            self._label.SetFont(self._label.GetFont().Italic())
            self.size_y = max(size_y, self._label.GetAdjustedBestSize()[1])
        else:
            _, size_y = self._label.GetEffectiveMinSize()
            self._label.SetFont(self._label.GetFont().Italic())
            self.size_y = max(size_y, self._label.GetEffectiveMinSize()[1])

        # Use a horizontal box to control vertical alignment
        labelSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer.Add(self._label, flag=wx.ALL | wx.ALIGN_BOTTOM)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._slider, flag=wx.ALL | wx.ALIGN_LEFT)
        sizer.Add(labelSizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

    def Layout(self):
        # Fix the slider height so that we can fit the whole text in
        w, h = self.GetSize()
        self._slider.SetMinSize((w, h - self.size_y))
        # Delgate to the sizers for the rest of the calculation
        super(ImageChooserControl, self).Layout()

    def set_temporary_label(self, label):
        """Set the display label to a 'temporary' styled entry"""
        self._label.SetForegroundColour((100, 100, 100))
        self._label.SetLabel(label)
        self._label.SetFont(wx.NORMAL_FONT.Italic())
        # Don't seem to get automatic layout calls inside toolbars
        self.Layout()

    def set_label(self, label):
        """Set the display label to a 'permanent' styled entry"""
        self._label.SetForegroundColour((0, 0, 0))
        self._label.SetLabel(label)
        self._label.SetFont(wx.NORMAL_FONT)
        # Don't seem to get automatic layout calls inside toolbars
        self.Layout()

    def GetValue(self):
        return self._slider.GetValue()

    def SetValue(self, value):
        self._slider.SetValue(value)

    def SetMax(self, value):
        "Set maximum, and disable the slider if necessary"
        if value == 1:
            assert self._slider.GetValue() == 1
            self._slider.Disable()
        else:
            self._slider.Enable()
        self._slider.SetMax(value)
