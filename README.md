# Yuml Recipes

![build_workflow_badge](https://github.com/yuml-recipes/yuml-recipes-gnome/actions/workflows/build.yaml/badge.svg)

This is the GNOME application for Yuml Recipes. It opens *.yuml files by registering the application/x-yuml mimetype. Internally it uses the [Yuml Recipes Python Library](https://github.com/yuml-recipes/yuml-recipes-py).

## Preview

![Yuml Recipes Preview](preview/preview.png "Yuml Recipes Preview")

## Installation

### Install from GitHub release

1. Download the `org.yumlrecipes.yumlrecipes.flatpak` file from the latest release in GitHub
1. Run `flatpak install --user org.yumlrecipes.yumlrecipes.flatpak`

### Install from sources

1. Clone this repository
1. Run `./run` to install and start the application

## Hints

### Open by mimetype from console

Run `xdg-open filename.yuml` to get console output.

### Important locations for development

- ~/.local/share/flatpak/exports/share
- ~/.local/share/flatpak/exports/share/applications
- ~/.local/share/flatpak/exports/share/mime/packages
- /var/lib/flatpak/exports/share
- /var/lib/flatpak/exports/share/applications
- /var/lib/flatpak/exports/share/mime/packages

## Links

- [Flatpak PIP Generator](https://github.com/flatpak/flatpak-builder-tools/tree/master/pip)
- [Flatpak CI Docker Image](https://hub.docker.com/r/bilelmoussaoui/flatpak-github-actions)
- [GTK4 Widget Documentation](https://docs.gtk.org/gtk4/index.html)
- [GNOME Integration](https://developer.gnome.org/documentation/guidelines/maintainer/integrating.html?highlight=mime)

## License

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

GPL-3.0

Copyright (c) 2022 Patrick Eschenbach

