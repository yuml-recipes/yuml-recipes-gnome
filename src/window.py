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


class ListModel(GObject.GObject):

    def __init__(self, text: str, align: Gtk.Align):
        super().__init__()
        self.text = text
        self.align = align


@Gtk.Template(resource_path='/org/yumlrecipes/yumlrecipes/window.ui')
class YumlRecipesWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'YumlRecipesWindow'

    image_frame = Gtk.Template.Child()
    image = Gtk.Template.Child()
    title = Gtk.Template.Child()
    serving_combobox = Gtk.Template.Child()
    ingredient_frame = Gtk.Template.Child()
    ingredient_listbox = Gtk.Template.Child()
    ingredient_quantity_listbox = Gtk.Template.Child()
    step_frame = Gtk.Template.Child()
    step_listbox = Gtk.Template.Child()
    step_index_listbox = Gtk.Template.Child()
    variant_frame = Gtk.Template.Child()
    variant_listbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Yuml Recipes')
        self.serving_combobox.connect('changed', self.__on_serving_changed)
        self.ingredients = None

        def create_entry(list_model: ListModel):
            entry = Gtk.Label(label=list_model.text)
            entry.set_halign(list_model.align)
            return entry

        self.ingredient_list_model = Gio.ListStore().new(ListModel)
        self.ingredient_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.ingredient_listbox.bind_model(self.ingredient_list_model, create_entry)

        self.ingredient_quantity_list_model = Gio.ListStore().new(ListModel)
        self.ingredient_quantity_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.ingredient_quantity_listbox.bind_model(self.ingredient_quantity_list_model, create_entry)

        self.step_list_model = Gio.ListStore().new(ListModel)
        self.step_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.step_listbox.bind_model(self.step_list_model, create_entry)

        self.step_index_list_model = Gio.ListStore().new(ListModel)
        self.step_index_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.step_index_listbox.bind_model(self.step_index_list_model, create_entry)

        self.variant_list_model = Gio.ListStore().new(ListModel)
        self.variant_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.variant_listbox.bind_model(self.variant_list_model, create_entry)

    def show_title(self, title: str) -> None:
        self.set_title(title)
        self.title.set_markup(f"<b>{title}</b>")

    def show_images(self, images: List[str]) -> None:
        if len(images) == 0:
            self.image_frame.set_visible(False)
        else:
            self.image.set_filename(images[0])

    def show_servings(self, servings: List[yuml.Serving]) -> None:
        if len(servings) == 0:
            self.serving_combobox.set_visible(False)
        else:
            empty_text = True
            for serving in servings:
                empty_text = empty_text and not bool(serving.text)
                self.serving_combobox.append_text(serving.text)
            if empty_text:
                self.serving_combobox.set_visible(False)
            elif len(servings) == 1:
                self.serving_combobox.set_sensitive(False)

    def __on_serving_changed(self, combobox):
        index = combobox.get_active()
        if index is None and self.ingredients is None:
            return
        self.ingredient_quantity_list_model.remove_all()
        for ingredient in self.ingredients:
            quantity = ingredient.quantities[index]
            self.ingredient_quantity_list_model.append(ListModel(quantity, Gtk.Align.START))

    def show_ingredients(self, ingredients: List[yuml.Ingredient]) -> None:
        self.ingredient_list_model.remove_all()
        if len(ingredients) == 0:
            self.ingredient_frame.set_visible(False)
        else:
            for ingredient in ingredients:
                self.ingredient_list_model.append(ListModel(ingredient.text, Gtk.Align.END))
        self.ingredients = ingredients
        self.serving_combobox.set_active(0)

    def show_steps(self, steps: List[yuml.Step]) -> None:
        self.step_list_model.remove_all()
        self.step_index_list_model.remove_all()
        if len(steps) == 0:
            self.step_frame.set_visible(False)
        else:
            for step in steps:
                self.step_list_model.append(ListModel(step.text, Gtk.Align.START))
                self.step_index_list_model.append(ListModel(f"{step.index + 1}.", Gtk.Align.END))

    def show_variants(self, variants: List[yuml.Variant]) -> None:
        self.variant_list_model.remove_all()
        if len(variants) == 0:
            self.variant_frame.set_visible(False)
        else:
            for variant in variants:
                self.variant_list_model.append(ListModel(f"-  {variant.text}", Gtk.Align.START))
