# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html
# This is an XBMC addon for demonstrating the capabilities
# and usage of PyXBMCt framework.

import os
import xbmc
import xbmcaddon
import pyxbmct

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')

# Enable or disable Estuary-based design explicitly
# pyxbmct.skin.estuary = True


class MyAddon(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        super(MyAddon, self).__init__(title)
        self.setGeometry(700, 450, 9, 4)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self):
        # Demo for PyXBMCt UI controls.
        no_int_label = pyxbmct.Label('Information output', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 0, 1, 2)
        #
        label_label = pyxbmct.Label('Label')
        self.placeControl(label_label, 1, 0)
        # Label
        self.label = pyxbmct.Label('Simple label')
        self.placeControl(self.label, 1, 1)
        #
        fadelabel_label = pyxbmct.Label('FadeLabel')
        self.placeControl(fadelabel_label, 2, 0)
        # FadeLabel
        self.fade_label = pyxbmct.FadeLabel()
        self.placeControl(self.fade_label, 2, 1)
        self.fade_label.addLabel('Very long string can be here.')
        #
        textbox_label = pyxbmct.Label('TextBox')
        self.placeControl(textbox_label, 3, 0)
        # TextBox
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 3, 1, 2, 1)
        self.textbox.setText('It can display long text.\n'
                             'Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(1000, 1000, 1000)
        #
        image_label = pyxbmct.Label('Image')
        self.placeControl(image_label, 5, 0)
        # Image
        self.image = pyxbmct.Image(os.path.join(_addon_path, 'bbb-splash.jpg'))
        self.placeControl(self.image, 5, 1, 2, 1)

    def set_active_controls(self):
        int_label = pyxbmct.Label('Interactive Controls', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(int_label, 0, 2, 1, 2)
        #
        radiobutton_label = pyxbmct.Label('RadioButton')
        self.placeControl(radiobutton_label, 1, 2)
        # RadioButton
        self.radiobutton = pyxbmct.RadioButton('Off')
        self.placeControl(self.radiobutton, 1, 3)
        self.connect(self.radiobutton, self.radio_update)
        #
        edit_label = pyxbmct.Label('Edit')
        self.placeControl(edit_label, 2, 2)
        # Edit
        self.edit = pyxbmct.Edit('Edit')
        self.placeControl(self.edit, 2, 3)
        # Additional properties must be changed after (!) displaying a control.
        self.edit.setText('Enter text here')
        #
        list_label = pyxbmct.Label('List')
        self.placeControl(list_label, 3, 2)
        #
        self.list_item_label = pyxbmct.Label('', textColor='0xFF808080')
        self.placeControl(self.list_item_label, 4, 2)
        # List
        self.list = pyxbmct.List()
        self.placeControl(self.list, 3, 3, 3, 1)
        # Add items to the list
        items = ['Item {0}'.format(i) for i in range(1, 8)]
        self.list.addItems(items)
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, lambda: xbmc.executebuiltin('Notification(Note!,{0} selected.)'.format(
            self.list.getListItem(self.list.getSelectedPosition()).getLabel())))
        # Connect key and mouse events for list navigation feedback.
        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.list_update)
        # Slider value label
        SLIDER_INIT_VALUE = 25.0
        self.slider_value = pyxbmct.Label(str(SLIDER_INIT_VALUE), alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.slider_value, 6, 3)
        #
        slider_caption = pyxbmct.Label('Slider')
        self.placeControl(slider_caption, 7, 2)
        # Slider
        self.slider = pyxbmct.Slider()
        self.placeControl(self.slider, 7, 3, pad_y=10)
        self.slider.setPercent(SLIDER_INIT_VALUE)
        # Connect key and mouse events for slider update feedback.
        self.connectEventList([pyxbmct.ACTION_MOVE_LEFT,
                               pyxbmct.ACTION_MOVE_RIGHT,
                               pyxbmct.ACTION_MOUSE_DRAG,
                               pyxbmct.ACTION_MOUSE_LEFT_CLICK],
                              self.slider_update)
        #
        button_label = pyxbmct.Label('Button')
        self.placeControl(button_label, 8, 2)
        # Button
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 8, 3)
        # Connect control to close the window.
        self.connect(self.button, self.close)

    def set_navigation(self):
        # Set navigation between controls
        self.button.controlUp(self.slider)
        self.button.controlDown(self.radiobutton)
        self.radiobutton.controlUp(self.button)
        self.radiobutton.controlDown(self.edit)
        self.edit.controlUp(self.radiobutton)
        self.edit.controlDown(self.list)
        self.list.controlUp(self.edit)
        self.list.controlDown(self.slider)
        self.slider.controlUp(self.list)
        self.slider.controlDown(self.button)
        # Set initial focus
        self.setFocus(self.radiobutton)

    def slider_update(self):
        # Update slider value label when the slider nib moves
        try:
            if self.getFocus() == self.slider:
                self.slider_value.setLabel('{:.1F}'.format(self.slider.getPercent()))
        except (RuntimeError, SystemError):
            pass

    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])


if __name__ == '__main__':
    window = MyAddon('PyXBMCt Demo')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window
