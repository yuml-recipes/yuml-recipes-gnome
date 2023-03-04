# Yuml Recipes

![build_workflow_badge](https://github.com/yuml-recipes/yuml-recipes-gnome/actions/workflows/build.yaml/badge.svg)

This is the GNOME application for Yuml Recipes. It opens *.yuml files by registering the application/x-yuml mimetype. Internally it uses the [Yuml Recipes Python Library](https://github.com/yuml-recipes/yuml-recipes-py).

## Preview

![Yuml Recipes Preview](preview/preview.png "Yuml Recipes Preview")

[See the corresponding 'Chili con Carne.yuml' file.](<preview/Chili con Carne.yuml>)

## Installation

### Install from GitHub release

1. Download the `org.yumlrecipes.yumlrecipes.flatpak` file from the latest release in GitHub
1. Run `flatpak install --user org.yumlrecipes.yumlrecipes.flatpak`

### Install from sources

1. Clone this repository
1. Run `./run` to install and start the application

## Roadmap

- Support for *.yuml files packaged with their images as ZIP file keeping the *.yuml extension
  - Export thumbnailer to give the zipped_recipe.yuml the thumbnail of its image, see [Flatpak thumbnailer feature request](https://github.com/flatpak/flatpak/issues/4923)

## Hints

### Manage mimetype from console

- Run `xdg-open filename.yuml` to run and get console output
- Run `xdg-mime default org.yumlrecipes.yumlrecipes.desktop application/x-yuml` to set as default

### Important locations for development

- ~/.local/share/flatpak/exports/share
- ~/.local/share/flatpak/exports/share/applications
- ~/.local/share/flatpak/exports/share/mime/packages
- /var/lib/flatpak/exports/share
- /var/lib/flatpak/exports/share/applications
- /var/lib/flatpak/exports/share/mime/packages

## Links

- [GTK 3 Python Reference](https://amolenaar.github.io/pgi-docgen/)
- [GTK 3 How Do I](https://wiki.gnome.org/HowDoI/Labels)
- [GTK 4 Widget Documentation](https://docs.gtk.org/gtk4/index.html)
- [GNOME Integration](https://developer.gnome.org/documentation/guidelines/maintainer/integrating.html?highlight=mime)
- [Flatpak PIP Generator](https://github.com/flatpak/flatpak-builder-tools/tree/master/pip)
- [Flatpak CI Docker Image](https://hub.docker.com/r/bilelmoussaoui/flatpak-github-actions)

## License

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

GPL-3.0

Copyright (c) 2023 Patrick Eschenbach

