# -*- coding: utf-8 -*-
from builtins import str
from builtins import range
from builtins import object
import os
import hashlib
import time
from datetime import date
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon(id='script.pinsentry')
ADDON_ID = ADDON.getAddonInfo('id')


# Common logging module
def log(txt, loglevel=xbmc.LOGDEBUG):
    if (ADDON.getSetting("logEnabled") == "true") or (loglevel != xbmc.LOGDEBUG):
        if isinstance(txt, str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (ADDON_ID, txt)
        xbmc.log(msg=message.encode("utf-8"), level=loglevel)


# There has been problems with calling join with non ascii characters,
# so we have this method to try and do the conversion for us
def os_path_join(dir, file):
    # Convert each argument - if an error, then it will use the default value
    # that was passed in
    try:
        dir = dir.decode("utf-8")
    except:
        pass
    try:
        file = file.decode("utf-8")
    except:
        pass
    return os.path.join(dir, file)


##############################
# Stores Various Settings
##############################
class Settings(object):
    INVALID_PIN_NOTIFICATION_POPUP = 0
    INVALID_PIN_NOTIFICATION_DIALOG = 1
    INVALID_PIN_NOTIFICATION_NONE = 2

    # Flags from www.pixabay.com User:OpenClipartVectors
    # https://pixabay.com/en/photos/?image_type=&cat=&min_width=&min_height=&q=user%3AOpenClipart-Vectors+flag+square&order=popular
    flags = [{'lang': 32301, 'icon': 'UK/UK-flag.png'},
             {'lang': 32302, 'icon': 'USA/USA-flag.png'},
             {'lang': 32303, 'icon': 'Germany/Germany-flag.png'},
             {'lang': 32304, 'icon': 'Ireland/Ireland-flag.png'},
             {'lang': 32305, 'icon': 'Netherlands/Netherlands-flag.png'},
             {'lang': 32306, 'icon': 'Australia/Australia-flag.png'},
             {'lang': 32307, 'icon': 'Brazil/Brazil-flag.png'},
             {'lang': 32308, 'icon': 'Hungary/Hungary-flag.png'},
             {'lang': 32309, 'icon': 'Denmark/Denmark-flag.png'},
             {'lang': 32310, 'icon': 'Norway/Norway-flag.png'},
             {'lang': 32311, 'icon': 'Sweden/Sweden-flag.png'},
             {'lang': 32312, 'icon': 'Finland/Finland-flag.png'},
             {'lang': 32313, 'icon': 'Canada/Canada-flag.png'},
             {'lang': 32315, 'icon': 'France/France-flag.png'},
             {'lang': 32316, 'icon': 'Italy/Italy-flag.png'},
             {'lang': 32317, 'icon': 'Spain/Spain-flag.png'},
             {'lang': 32318, 'icon': 'SouthKorea/SouthKorea-flag.png'},
             {'lang': 32319, 'icon': 'India/India-flag.png'},
             {'lang': 32320, 'icon': 'Portugal/Portugal-flag.png'}]

    # http://en.wikipedia.org/wiki/Motion_picture_rating_system
    movieCassificationsNames = [{'id': 1, 'name': '%s - U', 'lang': 32301, 'match': 'U', 'icon': 'UK/UK-U.png'},  # UK
                                {'id': 2, 'name': '%s - PG', 'lang': 32301, 'match': 'PG', 'icon': 'UK/UK-PG.png'},
                                {'id': 3, 'name': '%s - 12A', 'lang': 32301, 'match': '12A', 'icon': 'UK/UK-12A.png'},
                                {'id': 4, 'name': '%s - 12', 'lang': 32301, 'match': '12', 'icon': 'UK/UK-12.png'},
                                {'id': 5, 'name': '%s - 15', 'lang': 32301, 'match': '15', 'icon': 'UK/UK-15.png'},
                                {'id': 6, 'name': '%s - 18', 'lang': 32301, 'match': '18', 'icon': 'UK/UK-18.png'},
                                {'id': 7, 'name': '%s - R18', 'lang': 32301, 'match': 'R18', 'icon': 'UK/UK-R18.png'},
                                # USA
                                {'id': 8, 'name': '%s - G', 'lang': 32302, 'match': 'G', 'icon': 'USA/USA-G.png'},
                                {'id': 9, 'name': '%s - PG', 'lang': 32302, 'match': 'PG', 'icon': 'USA/USA-PG.png'},
                                {'id': 10, 'name': '%s - PG-13', 'lang': 32302, 'match': 'PG-13', 'icon': 'USA/USA-PG-13.png'},
                                {'id': 11, 'name': '%s - R', 'lang': 32302, 'match': 'R', 'icon': 'USA/USA-R.png'},
                                {'id': 12, 'name': '%s - NC-17', 'lang': 32302, 'match': 'NC-17', 'icon': 'USA/USA-NC-17.png'},
                                # Germany
                                {'id': 13, 'name': '%s - FSK 0', 'lang': 32303, 'match': '0', 'icon': 'Germany/Germany-FSK-0.png'},
                                {'id': 14, 'name': '%s - FSK 6', 'lang': 32303, 'match': '6', 'icon': 'Germany/Germany-FSK-6.png'},
                                {'id': 15, 'name': '%s - FSK 12', 'lang': 32303, 'match': '12', 'icon': 'Germany/Germany-FSK-12.png'},
                                {'id': 16, 'name': '%s - FSK 16', 'lang': 32303, 'match': '16', 'icon': 'Germany/Germany-FSK-16.png'},
                                {'id': 17, 'name': '%s - FSK 18', 'lang': 32303, 'match': '18', 'icon': 'Germany/Germany-FSK-18.png'},
                                # Ireland
                                {'id': 18, 'name': '%s - G', 'lang': 32304, 'match': 'G', 'icon': 'Ireland/Ireland-G.png'},
                                {'id': 19, 'name': '%s - PG', 'lang': 32304, 'match': 'PG', 'icon': 'Ireland/Ireland-PG.png'},
                                {'id': 20, 'name': '%s - 12A', 'lang': 32304, 'match': '12A', 'icon': 'Ireland/Ireland-12A.png'},
                                {'id': 21, 'name': '%s - 15A', 'lang': 32304, 'match': '15A', 'icon': 'Ireland/Ireland-15A.png'},
                                {'id': 22, 'name': '%s - 16', 'lang': 32304, 'match': '16', 'icon': 'Ireland/Ireland-16.png'},
                                {'id': 23, 'name': '%s - 18', 'lang': 32304, 'match': '18', 'icon': 'Ireland/Ireland-18.png'},
                                # Netherlands
                                {'id': 24, 'name': '%s - AL', 'lang': 32305, 'match': 'AL', 'icon': 'Netherlands/Netherlands-AL.png'},
                                {'id': 25, 'name': '%s - 6', 'lang': 32305, 'match': '6', 'icon': 'Netherlands/Netherlands-6.png'},
                                {'id': 26, 'name': '%s - 9', 'lang': 32305, 'match': '9', 'icon': 'Netherlands/Netherlands-9.png'},
                                {'id': 27, 'name': '%s - 12', 'lang': 32305, 'match': '12', 'icon': 'Netherlands/Netherlands-12.png'},
                                {'id': 28, 'name': '%s - 16', 'lang': 32305, 'match': '16', 'icon': 'Netherlands/Netherlands-16.png'},
                                # Australia
                                {'id': 29, 'name': '%s - E', 'lang': 32306, 'match': 'E', 'icon': 'Australia/Australia-E.png'},
                                {'id': 30, 'name': '%s - G', 'lang': 32306, 'match': 'G', 'icon': 'Australia/Australia-G.png'},
                                {'id': 31, 'name': '%s - PG', 'lang': 32306, 'match': 'PG', 'icon': 'Australia/Australia-PG.png'},
                                {'id': 32, 'name': '%s - M', 'lang': 32306, 'match': 'M', 'icon': 'Australia/Australia-M.png'},
                                {'id': 33, 'name': '%s - MA15+', 'lang': 32306, 'match': 'MA15+', 'icon': 'Australia/Australia-MA.png'},
                                {'id': 34, 'name': '%s - R18+', 'lang': 32306, 'match': 'R18+', 'icon': 'Australia/Australia-R.png'},
                                {'id': 35, 'name': '%s - X18+', 'lang': 32306, 'match': 'X18+', 'icon': 'Australia/Australia-X.png'},
                                # Brazil
                                {'id': 36, 'name': '%s - L', 'lang': 32307, 'match': 'L', 'icon': 'Brazil/Brazil-L.png'},
                                {'id': 37, 'name': '%s - 10', 'lang': 32307, 'match': '10', 'icon': 'Brazil/Brazil-10.png'},
                                {'id': 38, 'name': '%s - 12', 'lang': 32307, 'match': '12', 'icon': 'Brazil/Brazil-12.png'},
                                {'id': 39, 'name': '%s - 14', 'lang': 32307, 'match': '14', 'icon': 'Brazil/Brazil-14.png'},
                                {'id': 40, 'name': '%s - 16', 'lang': 32307, 'match': '16', 'icon': 'Brazil/Brazil-16.png'},
                                {'id': 41, 'name': '%s - 18', 'lang': 32307, 'match': '18', 'icon': 'Brazil/Brazil-18.png'},
                                # Hungary
                                {'id': 42, 'name': '%s - 0', 'lang': 32308, 'match': '0', 'icon': 'Hungary/Hungary-0.png'},
                                {'id': 43, 'name': '%s - 6', 'lang': 32308, 'match': '6', 'icon': 'Hungary/Hungary-6.png'},
                                {'id': 44, 'name': '%s - 12', 'lang': 32308, 'match': '12', 'icon': 'Hungary/Hungary-12.png'},
                                {'id': 45, 'name': '%s - 16', 'lang': 32308, 'match': '16', 'icon': 'Hungary/Hungary-16.png'},
                                {'id': 46, 'name': '%s - 18', 'lang': 32308, 'match': '18', 'icon': 'Hungary/Hungary-18.png'},
                                {'id': 47, 'name': '%s - X', 'lang': 32308, 'match': 'X', 'icon': 'Hungary/Hungary-X.png'},
                                # Denmark
                                {'id': 48, 'name': '%s - A', 'lang': 32309, 'match': 'A', 'icon': 'Denmark/Denmark-A.png'},
                                {'id': 49, 'name': '%s - 7', 'lang': 32309, 'match': '7', 'icon': 'Denmark/Denmark-7.png'},
                                {'id': 50, 'name': '%s - 11', 'lang': 32309, 'match': '11', 'icon': 'Denmark/Denmark-11.png'},
                                {'id': 51, 'name': '%s - 15', 'lang': 32309, 'match': '15', 'icon': 'Denmark/Denmark-15.png'},
                                {'id': 52, 'name': '%s - F', 'lang': 32309, 'match': 'F', 'icon': 'Denmark/Denmark-F.png'},
                                # Norway
                                {'id': 53, 'name': '%s - A', 'lang': 32310, 'match': 'A', 'icon': 'Norway/Norway-A.png'},
                                {'id': 54, 'name': '%s - 7', 'lang': 32310, 'match': '7', 'icon': 'Norway/Norway-7.png'},
                                {'id': 55, 'name': '%s - 11', 'lang': 32310, 'match': '11', 'icon': 'Norway/Norway-11.png'},
                                {'id': 56, 'name': '%s - 15', 'lang': 32310, 'match': '15', 'icon': 'Norway/Norway-15.png'},
                                {'id': 57, 'name': '%s - 18', 'lang': 32310, 'match': '18', 'icon': 'Norway/Norway-18.png'},
                                # Norway (New classifications for 2015 onwards)
                                {'id': 58, 'name': '%s - A', 'lang': 32310, 'match': 'A', 'icon': 'Norway/Norway-2015-A.png'},
                                {'id': 59, 'name': '%s - 6', 'lang': 32310, 'match': '6', 'icon': 'Norway/Norway-2015-6.png'},
                                {'id': 60, 'name': '%s - 9', 'lang': 32310, 'match': '9', 'icon': 'Norway/Norway-2015-9.png'},
                                {'id': 61, 'name': '%s - 12', 'lang': 32310, 'match': '12', 'icon': 'Norway/Norway-2015-12.png'},
                                {'id': 62, 'name': '%s - 15', 'lang': 32310, 'match': '15', 'icon': 'Norway/Norway-2015-15.png'},
                                {'id': 63, 'name': '%s - 18', 'lang': 32310, 'match': '18', 'icon': 'Norway/Norway-2015-18.png'},
                                # Sweden
                                {'id': 64, 'name': '%s - Btl', 'lang': 32311, 'match': 'Btl', 'icon': None},
                                {'id': 65, 'name': '%s - 7', 'lang': 32311, 'match': '7', 'icon': None},
                                {'id': 66, 'name': '%s - 11', 'lang': 32311, 'match': '11', 'icon': None},
                                {'id': 67, 'name': '%s - 15', 'lang': 32311, 'match': '15', 'icon': None},
                                # Finland
                                {'id': 68, 'name': '%s - S', 'lang': 32312, 'match': 'S', 'icon': 'Finland/Finland-S.png'},
                                {'id': 69, 'name': '%s - 7', 'lang': 32312, 'match': '7', 'icon': 'Finland/Finland-7.png'},
                                {'id': 83, 'name': '%s - 12', 'lang': 32312, 'match': '12', 'icon': 'Finland/Finland-12.png'},
                                {'id': 84, 'name': '%s - 16', 'lang': 32312, 'match': '16', 'icon': 'Finland/Finland-16.png'},
                                {'id': 85, 'name': '%s - 18', 'lang': 32312, 'match': '18', 'icon': 'Finland/Finland-18.png'},
                                # Canada
                                {'id': 70, 'name': '%s - G', 'lang': 32313, 'match': 'G', 'icon': 'Canada/Canada-G.png'},
                                {'id': 71, 'name': '%s - PG', 'lang': 32313, 'match': 'PG', 'icon': 'Canada/Canada-PG.png'},
                                {'id': 72, 'name': '%s - 14A', 'lang': 32313, 'match': '14A', 'icon': 'Canada/Canada-14A.png'},
                                {'id': 73, 'name': '%s - 18A', 'lang': 32313, 'match': '18A', 'icon': 'Canada/Canada-18A.png'},
                                {'id': 74, 'name': '%s - R', 'lang': 32313, 'match': 'R', 'icon': 'Canada/Canada-R.png'},
                                {'id': 75, 'name': '%%s (%s) - G' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': 'G', 'icon': 'Canada/Canada-Quebec-G.png'},
                                {'id': 76, 'name': '%%s (%s) - 13+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '13+', 'icon': 'Canada/Canada-Quebec-13.png'},
                                {'id': 77, 'name': '%%s (%s) - 16+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '16+', 'icon': 'Canada/Canada-Quebec-16.png'},
                                {'id': 78, 'name': '%%s (%s) - 18+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '18+', 'icon': 'Canada/Canada-Quebec-18.png'},
                                # France
                                {'id': 79, 'name': '%s - U', 'lang': 32315, 'match': 'U', 'icon': None},
                                {'id': 80, 'name': '%s - 12', 'lang': 32315, 'match': '12', 'icon': None},
                                {'id': 81, 'name': '%s - 16', 'lang': 32315, 'match': '16', 'icon': None},
                                {'id': 82, 'name': '%s - 18', 'lang': 32315, 'match': '18', 'icon': None},
                                # Italy
                                {'id': 86, 'name': '%s - T', 'lang': 32316, 'match': 'T', 'icon': 'Italy/Italy-T.png'},
                                {'id': 87, 'name': '%s - VM14', 'lang': 32316, 'match': 'VM14', 'icon': 'Italy/Italy-VM14.png'},
                                {'id': 88, 'name': '%s - VM18', 'lang': 32316, 'match': 'VM18', 'icon': 'Italy/Italy-VM18.png'},
                                # Spain
                                {'id': 89, 'name': '%s - APTA', 'lang': 32317, 'match': 'A', 'icon': 'Spain/Spain-A.png'},
                                {'id': 90, 'name': '%s - 7', 'lang': 32317, 'match': '7', 'icon': 'Spain/Spain-7.png'},
                                {'id': 91, 'name': '%s - 12', 'lang': 32317, 'match': '12', 'icon': 'Spain/Spain-12.png'},
                                {'id': 92, 'name': '%s - 16', 'lang': 32317, 'match': '12', 'icon': 'Spain/Spain-16.png'},
                                {'id': 93, 'name': '%s - 18', 'lang': 32317, 'match': '12', 'icon': 'Spain/Spain-18.png'},
                                {'id': 94, 'name': '%s - X', 'lang': 32317, 'match': 'X', 'icon': 'Spain/Spain-X.png'},
                                # South Korea
                                {'id': 95, 'name': '%s - All', 'lang': 32318, 'match': 'All', 'icon': 'SouthKorea/SouthKorea-All.png'},
                                {'id': 96, 'name': '%s - 12', 'lang': 32318, 'match': '12', 'icon': 'SouthKorea/SouthKorea-12.png'},
                                {'id': 97, 'name': '%s - 15', 'lang': 32318, 'match': '15', 'icon': 'SouthKorea/SouthKorea-15.png'},
                                {'id': 98, 'name': '%s - R', 'lang': 32318, 'match': 'R', 'icon': 'SouthKorea/SouthKorea-R.png'},
                                {'id': 99, 'name': '%s - Restricted Screening', 'lang': 32318, 'match': 'Restricted Screening', 'icon': 'SouthKorea/SouthKorea-Restricted.png'},
                                # India
                                {'id': 100, 'name': '%s - U', 'lang': 32319, 'match': 'U', 'icon': 'India/India-U.png'},
                                {'id': 101, 'name': '%s - UA', 'lang': 32319, 'match': 'UA', 'icon': 'India/India-UA.png'},
                                {'id': 102, 'name': '%s - A', 'lang': 32319, 'match': 'A', 'icon': 'India/India-A.png'},
                                {'id': 103, 'name': '%s - S', 'lang': 32319, 'match': 'S', 'icon': 'India/India-S.png'},
                                # France
                                {'id': 104, 'name': '%s - A', 'lang': 32320, 'match': 'A', 'icon': None},
                                {'id': 105, 'name': '%s - M/3', 'lang': 32320, 'match': 'M/3', 'icon': None},
                                {'id': 106, 'name': '%s - M/4', 'lang': 32320, 'match': 'M/4', 'icon': None},
                                {'id': 107, 'name': '%s - M/6', 'lang': 32320, 'match': 'M/6', 'icon': None},
                                {'id': 108, 'name': '%s - M/12', 'lang': 32320, 'match': 'M/12', 'icon': None},
                                {'id': 109, 'name': '%s - M/14', 'lang': 32320, 'match': 'M/14', 'icon': None},
                                {'id': 110, 'name': '%s - M/16', 'lang': 32320, 'match': 'M/16', 'icon': None},
                                {'id': 111, 'name': '%s - M/18', 'lang': 32320, 'match': 'M/18', 'icon': None},
                                {'id': 112, 'name': '%s - P', 'lang': 32320, 'match': 'P', 'icon': None}]

    # http://en.wikipedia.org/wiki/Television_content_rating_systems
    tvCassificationsNames = [{'id': 1, 'name': '%s - TV-Y', 'lang': 32302, 'match': 'TV-Y', 'icon': 'USA/USA-TV-Y.png'},  # USA
                             {'id': 2, 'name': '%s - TV-Y7', 'lang': 32302, 'match': 'TV-Y7', 'icon': 'USA/USA-TV-Y7.png'},
                             {'id': 3, 'name': '%s - TV-G', 'lang': 32302, 'match': 'TV-G', 'icon': 'USA/USA-TV-G.png'},
                             {'id': 4, 'name': '%s - TV-PG', 'lang': 32302, 'match': 'TV-PG', 'icon': 'USA/USA-TV-PG.png'},
                             {'id': 5, 'name': '%s - TV-14', 'lang': 32302, 'match': 'TV-14', 'icon': 'USA/USA-TV-14.png'},
                             {'id': 6, 'name': '%s - TV-MA', 'lang': 32302, 'match': 'TV-MA', 'icon': 'USA/USA-TV-MA.png'},
                             # Netherlands
                             {'id': 7, 'name': '%s - AL', 'lang': 32305, 'match': 'AL', 'icon': 'Netherlands/Netherlands-AL.png'},
                             {'id': 8, 'name': '%s - 6', 'lang': 32305, 'match': '6', 'icon': 'Netherlands/Netherlands-6.png'},
                             {'id': 9, 'name': '%s - 9', 'lang': 32305, 'match': '9', 'icon': 'Netherlands/Netherlands-9.png'},
                             {'id': 10, 'name': '%s - 12', 'lang': 32305, 'match': '12', 'icon': 'Netherlands/Netherlands-12.png'},
                             {'id': 11, 'name': '%s - 16', 'lang': 32305, 'match': '16', 'icon': 'Netherlands/Netherlands-16.png'},
                             # Australia
                             {'id': 12, 'name': '%s - P', 'lang': 32306, 'match': 'P', 'icon': 'Australia/Australia-TV-P.png'},
                             {'id': 13, 'name': '%s - C', 'lang': 32306, 'match': 'C', 'icon': 'Australia/Australia-TV-C.png'},
                             {'id': 14, 'name': '%s - G', 'lang': 32306, 'match': 'G', 'icon': 'Australia/Australia-TV-G.png'},
                             {'id': 15, 'name': '%s - PG', 'lang': 32306, 'match': 'PG', 'icon': 'Australia/Australia-TV-PG.png'},
                             {'id': 16, 'name': '%s - M', 'lang': 32306, 'match': 'M', 'icon': 'Australia/Australia-TV-M.png'},
                             {'id': 17, 'name': '%s - MA15+', 'lang': 32306, 'match': 'MA15+', 'icon': 'Australia/Australia-TV-MA.png'},
                             {'id': 18, 'name': '%s - AV15+', 'lang': 32306, 'match': 'AV15+', 'icon': 'Australia/Australia-TV-AV.png'},
                             {'id': 19, 'name': '%s - R18+', 'lang': 32306, 'match': 'R18+', 'icon': 'Australia/Australia-R.png'},
                             # Brazil
                             {'id': 20, 'name': '%s - L', 'lang': 32307, 'match': 'L', 'icon': 'Brazil/Brazil-L.png'},
                             {'id': 21, 'name': '%s - 10', 'lang': 32307, 'match': '10', 'icon': 'Brazil/Brazil-10.png'},
                             {'id': 22, 'name': '%s - 12', 'lang': 32307, 'match': '12', 'icon': 'Brazil/Brazil-12.png'},
                             {'id': 23, 'name': '%s - 14', 'lang': 32307, 'match': '14', 'icon': 'Brazil/Brazil-14.png'},
                             {'id': 24, 'name': '%s - 16', 'lang': 32307, 'match': '16', 'icon': 'Brazil/Brazil-16.png'},
                             {'id': 25, 'name': '%s - 18', 'lang': 32307, 'match': '18', 'icon': 'Brazil/Brazil-18.png'},
                             # Hungary
                             {'id': 26, 'name': '%s - 0', 'lang': 32308, 'match': '0', 'icon': 'Hungary/Hungary-TV-0.png'},
                             {'id': 27, 'name': '%s - 6', 'lang': 32308, 'match': '6', 'icon': 'Hungary/Hungary-TV-6.png'},
                             {'id': 28, 'name': '%s - 12', 'lang': 32308, 'match': '12', 'icon': 'Hungary/Hungary-TV-12.png'},
                             {'id': 29, 'name': '%s - 16', 'lang': 32308, 'match': '16', 'icon': 'Hungary/Hungary-TV-16.png'},
                             {'id': 30, 'name': '%s - 18', 'lang': 32308, 'match': '18', 'icon': 'Hungary/Hungary-TV-18.png'},
                             # Finland
                             {'id': 31, 'name': '%s - S', 'lang': 32312, 'match': 'S', 'icon': 'Finland/Finland-S.png'},
                             {'id': 32, 'name': '%s - 7', 'lang': 32312, 'match': '7', 'icon': 'Finland/Finland-7.png'},
                             {'id': 33, 'name': '%s - 12', 'lang': 32312, 'match': '12', 'icon': 'Finland/Finland-12.png'},
                             {'id': 34, 'name': '%s - 16', 'lang': 32312, 'match': '16', 'icon': 'Finland/Finland-16.png'},
                             {'id': 35, 'name': '%s - 18', 'lang': 32312, 'match': '18', 'icon': 'Finland/Finland-18.png'},
                             # Canada
                             {'id': 36, 'name': '%s - C', 'lang': 32313, 'match': 'C', 'icon': 'Canada/Canada-TV-C.png'},
                             {'id': 37, 'name': '%s - C8', 'lang': 32313, 'match': 'C8', 'icon': 'Canada/Canada-TV-C8.png'},
                             {'id': 38, 'name': '%s - G', 'lang': 32313, 'match': 'G', 'icon': 'Canada/Canada-TV-G.png'},
                             {'id': 39, 'name': '%s - PG', 'lang': 32313, 'match': 'PG', 'icon': 'Canada/Canada-TV-PG.png'},
                             {'id': 40, 'name': '%s - 14+', 'lang': 32313, 'match': '14+', 'icon': 'Canada/Canada-TV-14.png'},
                             {'id': 41, 'name': '%s - 18+', 'lang': 32313, 'match': '18+', 'icon': 'Canada/Canada-TV-18.png'},
                             {'id': 42, 'name': '%%s (%s) - G' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': 'G', 'icon': 'Canada/Canada-Quebec-G.png'},
                             {'id': 43, 'name': '%%s (%s) - 13+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '13+', 'icon': 'Canada/Canada-Quebec-13.png'},
                             {'id': 44, 'name': '%%s (%s) - 16+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '16+', 'icon': 'Canada/Canada-Quebec-16.png'},
                             {'id': 45, 'name': '%%s (%s) - 18+' % ADDON.getLocalizedString(32314), 'lang': 32313, 'match': '18+', 'icon': 'Canada/Canada-Quebec-18.png'},
                             # France
                             {'id': 46, 'name': '%s - 10', 'lang': 32315, 'match': '10', 'icon': 'France/France-TV-10.png'},
                             {'id': 47, 'name': '%s - 12', 'lang': 32315, 'match': '12', 'icon': 'France/France-TV-12.png'},
                             {'id': 48, 'name': '%s - 16', 'lang': 32315, 'match': '16', 'icon': 'France/France-TV-16.png'},
                             {'id': 49, 'name': '%s - 18', 'lang': 32315, 'match': '18', 'icon': 'France/France-TV-18.png'},
                             # Spain
                             {'id': 50, 'name': '%s - SC', 'lang': 32317, 'match': 'SC', 'icon': None},
                             {'id': 51, 'name': '%s - Infantil', 'lang': 32317, 'match': 'Infantil', 'icon': None},
                             {'id': 52, 'name': '%s - TP', 'lang': 32317, 'match': 'TP', 'icon': None},
                             {'id': 53, 'name': '%s - 7', 'lang': 32317, 'match': '7', 'icon': None},
                             {'id': 54, 'name': '%s - 10', 'lang': 32317, 'match': '10', 'icon': None},
                             {'id': 55, 'name': '%s - 12', 'lang': 32317, 'match': '12', 'icon': None},
                             {'id': 56, 'name': '%s - 13', 'lang': 32317, 'match': '13', 'icon': None},
                             {'id': 57, 'name': '%s - 16', 'lang': 32317, 'match': '16', 'icon': None},
                             {'id': 58, 'name': '%s - 18', 'lang': 32317, 'match': '18', 'icon': None},
                             # South Korea
                             {'id': 59, 'name': '%s - All', 'lang': 32318, 'match': 'All', 'icon': 'SouthKorea/SouthKorea-TV-All.png'},
                             {'id': 60, 'name': '%s - 7', 'lang': 32318, 'match': '7', 'icon': 'SouthKorea/SouthKorea-TV-7.png'},
                             {'id': 61, 'name': '%s - 12', 'lang': 32318, 'match': '12', 'icon': 'SouthKorea/SouthKorea-TV-12.png'},
                             {'id': 62, 'name': '%s - 15', 'lang': 32318, 'match': '15', 'icon': 'SouthKorea/SouthKorea-TV-15.png'},
                             {'id': 63, 'name': '%s - 19', 'lang': 32318, 'match': '19', 'icon': 'SouthKorea/SouthKorea-TV-19.png'},
                             # Portugal
                             {'id': 64, 'name': '%s - T', 'lang': 32320, 'match': 'T', 'icon': 'Portugal/Portugal-TV-T.png'},
                             {'id': 65, 'name': '%s - 10', 'lang': 32320, 'match': '10', 'icon': 'Portugal/Portugal-TV-10.png'},
                             {'id': 66, 'name': '%s - 12', 'lang': 32320, 'match': '12', 'icon': 'Portugal/Portugal-TV-12.png'},
                             {'id': 67, 'name': '%s - 16', 'lang': 32320, 'match': '16', 'icon': 'Portugal/Portugal-TV-16.png'}]

    @staticmethod
    def reloadsettings():
        # Before loading the new settings save off the length of the pin
        # this means that if the length of the pin has changed and the actual
        # pin value has not, we can clear the pin value
        pinlength = Settings.getpinlength()
        pinvalue = ADDON.getSetting("pinvalue")

        # Force the reload of the settings to pick up any new values
        global ADDON
        ADDON = xbmcaddon.Addon(id='script.pinsentry')

        if Settings.isPinSet():
            if pinlength != Settings.getpinlength():
                if pinvalue == ADDON.getSetting("pinValue"):
                    for i in range(1, 6):
                        Settings.setpinvalue("", i)
                        userid = "user%dPin" % i
                        Settings.setuserpinvalue("", userid)
                    # Display the warning in the settings
                    ADDON.setSetting("pinvalueset", "false")

    @staticmethod
    def setpinvalue(newpin, pinlevel=1):
        encryptedpin = ""
        if len(newpin) > 0:
            # Before setting the pin, encrypt it
            encryptedpin = Settings.encryptPin(newpin)

        # The first pin value does not have a numeric value at the end of it's ID
        pinsettingsvalue = "pinValue"
        if pinlevel > 1:
            pinsettingsvalue = "%s%d" % (pinsettingsvalue, pinlevel)
        ADDON.setSetting(pinsettingsvalue, encryptedpin)

    @staticmethod
    def setuserpinvalue(newpin, pinid):
        encryptedpin = ""
        pinset = 'false'
        if len(newpin) > 0:
            # Before setting the pin, encrypt it
            encryptedpin = Settings.encryptPin(newpin)
            pinset = 'true'

        ADDON.setSetting(pinid, encryptedpin)
        ADDON.setSetting("%sSet" % pinid, pinset)

    @staticmethod
    def checkpinsettings():
        # Check all of the pin settings to see if they are set
        # If they are not, then we need to enable the warning

        # Check how many pins are being used
        numlevels = Settings.getnumberoflevels()

        # Clear any of the pins that are not active
        clearpinnum = 5
        while numLevels < clearpinnum:
            log("SetPin: Clearing pin %d" % clearpinnum)
            Settings.setpinvalue("", clearpinnum)
            clearpinnum = clearpinnum - 1

        # Now check the remaining pins to see if they are set
        allpinsset = True
        pincheck = 1
        while pincheck <= numlevels:
            if not Settings.isPinSet(pincheck):
                allpinsset = False
                break
            pincheck = pincheck + 1

        if allpinsset:
            # This is an internal fudge so that we can display a warning if the pin is not set
            ADDON.setSetting("pinvalueset", "true")
        else:
            ADDON.setSetting("pinValueSet", "false")

        # Now we need to tidy up the user limits values
        numusers = Settings.getnumberoflimitedusers()
        clearuserpinnum = 5
        while numUsers < clearuserpinnum:
            log("SetPin: Clearing user pin %d" % clearuserpinnum)
            userid = "user%dPin" % clearuserpinnum
            usernameid = "%sName" % userid
            Settings.setuserpinvalue("", userid)

            # Set the user name to the default language specific one
            username = "%s %d" % (ADDON.getlocalizedstring(32036), clearuserpinnum)
            ADDON.setsetting(usernameid, username)
            clearuserpinnum = clearuserpinnum - 1
        # Also clear the unrestricted user if no user limit is being used
        if numUsers < 1:
            Settings.setuserpinvalue("", "unrestricteduserpin")

    @staticmethod
    def encryptpin(rawvalue):
        return hashlib.sha256(rawvalue).hexdigest()

    @staticmethod
    def ispinset(pinlevel=1):
        pinsettingsvalue = "pinValue"
        if pinlevel > 1:
            pinsettingsvalue = "%s%d" % (pinsettingsvalue, pinlevel)
        pinvalue = ADDON.getSetting(pinsettingsvalue)
        if pinvalue not in [None, ""]:
            return True
        return False

    @staticmethod
    def getpinlength():
        return int(float(ADDON.getSetting('pinlength')))

    @staticmethod
    def ispincorrect(inputpin, pinlevel=1):
        pinsettingsvalue = "pinvalue"
        if pinlevel > 1:
            pinsettingsvalue = "%s%d" % (pinsettingsvalue, pinlevel)
        # First encrypt the pin that has been passed in
        inputpinencrypt = Settings.encryptPin(inputPin)
        if inputpinencrypt == ADDON.getSetting(pinsettingsvalue):
            return True
        return False

    @staticmethod
    def isuserpincorrect(inputpin, pinid, blankiscorrect=True):
        # Make sure if the pin has not been set we do not lock the user out
        storedpin = ADDON.getSetting(pinId)
        if storedpin in [None, ""]:
            # Check if we are treating blank as a match to everything
            if blankiscorrect:
                return True
            else:
                return False

        # First encrypt the pin that has been passed in
        inputpinencrypt = Settings.encryptpin(inputpin)
        if inputpinencrypt == storedpin:
            return True
        return False

    @staticmethod
    def checkpinclash(newpin, pinlevel=1):
        # Check all the existing pins to make sure they are not the same
        pincheck = Settings.getNumberOfLevels()
        while pincheck > 0:
            if pincheck != pinlevel:
                if Settings.isPinSet(pincheck):
                    if Settings.isPinCorrect(newpin, pincheck):
                        # Found a matching pin, so report a clash
                        return True
            pincheck = pincheck - 1
        return False

    @staticmethod
    def checkuserpinclash(newpin, pinid):
        numusers = Settings.getNumberOfLimitedUsers()
        # Check all the existing pins to make sure they are not the same
        if (numusers > 0) and (pinId != 'unrestrictedUserPin'):
            if Settings.isUserPinCorrect(newpin, 'unrestrictedUserPin', False):
                return True
        if (numusers > 0) and (pinId != 'user1Pin'):
            if Settings.isUserPinCorrect(newpin, 'user1Pin', False):
                return True
        if (numusers > 1) and (pinId != 'user2Pin'):
            if Settings.isUserPinCorrect(newpin, 'user2Pin', False):
                return True
        if (numusers > 2) and (pinId != 'user3Pin'):
            if Settings.isUserPinCorrect(newpin, 'user3Pin', False):
                return True
        if (numusers > 3) and (pinId != 'user4Pin'):
            if Settings.isUserPinCorrect(newpin, 'user4Pin', False):
                return True
        if (numusers > 4) and (pinId != 'user5Pin'):
            if Settings.isUserPinCorrect(newpin, 'user5Pin', False):
                return True
        return False

    @staticmethod
    def getsecuritylevelforpin(inputpin):
        pincheck = Settings.getNumberOfLevels()
        apinset = False
        while pincheck > 0:
            if Settings.isPinSet(pincheck):
                apinset = True
                if Settings.isPinCorrect(inputPin, pincheck):
                    return pincheck
            pincheck = pincheck - 1
        # If no pins are set allow full access
        if not apinset:
            return 5
        return -1

    @staticmethod
    def getuserforpin(inputpin):
        numusers = Settings.getnumberoflimitedusers()
        # Check all the users to see if this pin matches any
        if numusers > 0:
            if Settings.isUserPinCorrect(inputpin, 'unrestrictedUserPin'):
                return 'unrestrictedUserPin'
            if Settings.isUserPinCorrect(inputpin, 'user1Pin'):
                return 'user1Pin'
        if numusers > 1:
            if Settings.isUserPinCorrect(inputpin, 'user2Pin'):
                return 'user2Pin'
        if numusers > 2:
            if Settings.isUserPinCorrect(inputpin, 'user3Pin'):
                return 'user3Pin'
        if numusers > 3:
            if Settings.isUserPinCorrect(inputpin, 'user4Pin'):
                return 'user4Pin'
        if numusers > 4:
            if Settings.isUserPinCorrect(inputpin, 'user5Pin'):
                return 'user5Pin'
        return None

    @staticmethod
    def getinvalidpinnotificationtype():
        return int(float(ADDON.getSetting('invalidPinNotificationType')))

    @staticmethod
    def ispinactive():
        # Check if the time restriction is enabled
        if ADDON.getSetting("timeRestrictionEnabled") != 'true':
            return True

        # Get the current time
        localtime = time.localtime()
        currenttime = (localtime.tm_hour * 60) + localtime.tm_min

        # Get the start time
        starttimestr = ADDON.getSetting("startTime")
        starttimesplit = starttimestr.split(':')
        starttime = (int(starttimesplit[0]) * 60) + int(starttimesplit[1])
        if starttime > currenttime:
            log("Pin not active until %s (%d) currently %d" % (starttimestr, starttime, currenttime))
            return False

        # Now check the end time
        endtimestr = ADDON.getSetting("endTime")
        endtimesplit = endtimestr.split(':')
        endtime = (int(endtimesplit[0]) * 60) + int(endtimesplit[1])
        if endtime < currenttime:
            log("Pin not active after %s (%d) currently %d" % (endtimestr, endtime, currenttime))
            return False

        log("Pin active between %s (%d) and %s (%d) currently %d" % (starttimestr, starttime, endtimestr, endtime, currenttime))
        return True

    @staticmethod
    def getpincachingenabledduration():
        cacheduration = 0
        cacheselection = int(ADDON.getSetting("pinCachingStatus"))
        if cacheselection == 0:
            # Cache is off
            cacheduration = 0
        elif cacheselection == 1:
            # Caching is on with no timeout
            cacheduration = -1
        elif cacheselection == 2:
            # Will time-out, so get the timeout time
            cacheduration = int(float(ADDON.getSetting("pinCachingDuration")))

        return cacheduration

    @staticmethod
    def isdirectionkeysaspin():
        return ADDON.getSetting("directionKeysAsPin") == 'true'

    @staticmethod
    def isdisplaybackground():
        return ADDON.getSetting("background") != "0"

    @staticmethod
    def getbackgroundimage():
        selectidx = ADDON.getSetting("background")
        if selectidx == "2":
            # PinSentry Fanart file as the BackgroundBrowser
            return ADDON.getAddonInfo('fanart')
        elif selectidx == "3":
            # Custom image selected, so return the value entered
            return ADDON.getSetting("backgroundImage")
        # If we reach here then there is no background image
        # or we want a black background
        return None

    @staticmethod
    def isactivevideoplaying():
        return ADDON.getSetting("activityvideoplaying") == 'true'

    @staticmethod
    def isactivenavigation():
        return ADDON.getSetting("activitynavigation") == 'true'

    @staticmethod
    def isactiveplugins():
        return ADDON.getSetting("activityplugins") == 'true'

    @staticmethod
    def isactivesystemsettings():
        return ADDON.getSetting("activitysystemsettings") == 'true'

    @staticmethod
    def isactiverepositories():
        return ADDON.getSetting("activityrepositories") == 'true'

    @staticmethod
    def isactivetvchannels():
        return ADDON.getSetting("activitytvchannels") == 'true'

    @staticmethod
    def isactivefilesource():
        return ADDON.getSetting("activityfilesource") == 'true'

    @staticmethod
    def isactivefilesourceplaying():
        return ADDON.getSetting("activityfilesourcenavigationonly") != 'true'

    @staticmethod
    def ispvrpausesupported():
        return ADDON.getSetting("pvrsupportspause") == 'true'

    @staticmethod
    def showsecuritylevelinplugin():
        if Settings.getnumberoflevels() < 2:
            return False
        return ADDON.getSetting("showSecurityInfo") == 'true'

    @staticmethod
    def issupportedmovieclassification(classification):
        for classificationitem in Settings.moviecassificationsnames:
            if classification == classificationitem['match']:
                return True
        return False

    @staticmethod
    def issupportedtvshowclassification(classification):
        for classificationitem in Settings.tvcassificationsnames:
            if classification == classificationitem['match']:
                return True
        return False

    @staticmethod
    def getdefaultmovieswithoutclassification():
        securityvalue = 0
        if ADDON.getSetting("defaultmovieswithoutclassification") != '0':
            securityvalue = 1
        return securityvalue

    @staticmethod
    def getdefaulttvshowswithoutclassification():
        securityvalue = 0
        if ADDON.getSetting("defaulttvshowswithoutclassification") != '0':
            securityvalue = 1
        return securityvalue

    @staticmethod
    def ishighlightclassificationunprotectedvideos():
        return ADDON.getSetting("highlightclassificationunprotectedvideos") == 'true'

    @staticmethod
    def ispromptforpinonstartup():
        return ADDON.getSetting("promptforpinonstartup") == 'true'

    @staticmethod
    def getnumberoflevels():
        return int(ADDON.getSetting("numberoflevels")) + 1

    @staticmethod
    def getsettingssecuritylevel():
        # The security level required to change the settings is the highest pin with a value set
        pincheck = Settings.getnumberoflevels()
        while pincheck > 0:
            if Settings.isPinSet(pincheck):
                return pincheck
            pincheck = pincheck - 1
        return -1

    @staticmethod
    def getnumberoflimitedusers():
        return int(ADDON.getSetting("numberoflimitedusers"))

    @staticmethod
    def getuserstarttime(userid):
        starttimetag = "%sStartTime" % userid
        # Get the start time
        starttimestr = ADDON.getSetting(starttimetag)
        starttimesplit = starttimestr.split(':')
        starttime = (int(starttimesplit[0]) * 60) + int(starttimesplit[1])
        return starttime, starttimestr

    @staticmethod
    def getuserendtime(userid):
        endtimetag = "%sEndTime" % userid
        # Get the end time
        endtimestr = ADDON.getSetting(endtimetag)
        endtimesplit = endtimestr.split(':')
        endtime = (int(endtimesplit[0]) * 60) + int(endtimesplit[1])
        return endtime, endtimestr

    @staticmethod
    def getuserviewinglimit(userid):
        viewinglimittag = "%sViewingLimit" % userid
        viewinglimit = int(ADDON.getSetting(viewinglimittag))
        return viewinglimit

    @staticmethod
    def getuserviewingusedtime(userid):
        lastlimitdatatag = "%sLastLimitData" % userid
        lastlimitdata = ADDON.getSetting(lastlimitdatatag)

        # Check to see if the last date that viewing limit was set is still today
        todaysdate = date.today().strftime("%d/%m/%y")

        # If not from today, then we have not used any for this user
        if todaysdate != lastlimitdata:
            return 0

        # Now check to see how much the user has already used today
        limitusedtag = "%sLimitUsed" % userid
        limitused = ADDON.getSetting(limitusedtag)

        if limitused in [None, ""]:
            return 0
        return int(limitused)

    @staticmethod
    def setuserviewingusedtime(userid, usedviewingtime):
        # Store the date when we last viewed something
        todaysdate = date.today().strftime("%d/%m/%y")
        lastlimitdatatag = "%sLastLimitData" % userid
        ADDON.setSetting(lastlimitdatatag, todaysdate)

        # Now store the amount of time we have used
        limitusedtag = "%sLimitUsed" % userid
        ADDON.setSetting(limitusedtag, str(usedviewingtime))

    @staticmethod
    def getwarnexpiringtime():
        return int(float(ADDON.getSetting('warnExpiringTime')))

    @staticmethod
    def getusername(userid):
        usernametag = "%sName" % userid
        return ADDON.getSetting(usernametag)
