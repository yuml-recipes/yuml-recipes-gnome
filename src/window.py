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


class QuantityModel(GObject.GObject):
    quantity = GObject.Property(type=str)

    def __init__(self, quantity: str):
        super().__init__()
        self.quantity = quantity


class IngredientModel(GObject.GObject):
    text = GObject.Property(type=str)
    quantities = GObject.Property(type=str)

    def __init__(self, ingredient: yuml.Ingredient):
        super().__init__()
        self.text = ingredient.text
        self.quantities = ingredient.quantities


class StepModel(GObject.GObject):
    text = GObject.Property(type=str)

    def __init__(self, index: int, step: yuml.Step):
        super().__init__()
        self.index = f"{index + 1}."
        self.text = step.text


class VariantModel(GObject.GObject):
    text = GObject.Property(type=str)

    def __init__(self, variant: yuml.Variant):
        super().__init__()
        self.text = f"-  {variant.text}"


@Gtk.Template(resource_path='/org/yumlrecipes/yumlrecipes/window.ui')
class YumlRecipesWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'YumlRecipesWindow'

    image_frame = Gtk.Template.Child()
    image = Gtk.Template.Child()
    title = Gtk.Template.Child()
    ingredient_combobox = Gtk.Template.Child()
    ingredient_frame = Gtk.Template.Child()
    ingredient_label = Gtk.Template.Child()
    ingredient_listbox = Gtk.Template.Child()
    ingredient_quantity_listbox = Gtk.Template.Child()
    step_frame = Gtk.Template.Child()
    step_label = Gtk.Template.Child()
    step_listbox = Gtk.Template.Child()
    step_index_listbox = Gtk.Template.Child()
    variant_frame = Gtk.Template.Child()
    variant_label = Gtk.Template.Child()
    variant_listbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Yuml Recipes')
        self.ingredient_frame.set_label_align(0.5)
        self.ingredient_label.set_text(" Zutaten ")
        self.step_frame.set_label_align(0.5)
        self.step_label.set_text(" Zubereitung ")
        self.variant_frame.set_label_align(0.5)
        self.variant_label.set_text(" Varianten ")
        self.ingredient_combobox.connect('changed', self.__on_serving_changed)
        self.ingredients = None

        def create_quantity_entry(quantity_model: QuantityModel):
            entry = Gtk.Label(label=quantity_model.quantity)
            entry.set_halign(Gtk.Align.START)
            return entry

        self.quantity_list_model = Gio.ListStore().new(QuantityModel)
        self.ingredient_quantity_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.ingredient_quantity_listbox.bind_model(self.quantity_list_model, create_quantity_entry)

    def show_title(self, title: str) -> None:
        self.set_title(title)
        self.title.set_markup(f"<b>{title}</b>")

    def show_images(self, images: List[str]) -> None:
        if len(images) == 0:
            self.image_frame.set_visible(False)
            return

        self.image.set_filename(images[0])

    def show_servings(self, servings: List[yuml.Serving]) -> None:
        for serving in servings:
            self.ingredient_combobox.append_text(serving.text)
        if len(servings) == 0:
            self.ingredient_combobox.set_visible(False)
        elif len(servings) == 1:
            if servings[0].text:
                self.ingredient_combobox.set_sensitive(False)
            else:
                self.ingredient_combobox.set_visible(False)

    def __on_serving_changed(self, combobox):
        index = combobox.get_active()
        if index is None and self.ingredients is None:
            return
        self.quantity_list_model.remove_all()
        for ingredient in self.ingredients:
            quantity = ingredient.quantities[index]
            self.quantity_list_model.append(QuantityModel(quantity))

    def show_ingredients(self, ingredients: List[yuml.Ingredient]) -> None:
        def create_name_entry(ingredient_model: IngredientModel):
            entry = Gtk.Label(label=ingredient_model.text)
            entry.set_halign(Gtk.Align.END)
            return entry

        ingredient_list_model = Gio.ListStore().new(IngredientModel)
        for ingredient in ingredients:
            ingredient_list_model.append(IngredientModel(ingredient))

        self.ingredient_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.ingredient_listbox.bind_model(ingredient_list_model, create_name_entry)

        self.ingredients = ingredients
        self.ingredient_combobox.set_active(0)

    def show_steps(self, steps: List[yuml.Step]) -> None:
        if len(steps) == 0:
            self.step_frame.set_visible(False)
            return

        def create_index_entry(step_model: StepModel):
            entry = Gtk.Label(label=step_model.index)
            entry.set_halign(Gtk.Align.END)
            return entry
        def create_text_entry(step_model: StepModel):
            entry = Gtk.Label(label=step_model.text)
            entry.set_halign(Gtk.Align.START)
            return entry

        step_list_model = Gio.ListStore().new(StepModel)
        for step in steps:
            step_list_model.append(StepModel(step.index, step))

        self.step_index_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.step_index_listbox.bind_model(step_list_model, create_index_entry)
        self.step_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.step_listbox.bind_model(step_list_model, create_text_entry)

    def show_variants(self, variants: List[yuml.Variant]) -> None:
        if len(variants) == 0:
            self.variant_frame.set_visible(False)
            return

        def create_variant_entry(variant_model: VariantModel):
            entry = Gtk.Label(label=variant_model.text)
            entry.set_halign(Gtk.Align.START)
            return entry

        variant_list_model = Gio.ListStore().new(VariantModel)
        for variant in variants:
            variant_list_model.append(VariantModel(variant))

        self.variant_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.variant_listbox.bind_model(variant_list_model, create_variant_entry)

