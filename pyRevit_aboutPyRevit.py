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

__doc__ = 'About pyRevit. Opens the pyRevit blog website. You can find detailed information on how pyRevit works, ' \
          'updates about the new tools and changes, and a lot of other information there.'

__window__.Close()

import clr
import os

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows


def get_repo_version():
    return '3.0.0-beta'


class aboutWindow:
    def __init__(self):
        # Create window
        self.my_window = System.Windows.Window()
        self.my_window.Title = 'About pyRevit'
        self.my_window.Width = 400
        self.my_window.Height = 300
        self.my_window.ResizeMode = System.Windows.ResizeMode.CanMinimize
        self.my_window.WindowStartupLocation = System.Windows.WindowStartupLocation.CenterScreen
        fontfam = System.Windows.Media.FontFamily('Myriad Pro Light')
        # fontfam = System.Windows.Media.FontFamily('not existing font test')

        # Create StackPanel to Layout UI elements
        self.my_stack = System.Windows.Controls.StackPanel()
        self.my_stack.Margin = System.Windows.Thickness(5)
        self.my_window.Content = self.my_stack

        self.reponame = System.Windows.Controls.Label()
        self.reponame.Content = 'pyRevit'
        self.reponame.FontFamily = fontfam
        self.reponame.FontSize = 32.0
        self.reponame.Margin = System.Windows.Thickness(30, 10, 30, 0)

        self.versionlabel = System.Windows.Controls.Label()
        self.versionlabel.Content = 'IronPython Scripts for Autodesk Revit®\nv {0}'.format(get_repo_version())
        self.versionlabel.FontFamily = fontfam
        self.versionlabel.FontSize = 16.0
        self.versionlabel.Margin = System.Windows.Thickness(30, -10, 30, 0)

        self.my_stack.Children.Add(self.reponame)
        self.my_stack.Children.Add(self.versionlabel)

        self.my_button_openwebsite = System.Windows.Controls.Button()
        self.my_button_openwebsite.Content = 'Open pyRevit website'
        self.my_button_openwebsite.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_button_openwebsite.Click += self.openwebsite
        self.my_button_openwebsite.Cursor = System.Windows.Input.Cursors.Hand

        self.my_button_opencredits = System.Windows.Controls.Button()
        self.my_button_opencredits.Content = 'Open Credits webpage'
        self.my_button_opencredits.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_button_opencredits.Click += self.opencredits
        self.my_button_opencredits.Cursor = System.Windows.Input.Cursors.Hand

        self.my_button_openrevisionhistory = System.Windows.Controls.Button()
        self.my_button_openrevisionhistory.Content = 'Open Revision History webpage'
        self.my_button_openrevisionhistory.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_button_openrevisionhistory.Click += self.openrevisionhistory
        self.my_button_openrevisionhistory.Cursor = System.Windows.Input.Cursors.Hand

        self.my_button_opengithubrepopage = System.Windows.Controls.Button()
        self.my_button_opengithubrepopage.Content = 'Open Github Repository for this library'
        self.my_button_opengithubrepopage.Margin = System.Windows.Thickness(30, 10, 30, 0)
        self.my_button_opengithubrepopage.Click += self.opengithubrepopage
        self.my_button_opengithubrepopage.Cursor = System.Windows.Input.Cursors.Hand

        self.my_stack.Children.Add(self.my_button_openwebsite)
        self.my_stack.Children.Add(self.my_button_opencredits)
        self.my_stack.Children.Add(self.my_button_openrevisionhistory)
        self.my_stack.Children.Add(self.my_button_opengithubrepopage)


    def openwebsite(self, sender, args):
        os.system('start http://eirannejad.github.io/pyRevit/')


    def opencredits(self, sender, args):
        os.system('start http://eirannejad.github.io/pyRevit/credits/')


    def openrevisionhistory(self, sender, args):
        os.system('start http://eirannejad.github.io/pyRevit/releasenotes/')


    def opengithubrepopage(self, sender, args):
        os.system('start https://github.com/eirannejad/pyRevit')


    def showwindow(self):
        self.my_window.ShowDialog()


aboutWindow().showwindow()
