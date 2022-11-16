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

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw
from .window import YumlRecipesWindow


class YumlRecipesApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.yumlrecipes.yumlrecipes',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
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

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = YumlRecipesWindow(application=self)
        win.present()

        try:
            path = "/home/patrick/Chili con Carne.yuml"
            recipe = yuml.recipe_from_file(path)
            win.show_title(recipe.name)
            win.show_images(path, recipe.images)
            win.show_servings(recipe.servings)
            win.show_ingredients(recipe.ingredients)
            win.show_steps(recipe.steps)
            win.show_variants(recipe.variants)

        except yuml.YumlException as ex:
            win.set_title('Could not load *.yuml')
            print(str(ex))

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

