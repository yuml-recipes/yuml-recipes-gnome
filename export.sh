#!/bin/sh

./build.sh

echo "---- build-export ----"
flatpak build-export --arch=x86_64 \
                     _flatpak/repo \
                     _flatpak/staging/x86_64-main \
                     main

echo "---- build-bundle ----"
flatpak build-bundle --arch=x86_64 \
                     _flatpak/repo \
                     _flatpak/staging/x86_64-main/org.yumlrecipes.yumlrecipes.flatpak \
                     org.yumlrecipes.yumlrecipes \
                     main
