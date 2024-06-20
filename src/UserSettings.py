#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 14:53:00 2020

@author: fatih
"""

import configparser
from pathlib import Path

import distro

from Logger import Logger


class UserSettings(object):
    def __init__(self):
        self.userdistroid = distro.id()
        self.userdistroversion = distro.major_version().lower()
        self.usercodename = distro.codename().lower()
        if self.usercodename == "etap":
            self.usercodename = self.usercodename + self.userdistroversion
        self.userdistro = ", ".join(filter(bool, (distro.name(), distro.version(), distro.codename())))

        userhome = str(Path.home())
        self.username = userhome.rsplit("/", maxsplit=1)[-1]

        # The following config assignment are for backward compatibility
        self.configdir = os.getenv("XDG_CONFIG_HOME", userhome + "/.config") +  "/pardus-software/"
        # This is for the new versions
        if not os.path.exists(self.configdir):
            self.configdir = os.getenv("XDG_CONFIG_HOME", userhome + "/.config") +  "/pardus/pardus-software/"
        self.configfile = "settings.ini"
        self.config = configparser.ConfigParser(strict=False)
        self.config_usi = None
        self.config_ea = None
        self.config_saa = None
        self.config_hera = None
        self.config_icon = None
        self.config_sgc = None
        self.config_udt = None
        self.config_aptup = None
        self.config_lastaptup = None
        self.config_forceaptuptime = None

        self.cachedir = userhome + "/.cache/pardus-software/"

        self.Logger = Logger(__name__)

    def createDefaultConfig(self, force=False):
        self.config['DEFAULT'] = {'UseServerIcons': 'yes',
                                  'Animations': 'yes',
                                  'ShowAvailableApps': 'yes',
                                  'HideExternalRepoApps': 'yes',
                                  'IconName': 'default',
                                  'ShowGnomeComments': 'yes',
                                  'UseDarkTheme': 'no',
                                  'AutoAptUpdate': 'yes',
                                  'LastAutoAptUpdate': '0',
                                  'ForceAutoAptUpdateTime': '0'}

        if not Path.is_file(Path(self.configdir + self.configfile)) or force:
            if self.createDir(self.configdir):
                with open(self.configdir + self.configfile, "w") as cf:
                    self.config.write(cf)

    def readConfig(self):
        try:
            self.Logger.info("in readconfig")
            self.config.read(self.configdir + self.configfile)
            self.config_usi = self.config.getboolean('DEFAULT', 'UseServerIcons')
            self.config_ea = self.config.getboolean('DEFAULT', 'Animations')
            self.config_saa = self.config.getboolean('DEFAULT', 'ShowAvailableApps')
            self.config_hera = self.config.getboolean('DEFAULT', 'HideExternalRepoApps')
            self.config_icon = self.config.get('DEFAULT', 'IconName')
            self.config_sgc = self.config.getboolean('DEFAULT', 'ShowGnomeComments')
            self.config_udt = self.config.getboolean('DEFAULT', 'UseDarkTheme')
            self.config_aptup = self.config.getboolean('DEFAULT', 'AutoAptUpdate')
            self.config_lastaptup = self.config.getint('DEFAULT', 'LastAutoAptUpdate')
            self.config_forceaptuptime = self.config.getint('DEFAULT', 'ForceAutoAptUpdateTime')
        except Exception as e:
            self.Logger.warning("user config read error ! Trying create defaults")
            self.Logger.exception("{}".format(e))
            # if not read; try to create defaults
            self.config_usi = True
            self.config_ea = True
            self.config_saa = True
            self.config_hera = True
            self.config_icon = "default"
            self.config_sgc = True
            self.config_udt = False
            self.config_aptup = True
            self.config_lastaptup = 0
            self.config_forceaptuptime = 0
            try:
                self.createDefaultConfig(force=True)
            except Exception as e:
                self.Logger.warning("self.createDefaultConfig(force=True)")
                self.Logger.exception("{}".format(e))

    def writeConfig(self, srvicons, anims, avaiapps, extapps, iconname, gnomecom, darktheme, aptup, lastaptup, faptupt):
        self.config['DEFAULT'] = {'UseServerIcons': srvicons,
                                  'Animations': anims,
                                  'ShowAvailableApps': avaiapps,
                                  'HideExternalRepoApps': extapps,
                                  'IconName': iconname,
                                  'ShowGnomeComments': gnomecom,
                                  'UseDarkTheme': darktheme,
                                  'AutoAptUpdate': aptup,
                                  'LastAutoAptUpdate': lastaptup,
                                  'ForceAutoAptUpdateTime': faptupt}
        if self.createDir(self.configdir):
            with open(self.configdir + self.configfile, "w") as cf:
                self.config.write(cf)
                return True
        return False

    def createDir(self, dir):
        try:
            Path(dir).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.Logger.warning("{} : {}".format("mkdir error", dir))
            self.Logger.exception("{}".format(e))
            return False
