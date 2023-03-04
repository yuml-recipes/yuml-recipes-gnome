# main.py
#
# Copyright 2022 Patrick Eschenbach
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import gi
import yuml
from urllib import parse

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw
from .window import YumlRecipesWindow


class YumlRecipesApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.yumlrecipes.yumlrecipes',
                         flags=Gio.ApplicationFlags.HANDLES_OPEN)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.init_css()

    def init_css(self):
        css_resource_path = os.path.join(self.get_resource_base_path(), 'window.css')
        css_bytes = Gio.resources_lookup_data(css_resource_path, 0)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css_bytes.get_data())

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_open(self, files, hint, _):
        """Called when the application is opened with a file."""
        for file in files:
            self.do_activate(self.get_file_path(file))

    def do_activate(self, path: str = None):
        """Called when the application is activated."""
        win = YumlRecipesWindow(application=self)
        win.present()

        if path:
            self.open_recipe(win, path)
        else:
            path = self.choose_recipe(win)

    def open_recipe(self, win: YumlRecipesWindow, path: str):
        try:
            recipe = yuml.recipe_from_file(path)
            win.show_title(recipe.name)
            win.show_images(recipe.images)
            win.show_servings(recipe.servings)
            win.show_ingredients(recipe.ingredients)
            win.show_steps(recipe.steps)
            win.show_variants(recipe.variants)

        except yuml.YumlException as ex:
            win.show_title(f"Couldn't load {path}: {str(ex)}")
            print(str(ex))

    def choose_recipe(self, win: YumlRecipesWindow):
        chooser = Gtk.FileChooserNative(title=win.initial_title,
                                        transient_for=win,
                                        modal=True,
                                        action=Gtk.FileChooserAction.OPEN)
        file_filter = Gtk.FileFilter()
        file_filter.add_mime_type('application/x-yuml')
        chooser.add_filter(file_filter)
        def on_response(file_chooser, _):
            if file_chooser.get_file() is not None:
                file = file_chooser.get_file()
                self.open_recipe(win, self.get_file_path(file))
            else:
                sys.exit(0)
        chooser.connect("response", on_response)
        chooser.show()

    def get_file_path(self, file: Gio.File) -> str:
        path = parse.unquote(file.get_uri())
        schema = 'file://'
        if path.startswith(schema):
            path = path[len(schema):]
        return path

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Yuml Recipes',
                                application_icon='org.yumlrecipes.yumlrecipes',
                                developer_name='Patrick Eschenbach',
                                version='0.1.0',
                                developers=['Patrick Eschenbach'],
                                copyright='© 2022 Patrick Eschenbach')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = YumlRecipesApplication()
    return app.run(sys.argv)

