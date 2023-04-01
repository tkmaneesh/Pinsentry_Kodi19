# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import str
from builtins import object
import xbmc
import xbmcaddon
import xbmcvfs
import sqlite3
import xbmcgui

# Import the common settings
from .settings import log
from .settings import os_path_join

ADDON = xbmcaddon.Addon(id='script.pinsentry')


#################################
# Class to handle database access
#################################
class PinSentryDB(object):
    def __init__(self):
        # Start by getting the database location
        self.configPath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        self.databasefile = os_path_join(self.configPath, "pinsentry_database.db")
        log("PinSentryDB: Database file location = %s" % self.databasefile)
        # Check to make sure the DB has been created
        self._createDatabase()

    # Removes the database if it exists
    def cleandatabase(self):
        msg = "%s%s" % (ADDON.getLocalizedString(32113), "?")
        isyes = xbmcgui.Dialog().yesno(ADDON.getLocalizedString(32001), msg)
        if isYes:
            # If the database file exists, delete it
            if xbmcvfs.exists(self.databasefile):
                xbmcvfs.delete(self.databasefile)
                log("PinSentryDB: Removed database: %s" % self.databasefile)
            else:
                log("PinSentryDB: No database exists: %s" % self.databasefile)

    # Creates the database if the file does not already exist
    def _createdatabase(self):
        # Make sure the database does not already exist
        if not xbmcvfs.exists(self.databasefile):
            # Get a connection to the database, this will create the file
            conn = sqlite3.connect(self.databasefile)
            conn.text_factory = str
            c = conn.cursor()

            # Create the version number table, this is a simple table
            # that just holds the version details of what created it
            # It should make upgrade later easier
            c.execute('''CREATE TABLE version (version text primary key)''')

            # Insert a row for the version
            versionnum = "6"

            # Run the statement passing in an array with one value
            c.execute("INSERT INTO version VALUES (?)", (versionNum,))

            # Create a table that will be used to store each Video and its access level
            # The "id_" will be auto-generated as the primary key
            # Note: Index will automatically be created for "unique" values, so no
            # need to manually create them
            c.execute('''CREATE TABLE TvShows (id_ integer primary key, name text unique, dbid integer unique, level integer)''')
            c.execute('''CREATE TABLE Movies (id_ integer primary key, name text unique, dbid integer unique, level integer)''')
            c.execute('''CREATE TABLE MovieSets (id_ integer primary key, name text unique, dbid integer unique, level integer)''')
            c.execute('''CREATE TABLE Plugins (id_ integer primary key, name text unique, dbid text unique, level integer)''')
            c.execute('''CREATE TABLE Repositories (id_ integer primary key, name text unique, dbid text unique, level integer)''')

            # This is in version 2
            c.execute('''CREATE TABLE MusicVideos (id_ integer primary key, name text unique, dbid integer unique, level integer)''')

            # This is in version 3
            c.execute('''CREATE TABLE FileSources (id_ integer primary key, name text unique, dbid text unique, level integer)''')

            # This is in version 4
            c.execute('''CREATE TABLE ClassificationsMovies (id_ integer primary key, name text unique, dbid text, level integer)''')
            c.execute('''CREATE TABLE ClassificationsTV (id_ integer primary key, name text unique, dbid text, level integer)''')

            # This is in version 6
            c.execute('''CREATE TABLE TvChannels (id_ integer primary key, name text unique, dbid integer unique, level integer)''')

            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()

    # Creates or DB if it does not exist, or updates it if it does already exist
    def createorupdatedb(self):
        if not xbmcvfs.exists(self.databasefile):
            # No database created yet - nothing to do
            self._createDatabase()
            return

        # The database was already created, check to see if they need to be updated
        # Check if this is an upgrade
        conn = sqlite3.connect(self.databasefile)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('SELECT * FROM version')
        currentversion = int(c.fetchone()[0])
        log("PinSentryDB: Current version number in DB is: %d" % currentVersion)

        # If the database is at version one, add the version 2 tables
        if currentVersion < 2:
            log("PinSentryDB: Updating to version 2")
            # Add the tables that were added in version 2
            c.execute('''CREATE TABLE MusicVideos (id_ integer primary key, name text unique, dbid integer unique, level integer)''')
            # Update the new version of the database
            currentversion = 2
            c.execute('DELETE FROM version')
            c.execute("INSERT INTO version VALUES (?)", (currentVersion,))
            # Save (commit) the changes
            conn.commit()

        # If the database is at version two, add the version 3 tables
        if currentVersion < 3:
            log("PinSentryDB: Updating to version 3")
            # Add the tables that were added in version 3
            c.execute('''CREATE TABLE FileSources (id_ integer primary key, name text unique, dbid text unique, level integer)''')
            # Update the new version of the database
            currentversion = 3
            c.execute('DELETE FROM version')
            c.execute("INSERT INTO version VALUES (?)", (currentVersion,))
            # Save (commit) the changes
            conn.commit()

        # If the database is at version three, add the version 4 tables
        if currentVersion < 4:
            log("PinSentryDB: Updating to version 4")
            # Add the tables that were added in version 4
            c.execute('''CREATE TABLE ClassificationsMovies (id_ integer primary key, name text unique, dbid text, level integer)''')
            c.execute('''CREATE TABLE ClassificationsTV (id_ integer primary key, name text unique, dbid text, level integer)''')
            # Update the new version of the database
            currentversion = 4
            c.execute('DELETE FROM version')
            c.execute("INSERT INTO version VALUES (?)", (currentVersion,))
            # Save (commit) the changes
            conn.commit()

        # If the database is at version four, add the version 5 tables
        if currentversion < 5:
            log("PinSentryDB: Updating to version 5")
            # Add the tables that were added in version 5
            c.execute('''CREATE TABLE Repositories (id_ integer primary key, name text unique, dbid text unique, level integer)''')
            # Update the new version of the database
            currentversion = 5
            c.execute('DELETE FROM version')
            c.execute("INSERT INTO version VALUES (?)", (currentVersion,))
            # Save (commit) the changes
            conn.commit()

        # If the database is at version five, add the version 6 tables
        if currentversion < 6:
            log("PinSentryDB: Updating to version 6")
            # Add the tables that were added in version 6
            c.execute('''CREATE TABLE TvChannels (id_ integer primary key, name text unique, dbid integer unique, level integer)''')
            # Update the new version of the database
            currentversion = 6
            c.execute('DELETE FROM version')
            c.execute("INSERT INTO version VALUES (?)", (currentVersion,))
            # Save (commit) the changes
            conn.commit()

        conn.close()

    # Get a connection to the current database
    def getconnection(self):
        conn = sqlite3.connect(self.databasefile)
        conn.text_factory = str
        return conn

    # Set the security value for a given TvShow
    def settvshowsecuritylevel(self, showname, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("TvShows", showName, dbid, level)
        else:
            self._deleteSecurityDetails("TvShows", showName)
        return ret

    # Set the security value for a given Movie
    def setmoviesecuritylevel(self, moviename, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("Movies", moviename, dbid, level)
        else:
            self._deleteSecurityDetails("Movies", moviename)
        return ret

    # Set the security value for a given Movie Set
    def setmoviesetsecuritylevel(self, moviesetname, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("MovieSets", moviesetname, dbid, level)
        else:
            self._deleteSecurityDetails("MovieSets", moviesetname)
        return ret

    # Set the security value for a given Plugin
    def setpluginpecuritypevel(self, pluginname, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("Plugins", pluginname, dbid, level)
        else:
            self._deleteSecurityDetails("Plugins", pluginname)
        return ret

    # Set the security value for a given Repository
    def setrepositorysecuritylevel(self, reponame, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("Repositories", reponame, dbid, level)
        else:
            self._deleteSecurityDetails("Repositories", reponame)
        return ret

    # Set the security value for a given Music Video
    def setmusicvideosecuritylevel(self, musicvideoname, dbid, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("MusicVideos", musicvideoname, dbid, level)
        else:
            self._deleteSecurityDetails("MusicVideos", musicvideoname)
        return ret

    # Set the security value for a given File Source
    def setfilesourcesecuritylevel(self, sourcename, sourcepath, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("FileSources", sourcename, sourcepath, level)
        else:
            self._deleteSecurityDetails("FileSources", sourcename)
        return ret

    # Set the security value for a given Movie Classification
    def setmovieclassificationsecuritylevel(self, id_, match, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("ClassificationsMovies", id_, match, level)
        else:
            self._deleteSecurityDetails("ClassificationsMovies", id_)
        return ret

    # Set the security value for a given TV Classification
    def settvclassificationsecuritylevel(self, id_, match, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("ClassificationsTV", id_, match, level)
        else:
            self._deleteSecurityDetails("ClassificationsTV", id_)
        return ret

    # Set the security value for a given TV Channel
    def settvchannelsecuritylevel(self, channelname, id_, level=1):
        ret = -1
        if level != 0:
            ret = self._insertOrUpdate("TvChannels", channelname, id_, level)
        else:
            self._deleteSecurityDetails("TvChannels", channelname)
        return ret

    # Insert or replace an entry in the database
    def _insertorupdate(self, tablename, name, dbid, level=1):
        log("PinSentryDB: Adding %s %s (id_:%s) at level %d" % (tablename, name, str(dbid), level))

        # Get a connection to the DB
        conn = self.getConnection()
        c = conn.cursor()

        insertdata = (name, dbid, level)
        cmd = 'INSERT OR REPLACE INTO %s (name, dbid, level) VALUES (?,?,?)' % tablename
        c.execute(cmd, insertData)

        rowid = c.lastrowid
        conn.commit()
        conn.close()

        return rowId

    # Delete an entry from the database
    def _deletesecuritydetails(self, tablename, name):
        log("PinSentryDB: delete %s for %s" % (tablename, name))

        # Get a connection to the DB
        conn = self.getConnection()
        c = conn.cursor()
        # Delete any existing data from the database
        cmd = 'DELETE FROM %s where name = ?' % tableName
        c.execute(cmd, (name,))
        conn.commit()

        log("PinSentryDB: delete for %s removed %d rows" % (name, conn.total_changes))

        conn.close()

    # Get the security value for a given TvShow
    def gettvshowsecuritylevel(self, showname):
        return self._getSecurityLevel("TvShows", showname)

    # Get the security value for a given Movie
    def getmoviesecuritylevel(self, moviename):
        return self._getSecurityLevel("Movies", moviename)

    # Get the security value for a given Movie Set
    def getmoviesetsecuritylevel(self, moviesetname):
        return self._getSecurityLevel("MovieSets", moviesetname)

    # Get the security value for a given Plugin
    def getpluginsecuritylevel(self, pluginname):
        return self._getSecurityLevel("Plugins", pluginname)

    # Get the security value for a given Repository
    def getrepositorysecuritylevel(self, pluginname):
        return self._getSecurityLevel("Repositories", pluginname)

    # Get the security value for a given Music Video
    def getmusicvideosecuritylevel(self, musicvideoname):
        return self._getSecurityLevel("MusicVideos", musicvideoname)

    # Get the security value for a given File Source
    def getfilesourcesecuritylevel(self, sourcename):
        return self._getSecurityLevel("FileSources", sourcename)

    # Select the security entry from the database for a given File Source Path
    def getfilesourcesecuritylevelforpath(self, path):
        return self._getSecurityLevel("FileSources", path, 'dbid')

    # Get the security value for a given Movie Classification
    def getmovieclassificationsecuritylevel(self, classname):
        return self._getSecurityLevel("ClassificationsMovies", classname, 'dbid')

    # Get the security value for a given TV Classification
    def gettvclassificationsecuritylevel(self, classname):
        return self._getSecurityLevel("ClassificationsTV", classname, 'dbid')

    # Get the security value for a given TV Channel
    def gettvchannelssecuritylevel(self, channelname):
        return self._getSecurityLevel("TvChannels", channelname)

    # Select the security entry from the database
    def _getsecuritylevel(self, tablename, name, dbfield='name'):
        log("PinSentryDB: select %s for %s (dbfield=%s)" % (tablename, name, dbfield))

        # Get a connection to the DB
        conn = self.getConnection()
        c = conn.cursor()
        # Select any existing data from the database
        cmd = 'SELECT * FROM %s where %s = ?' % (tablename, dbfield)
        c.execute(cmd, (name,))
        row = c.fetchone()

        securitylevel = 0
        if row is None:
            log("PinSentryDB: No entry found in the database for %s" % name)
            # Not stored in the database so return 0 for no pin required
        else:
            log("PinSentryDB: Database info: %s" % str(row))

            # Return will contain
            # row[0] - Unique Index in the DB
            # row[1] - Name of the TvShow/Movie/MovieSet
            # row[2] - dbid
            # row[3] - Security Level
            securitylevel = row[3]

        conn.close()
        return securitylevel

    # Select all TvShow entries from the database
    def getalltvshowssecurity(self):
        return self._getAllSecurityDetails("TvShows")

    # Select all Movie entries from the database
    def getallmoviessecurity(self):
        return self._getAllSecurityDetails("Movies")

    # Select all Movie Set entries from the database
    def getallmoviesetssecurity(self):
        return self._getAllSecurityDetails("MovieSets")

    # Select all Plugin entries from the database
    def getallpluginssecurity(self):
        return self._getAllSecurityDetails("Plugins")

    # Select all Plugin entries from the database
    def getallrepositoriessecurity(self):
        return self._getAllSecurityDetails("Repositories")

    # Select all Music Video entries from the database
    def getallmusicvideossecurity(self):
        return self._getAllSecurityDetails("MusicVideos")

    # Select all File Sources entries from the database
    def getallfilesourcessecurity(self):
        return self._getAllSecurityDetails("FileSources")

    # Get All File Source Paths entries from the database
    def getallfilesourcespathssecurity(self):
        # The path is stored in the ID column, so use that as the key
        return self._getAllSecurityDetails("FileSources", keyCol=2)

    # Get All Movie Classification entries from the database
    def getallmovieclassificationsecurity(self, usecertkey=False):
        keycol = 1
        if usecertkey:
            keycol = 2
        return self._getAllSecurityDetails("ClassificationsMovies", keycol)

    # Get All TV Classification entries from the database
    def getalltvclassificationsecurity(self, usecertkey=False):
        keycol = 1
        if usecertkey:
            keycol = 2
        return self._getAllSecurityDetails("ClassificationsTV", keycol)

    # Get All File Source Paths entries from the database
    def getalltvchannelssecurity(self):
        # The path is stored in the ID column, so use that as the key
        return self._getAllSecurityDetails("TvChannels")

    # Select all security details from a given table in the database
    def _getallsecuritydetails(self, tablename, keycol=1):
        log("PinSentryDB: select all %s" % tableName)

        # Get a connection to the DB
        conn = self.getConnection()
        c = conn.cursor()
        # Select any existing data from the database
        cmd = 'SELECT * FROM %s' % tableName
        c.execute(cmd)
        rows = c.fetchall()

        resultdict = {}
        if rows is None:
            # No data
            log("PinSentryDB: No entry found in TvShow database")
        else:
            log("PinSentryDB: Database info: %s" % str(rows))

            # Return will contain
            # row[0] - Unique Index in the DB
            # row[1] - Name of the TvShow/Movie/MovieSet
            # row[2] - dbid
            # row[3] - Security Level
            for row in rows:
                name = row[keycol]
                resultDict[name] = row[3]

        conn.close()
        return resultDict
