# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import str
from builtins import range
import xbmcaddon
import xbmcgui

# Import the common settings
from .settings import log
from .settings import Settings

ADDON = xbmcaddon.Addon(id='script.pinsentry')
CWD = ADDON.getAddonInfo('path').decode("utf-8")


# Class that uses the default Number keyboard and overwrites it's behaviour
# so that it can except hidden pin numbers
class NumberPad(xbmcgui.WindowXMLDialog):
    BUTTON_BACKSPACE = 23
    BUTTON_DONE = 21
    BUTTON_PREVIOUS = 20
    BUTTON_NEXT = 22

    def __init__(self, strxmlname, strfallbackpath, titlelangid=32103):
        self.code = ""
        self.stars = ""
        self.titleLangId = titleLangId

    @staticmethod
    def createnumberpad(titlelangid=32103):
        return NumberPad("DialogNumeric.xml", CWD, titlelangid=titlelangid)

    # Returns the value of the pin code
    def getpin(self):
        # Only return the pin value if it meets the required length
        if Settings.getPinLength() < len(self.code):
            return ""
        return self.code

    def oninit(self):
        # Disable the buttons we are not interested in
        try:
            prevbutton = self.getControl(NumberPad.BUTTON_PREVIOUS)
            prevbutton.setEnabled(False)
            nextbutton = self.getControl(NumberPad.BUTTON_NEXT)
            nextbutton.setEnabled(False)
        except:
            # Having the buttons enabled is not a big issue, we can just
            # continue as they will just do nothing
            log("NumberPad: Failed to disable next and previous buttons")

        # Make sure all the numbers are set correctly, some times the mapping
        # to the string class do not work
        for i in range(0, 10):
            try:
                numbutton = self.getControl(i + 10)
                numbutton.setLabel(str(i))
            except:
                log("NumberPad: Failed to update text on numeric button %d" % i)

        # Set the title of the dialog
        try:
            self.getControl(1).setLabel(ADDON.getLocalizedString(self.titleLangId).encode('utf-8'))
        except:
            log("NumberPad: Failed to set title")

        # Check if the direction keys are being used as a pin code, in which case
        # we do not want to allow the user to select any of the buttons via the screen
        if Settings.isDirectionKeysAsPin():
            try:
                for i in range(0, 10):
                    numbutton = self.getControl(i + 10)
                    numbutton.setEnabled(False)
                backspacebutton = self.getControl(NumberPad.BUTTON_BACKSPACE)
                backspacebutton.setEnabled(False)
            except:
                log("NumberPad: Failed to disable keys on keypad")

        xbmcgui.WindowXMLDialog.onInit(self)

    # Detect things like remote control of keyboard button presses
    def onaction(self, action):
        id_ = action.getId()
        # actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h
        action_previous_menu = 10
        action_nav_back = 92
        action_backspace = 110

        if (action == action_previous_menu) or (action == action_nav_back):
            log("NumberPad: Close Action received: %s" % str(id_))
            self.close()
        elif action == action_backspace:
            # Backspace has been pressed
            self._removelastcharacter()
        elif (id_ > 57) and (id_ < 68):
            # NumericValue found, convert it
            # Numbers as follows
            # 58 = 0, 59 = 1 ...
            # So take 58 off and you get the number
            numval = id_ - 58
            self._numberEntered(numval)
        elif (id_ > 139) and (id_ < 150):
            # Remote control can send different keys
            # NumericValue found, convert it
            # Numbers as follows
            # 140 = 0, 141 = 1 ...
            # So take 140 off and you get the number
            numval = id_ - 140
            self._numberEntered(numval)
        elif Settings.isDirectionKeysAsPin() and (id_ > 0) and (id_ < 5):
            # If we want to allow the direction arrows on remote controls to be used
            # in the keys, then we need to map the directions to numbers, for simplicity
            # we map like a phone or remote, looking at the key pad:
            #     1 2 3
            #     4 5 6
            #     7 8 9
            #       0
            # So we map UP to 2, Down to 8, Left to 4 and right to 6
            if id_ == 1:
                # 1 is Left
                self._numberEntered(4)
            elif id_ == 2:
                # 2 is Right
                self._numberEntered(6)
            elif id_ == 3:
                # 3 is Up
                self._numberEntered(2)
            elif id_ == 4:
                # 4 is Down
                self._numberEntered(8)
        else:
            log("NumberPad: Unknown key pressed %s" % str(id_))

    # Record that a numeric value has been entered by the user
    def _numberentered(self, numvalue):
        log("NumberPad: Entered number %d" % numvalue)
        self.code += str(numvalue)
        # Sets the correct number of stars on the display
        self.stars = self.stars + "*"
        self.getControl(4).setLabel(self.stars)

        # Check if we have 4 numbers, if we do, then we can close the dialog
        # automatically
        if len(self.code) == Settings.getPinLength():
            self.close()

    # Removes the last character from the code
    def _removelastcharacter(self):
        log("NumberPad: Delete last character request")
        if len(self.code) > 0:
            self.code = self.code[:-1]
            self.stars = self.stars[:-1]
            self.getControl(4).setLabel(self.stars)

    # Detect when the user has clicked on the screen
    def onclick(self, controlid):
        # Convert all the numbers that are supported
        if (controlid > 9) and (controlid < 20):
            self._numberEntered(controlid - 10)
        elif controlid == NumberPad.BUTTON_DONE:
            # Done button has been pressed
            self.close()
        elif controlid == NumberPad.BUTTON_BACKSPACE:
            # Backspace has been pressed
            self._removeLastCharacter()
