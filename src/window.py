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


class IngredientModel(GObject.GObject):

    text = GObject.Property(type=str)
    quantity = GObject.Property(type=str)

    def __init__(self, ingredient: yuml.Ingredient):
        super().__init__()
        self.text = ingredient.text
        self.quantity = ingredient.quantity

    def __str__(self):
        return str(self.text)


class StepModel(GObject.GObject):

    text = GObject.Property(type=str)

    def __init__(self, step: yuml.Step):
        super().__init__()
        self.text = step.text

    def __str__(self):
        return str(self.text)


class VariantModel(GObject.GObject):

    text = GObject.Property(type=str)

    def __init__(self, variant: yuml.Variant):
        super().__init__()
        self.text = variant.text

    def __str__(self):
        return str(self.text)


@Gtk.Template(resource_path='/org/yumlrecipes/yumlrecipes/window.ui')
class YumlRecipesWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'YumlRecipesWindow'

    image = Gtk.Template.Child()
    label = Gtk.Template.Child()
    combobox = Gtk.Template.Child()
    listbox = Gtk.Template.Child()
    steplistbox = Gtk.Template.Child()
    variantlistbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Yuml Recipes')

    def show_title(self, title: str) -> None:
        self.set_title(title)
        self.label.set_text(title)

    def show_images(self, yuml_path: str, images: List[str]) -> None:
        abs_path = os.path.join(os.path.dirname(yuml_path), images[0])
        self.image.set_from_file(abs_path)

    def show_servings(self, servings: List[yuml.Serving]) -> None:
        for serving in servings:
            self.combobox.append_text(serving.text)

    def show_ingredients(self, ingredients: List[yuml.Ingredient]) -> None:
        def create_ingredient_entry(ingredient_model: IngredientModel):
            return Gtk.Label(label=f'{ingredient_model.text} - {ingredient_model.quantity}')

        ingredient_list_model = Gio.ListStore().new(IngredientModel)
        for ingredient in ingredients:
            ingredient_list_model.append(IngredientModel(ingredient))

        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.bind_model(ingredient_list_model, create_ingredient_entry)

    def show_steps(self, steps: List[yuml.Step]) -> None:
        def create_step_entry(step_model: StepModel):
            return Gtk.Label(label=step_model.text)

        step_list_model = Gio.ListStore().new(StepModel)
        for step in steps:
            step_list_model.append(StepModel(step))

        self.steplistbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.steplistbox.bind_model(step_list_model, create_step_entry)

    def show_variants(self, variants: List[yuml.Variant]) -> None:
        def create_variant_entry(variant_model: VariantModel):
            return Gtk.Label(label=variant_model.text)

        variant_list_model = Gio.ListStore().new(VariantModel)
        for variant in variants:
            variant_list_model.append(VariantModel(variant))

        self.variantlistbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.variantlistbox.bind_model(variant_list_model, create_variant_entry)

