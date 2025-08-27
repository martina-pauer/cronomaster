#!/usr/bin/bash
# Make a flatpak package with source in folder
flatpak_path="./"
flatpak_name="cronomaster"
conf_file=$flatpak_path"org.flatpak.cronomaster.yml"
build_folder=$flatpak_path"$flatpak_name-flatpak/"
repo=$flatpak_path"repo/"
timeout="3"

echo "Use $conf_file"
echo "for building flatpak package in $build_folder..."
sleep $timeout

echo "Build folder"
flatpak-builder --force-clean --user --install $build_folder $conf_file --repo=$repo
sleep $timeout

echo "Build bundle for make flatpak package in $flatpak_path"
flatpak build-bundle $repo "$flatpak_name.flatpak" "org.flatpak.$flatpak_name"
sleep $timeout

mv "$flatpak_name.flatpak" $flatpak_path
