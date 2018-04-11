#!/bin/bash
#
echo "ensur installed zsh!!!"


cd ~/
echo "install oh-my-zsh ...(ing)"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
echo "plugins=($plugins zpython) " >> ~/.zshrc

echo "You must ensure installed python3 and pip3!!!"
echo "install mroy-line and complete plugins"
pip3 install mroy-line
echo "fine !!!"
echo "try 'rp -s new'
echo "rp import url<tab>"
