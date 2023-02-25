#!/bin/sh

echo "---- build-init ----"
flatpak build-init --update \
                   --type=app \
                   --arch=x86_64 \
                   _flatpak/staging/x86_64-main \
                   org.yumlrecipes.yumlrecipes \
                   org.gnome.Sdk \
                   org.gnome.Platform 43

echo "---- builder ----"
flatpak-builder --arch=x86_64 \
                --ccache \
                --force-clean \
                --disable-updates \
                --state-dir \
                _flatpak-builder \
                _flatpak/staging/x86_64-main \
                org.yumlrecipes.yumlrecipes.json
