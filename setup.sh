#sudo apt-get install qt4-qmake
#https://blog.csdn.net/u011008379/article/details/55299371
sudo apt-get install build-essential
sudo apt-get install qt4-dev-tools # qt4-doc qt4-qtconfig qt4-demos qt4-designer qtcreator
pip install pyside
pip install httplib2
pip install pygame
pip install evdev
pip install wget

WORKSPACE=$(cd `dirname $0`; pwd)

target_desktop="/usr/share/applications/niubility-word.desktop"
echo $target_desktop

if [ -f $target_desktop ]; then
   sudo rm $target_desktop
fi
sudo touch $target_desktop
sudo chmod 777 $target_desktop

sudo cat $WORKSPACE/res/nbword.desktop > $target_desktop
sudo echo "Exec=python2.7 ${WORKSPACE}/main.py" >> $target_desktop
sudo echo "Icon=${WORKSPACE}/res/app_icon.png" >> $target_desktop

#https://blog.csdn.net/u014025444/article/details/94024282
echo "--------------set desktop shortcut succeed !------------------------------"
sudo cat $target_desktop
echo "-------------------------------------------------------------------------"
