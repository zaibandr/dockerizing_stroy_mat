#!/usr/bin/env bash
sudo apt-add-repository ppa:fish-shell/release-2
sudo apt update
sudo apt install fish
chsh -s /usr/bin/fish