#!/bin/sh

./export.sh

echo "---- install ----"
flatpak install --user \
                --noninteractive \
                _flatpak/staging/x86_64-main/org.yumlrecipes.yumlrecipes.flatpak

echo "---- run ----"
flatpak run org.yumlrecipes.yumlrecipes
