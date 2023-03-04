# window.py
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

import yuml
import os
from gi.repository import Gtk, Gio, GObject, Adw
from typing import List


def create_left_entry(text: str):
    entry = Gtk.Label(label=text)
    entry.set_halign(Gtk.Align.END)
    entry.set_yalign(0.0)
    entry.set_selectable(True)
    return entry


def create_right_entry(text: str):
    entry = Gtk.Label(label=text)
    entry.add_css_class('yuml-right-entry')
    entry.set_justify(Gtk.Justification.FILL)
    entry.set_halign(Gtk.Align.FILL)
    entry.set_xalign(0.0)
    entry.set_hexpand(True)
    entry.set_wrap(True)
    entry.set_selectable(True)
    return entry


def attach_row(grid: Gtk.Grid, left: Gtk.Widget, right: Gtk.Widget, index: int):
    grid.attach(left, 0, index, 1, 1)
    grid.attach(right, 1, index, 1, 1)


def replace_row(grid: Gtk.Grid, left: Gtk.Widget, right: Gtk.Widget, index: int):
    cur_left = grid.get_child_at(0, index)
    cur_right = grid.get_child_at(1, index)
    if cur_left: grid.remove(cur_left)
    if cur_right: grid.remove(cur_right)
    attach_row(grid, left, right, index)


@Gtk.Template(resource_path='/org/yumlrecipes/yumlrecipes/window.ui')
class YumlRecipesWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'YumlRecipesWindow'

    scrolled_window = Gtk.Template.Child()
    content = Gtk.Template.Child()
    image_frame = Gtk.Template.Child()
    image = Gtk.Template.Child()
    title = Gtk.Template.Child()
    serving_combobox = Gtk.Template.Child()
    ingredient_frame = Gtk.Template.Child()
    ingredient_grid = Gtk.Template.Child()
    step_frame = Gtk.Template.Child()
    step_grid = Gtk.Template.Child()
    variant_frame = Gtk.Template.Child()
    variant_grid = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Yuml Recipes')
        self.serving_combobox.connect('changed', self.__on_serving_changed)
        self.initial_title = self.title.get_text()
        self.ingredients = []

    def show_title(self, title: str) -> None:
        self.set_title(title)
        self.title.set_markup(f"<b>{title}</b>")

    def show_images(self, images: List[str]) -> None:
        if len(images) == 0:
            self.image_frame.set_visible(False)
        else:
            self.image.set_filename(images[0])

    def show_servings(self, servings: List[yuml.Serving]) -> None:
        self.serving_combobox.set_visible(len(servings) > 0)
        empty_text = True
        for serving in servings:
            empty_text = empty_text and not bool(serving.text)
            self.serving_combobox.append_text(serving.text)
        if empty_text:
            self.serving_combobox.set_visible(False)
        elif len(servings) == 1:
            self.serving_combobox.set_sensitive(False)

    def __on_serving_changed(self, combobox: Gtk.ComboBoxText):
        index = combobox.get_active()
        if index is None:
            return
        for ingredient in self.ingredients:
            left = create_left_entry(ingredient.text)
            right = create_right_entry(ingredient.quantities[index])
            replace_row(self.ingredient_grid, left, right, ingredient.index + 1)

    def show_ingredients(self, ingredients: List[yuml.Ingredient]) -> None:
        self.ingredient_frame.set_visible(len(ingredients) > 0)
        self.ingredients = ingredients
        self.serving_combobox.set_active(0)

    def show_steps(self, steps: List[yuml.Step]) -> None:
        self.step_frame.set_visible(len(steps) > 0)
        for step in steps:
            left = create_left_entry(f"{step.index + 1}.")
            right = create_right_entry(step.text)
            attach_row(self.step_grid, left, right, step.index)

    def show_variants(self, variants: List[yuml.Variant]) -> None:
        self.variant_frame.set_visible(len(variants) > 0)
        for variant in variants:
            left = create_left_entry(f"-")
            right = create_right_entry(variant.text)
            attach_row(self.variant_grid, left, right, variant.index)

    def ensure_natural_height(self):
        def tick(widget, frame_clock, user_data):
            if self.count > 0:
                max_content_height = self.scrolled_window.get_max_content_height()
                allocated_content_height = self.content.get_allocated_height()
                min_content_height = min(max_content_height, allocated_content_height)
                self.scrolled_window.set_min_content_height(min_content_height)
            else:
                self.scrolled_window.add_tick_callback(tick, None)
                self.count = self.count + 1
        self.count = 0
        self.scrolled_window.add_tick_callback(tick, None)

