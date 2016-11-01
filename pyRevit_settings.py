"""
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'Shows the preferences window for pyRevit. You can customize how pyRevit loads and set some basic ' \
          'parameters here.'

__window__.Close()

import clr
import os
import os.path as op
import ConfigParser as settingsParser

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReferenceByPartialName('System.Data')
import System.Windows

from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

logScriptUsage = None
archivelogfolder = None
verbose = None

initsectionname = 'init'
globalsectionname = 'global'

ADDIN_DLL_NAME = "RevitPythonLoader"
ADDIN_CLASSNAME = "RevitPythonLoaderApplication"
ADDIN_GUID = "7E37F14E-D840-42F8-8CA6-90FFC5497972"
ADDIN_DEF_FILENAME = 'pyRevit.addin'
ADDIN_VENDORID = 'eirannejad'

addinfilecontents =                                                                         \
'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'                                  \
 '<RevitAddIns>\n'                                                                          \
 '  <AddIn Type="Application">\n'                                                           \
 '    <Name>{addinname}</Name>\n'                                                           \
 '    <Assembly>{addinfolder}\\{addinname}.dll</Assembly>\n'                                \
 '    <AddInId>{addinguid}</AddInId>\n'                                                     \
 '    <FullClassName>{addinname}.{addinclassname}</FullClassName>\n'                             \
 '  <VendorId>{addinvendorid}</VendorId>\n'                                                      \
 '  </AddIn>\n'                                                                             \
 '</RevitAddIns>\n'


class ErrorWritingUserSettings(Exception):
    pass


class ErrorReadingUserSettings(Exception):
    pass


class MasterSettingsIsOverriding(Exception):
    pass


class settingsWindow:
    def __init__(self):
        # read config values

        global logScriptUsage
        global archivelogfolder
        global verbose
        
        # Create window
        self.my_window = System.Windows.Window()
        self.my_window.Title = 'pyRevit user settings'
        self.my_window.Width = 400
        self.my_window.Height = 400
        self.my_window.ResizeMode = System.Windows.ResizeMode.CanMinimize
        self.my_window.SizeToContent = System.Windows.SizeToContent.Height
        self.my_window.WindowStartupLocation = System.Windows.WindowStartupLocation.CenterScreen

        # Create StackPanel to Layout UI elements
        self.my_stack = System.Windows.Controls.StackPanel()
        self.my_stack.Margin = System.Windows.Thickness(5)
        self.my_window.Content = self.my_stack

        self.verboseCheckBox = System.Windows.Controls.CheckBox()
        self.verboseCheckBox.Content = 'Verbose reporting at Revit startup\nPrints a full report of all '             \
                                       'the scripts and tabs found\nand the corresponding buttons created in the UI.' \
                                       '\nThis is a very lengthy report and increases the load time,'                 \
                                       '\nbut it is very valuable for debugging.'
        self.verboseCheckBox.IsChecked = verbose
        self.verboseCheckBox.Margin = System.Windows.Thickness(30, 15, 30, 0)
        self.my_stack.Children.Add(self.verboseCheckBox)


        self.logScriptUsageCheckBox = System.Windows.Controls.CheckBox()
        self.logScriptUsageCheckBox.Content = 'Log script usage\nIf logging is active, pyRevit records '     \
                                              'each script run\nin a log under user temporary folder.\n'     \
                                              'pyRevit will create a log for every session and will '        \
                                              'copy\nthe previous session logs into the archive folder\n'    \
                                              'specified below, at each Revit startup.'
        self.logScriptUsageCheckBox.IsChecked = logScriptUsage
        self.logScriptUsageCheckBox.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_stack.Children.Add(self.logScriptUsageCheckBox)
        self.logScriptUsageCheckBox.Click += self.togglearchivefoldertextbox

        label = System.Windows.Controls.Label()
        label.Content = 'Archive log files to this folder:'
        label.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_textbox_archivelogfolder = System.Windows.Controls.TextBox()
        self.my_textbox_archivelogfolder.MaxLines = 1
        self.my_textbox_archivelogfolder.Text = archivelogfolder
        self.my_textbox_archivelogfolder.Margin = System.Windows.Thickness(30, 0, 30, 0)
        self.my_textbox_archivelogfolder.IsEnabled = True if logScriptUsage else False
        self.my_stack.Children.Add(label)
        self.my_stack.Children.Add(self.my_textbox_archivelogfolder)

        label = System.Windows.Controls.Label()
        label.Content = 'Activate pyRevit for:\n'                           \
                        '(Restart Revit for this change to take effect)'
        label.Margin = System.Windows.Thickness(30, 15, 30, 0)
        self.my_stack.Children.Add(label)
        
        self.rvtCheckboxes = {}
        revitversionspanel = System.Windows.Controls.WrapPanel()
        revitversionspanel.Margin = System.Windows.Thickness(30, 0, 30, 15)
        self.my_stack.Children.Add(revitversionspanel)
        for rvtversion in get_installed_revit_versions():
            if rvtversion.isdigit():
                self.revitVersionCheckbox = System.Windows.Controls.CheckBox()
                self.revitVersionCheckbox.Content = 'Revit {}'.format(rvtversion)
                self.revitVersionCheckbox.Margin = System.Windows.Thickness(0, 0, 10, 0)
                if addin_def_exists(rvtversion):
                    self.revitVersionCheckbox.IsChecked = True
                self.rvtCheckboxes[rvtversion] = self.revitVersionCheckbox
                revitversionspanel.Children.Add(self.revitVersionCheckbox)

        self.my_button_savesettings = System.Windows.Controls.Button()
        self.my_button_savesettings.Content = 'Save User Settings & Close'
        self.my_button_savesettings.Margin = System.Windows.Thickness(30, 10, 10, 30)
        self.my_button_savesettings.Click += self.savesettings
        self.my_stack.Children.Add(self.my_button_savesettings)

    def togglearchivefoldertextbox(self, sender, args):
        if self.logScriptUsageCheckBox.IsChecked:
            self.my_textbox_archivelogfolder.IsEnabled = True
        else:
            self.my_textbox_archivelogfolder.IsEnabled = False

    def savesettings(self, sender, args):
        global logScriptUsage
        global archivelogfolder
        global verbose
        
        verbose = self.verboseCheckBox.IsChecked
        logScriptUsage = self.logScriptUsageCheckBox.IsChecked
        archivelogfolder = self.my_textbox_archivelogfolder.Text
        
        checkedversions = []
        for revitversion, checkbox in self.rvtCheckboxes.items():
            if checkbox.IsChecked:
                checkedversions.append(revitversion)
        if len(checkedversions) == 0:
            res = TaskDialog.Show('pyRevit', 'You are disabling pyRevit for all Revit versions. If you make this '     \
                                             'change, pyRevit will not load under any Revit version and later you '    \
                                             'have to manually re-activate it. Are you sure?',
                                   TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.Cancel)
            if res == TaskDialogResult.Yes:
                TaskDialog.Show('pyRevit', 'Okay. To activate pyRevit later, go under the installation folder and ' \
                                           'run "makeAddins.bat" file. This will recreate the addin files for '     \
                                           'installed Revit versions.',
                                TaskDialogCommonButtons.Ok)
                toggle_addin_for(checkedversions)
        else:
            toggle_addin_for(checkedversions)
        
        save_user_settings()
        self.my_window.Close()

    def showwindow(self):
        self.my_window.ShowDialog()


def get_parent_directory(path):
    return op.dirname(path)


def get_install_dir():
    return get_parent_directory(get_parent_directory(get_parent_directory(__file__)))


def get_loader_clone_dir():
    return op.join(get_install_dir(), '__init__')


def find_revit_addin_directory():
    userappdatafolder = os.getenv('appdata')
    return op.join(userappdatafolder, "Autodesk", "Revit", "Addins")


def get_installed_revit_versions():
    revitaddinfolder = find_revit_addin_directory()
    return os.listdir(revitaddinfolder)


def addin_def_exists(revitversion):
    global ADDIN_DLL_NAME
    revitaddinfolder = find_revit_addin_directory()
    for fname in os.listdir(op.join(revitaddinfolder, revitversion)):
        if op.splitext(fname)[1].lower() == '.addin':
            fullfname = op.join(revitaddinfolder, revitversion, fname)
            with open(fullfname, 'r') as f:
                for line in f.readlines():
                    if (ADDIN_DLL_NAME + '.dll').lower() in line.lower():
                        return fullfname
    return False


def toggle_addin_for(revitversions):
    global ADDIN_DLL_NAME
    global ADDIN_CLASSNAME
    global ADDIN_GUID
    global ADDIN_DEF_FILENAME
    global ADDIN_VENDORID

    revitaddinfolder = find_revit_addin_directory()
    for revitversion in get_installed_revit_versions():
        if revitversion in revitversions:
            if addin_def_exists(revitversion):
                pass
            else:
                addin_definition_file = op.join(op.join(revitaddinfolder, revitversion, ADDIN_DEF_FILENAME))
                with open(addin_definition_file, 'w') as f:
                    f.writelines(addinfilecontents.format( addinname = ADDIN_DLL_NAME,               \
                                                           addinfolder = get_loader_clone_dir(),     \
                                                           addinguid = ADDIN_GUID,                   \
                                                           addinvendorid = ADDIN_VENDORID,           \
                                                           addinclassname = ADDIN_CLASSNAME))
        else:
            addinfile = addin_def_exists(revitversion)
            if addinfile:
                os.remove(addinfile)


#user config file functions
def find_user_configfile():
    # find the user config file
    userappdatafolder = os.getenv('appdata')
    pyrevituserappdatafolder = op.join(userappdatafolder, "pyRevit")
    return op.join(pyrevituserappdatafolder, "userdefaults.ini")


def load_user_settings():
    global logScriptUsage
    global archivelogfolder
    global verbose
    
    global initsectionname
    global globalsectionname
    
    configfile = find_user_configfile()

    # if the config file exists then read values and apply
    if op.exists(configfile):
        try:
            with open(configfile,'r') as udfile:
                cparser = settingsParser.ConfigParser()          
                cparser.readfp(udfile)
                logScriptUsageConfigValue = cparser.get(initsectionname, "logScriptUsage")
                logScriptUsage = True if logScriptUsageConfigValue.lower() == "true" else False
                archivelogfolder = cparser.get(initsectionname, "archivelogfolder")
                verbose = True if cparser.get(globalsectionname, "verbose").lower() == "true" else False
                
        except:
            raise ErrorReadingUserSettings
    else:
        raise MasterSettingsIsOverriding


def save_user_settings():
    global logScriptUsage
    global archivelogfolder
    global verbose
    
    global initsectionname
    global globalsectionname

    configfile = find_user_configfile()
    
    # if the config file exists then read values and apply
    if op.exists(configfile):
        try:
            with open(configfile,'w') as udfile:
                cparser = settingsParser.ConfigParser()
                cparser.add_section(globalsectionname)
                cparser.set(globalsectionname, "verbose", "true" if verbose else "false")
                cparser.add_section(initsectionname)
                cparser.set(initsectionname, "logScriptUsage", "true" if logScriptUsage else "false")
                cparser.set(initsectionname, "archivelogfolder", archivelogfolder)
                cparser.write(udfile)   
        except:
            raise ErrorWritingUserSettings
    else:
        raise MasterSettingsIsOverriding


try:
    load_user_settings()
    settingsWindow().showwindow()
except ErrorReadingUserSettings:
    TaskDialog.Show('pyRevit', 'Error reading settings file.')
except ErrorWritingUserSettings:
    TaskDialog.Show('pyRevit', 'Error writing settings file.')
except MasterSettingsIsOverriding:
    TaskDialog.Show('pyRevit', 'Settings are set by the master settings file and '\
                               'can not be changed from this window.')
