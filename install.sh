#!/bin/bash
set -e

INSTALLATION_DIR="$HOME"/ABS

OUTPUT_PREFIX="ABS INSTALLER:"
OUTPUT_ERROR_PREFIX="$OUTPUT_PREFIX ERROR:"




git clone https://github.com/aleonal/ABS "$INSTALLATION_DIR"

cd "$INSTALLATION_DIR"

### Helper functions
#
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case $yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}

#Install platform specific dependencies
PYTHON_EXEC="python3"
OS_VERSION="UNKNOWN"
if lsb_release -c | grep -iq 'focal'; then
   OS_VERSION="ubuntu_focal"
   echo "Ubuntu Focal detected; adding repository for suricata"
   add-apt-repository ppa:oisf/suricata-stable
   apt-get update -y
   apt-get install suricata python3-tk -y
fi
if lsb_release -c | grep -q 'bionic'; then
   OS_VERSION="ubuntu_bionic" 
   echo "Ubuntu Bionic detected; adding repository for gcc-9"
   add-apt-repository ppa:ubuntu-toolchain-r/test
   apt-get update -y
   apt-get install gcc-9 python3-tk -y
fi
if lsb_release -c | grep -iq 'xenial'; then
   OS_VERSION="ubuntu_xenial"
   echo "Ubuntu Xenial detected; installing dependencies specific to OS"
   echo "adding repository for gcc-9"
   apt-get install libxcb-xinerama0 -y
   add-apt-repository ppa:ubuntu-toolchain-r/test
   apt-get update -y
   apt-get install gcc-9 python3-tk -y

fi

if lsb_release -d | grep -iq 'kali'; then
    if lsb_release -r | grep -q '2020'; then
        OS_VERSION="kali_2020"
        #works out of the box
    fi
    if lsb_release -r | grep -q '2019.2'; then
        OS_VERSION="kali_2019.2"
        echo "Kali 2019.2 detected; checking for OS specific dependencies"
        if apt-cache policy libgcc-8-dev | grep -q 'Installed: 8'; then
            echo "Kali 2019 does not work out of the box. Many dependent packages require updated libgcc."
            echo "You need to remove libgcc-8-dev and install libgcc-10-dev."
            if prompt_accepted_Yn "Run upgrade command? (May take a while)"; then
                apt-get -y update
                apt-get remove libgcc-8-dev
                apt-get install libgcc-10-dev
            else
                echo "Cannot install due to old version of libgcc"
                exit 1
            fi
        fi
    fi
fi

if echo $OS_VERSION | grep -q "UNKNOWN"; then
    echo "This version of Linux is currently not support."
    echo "Currently Supported:"
    echo "Ubuntu: Focal, Xenial"
    echo "Kali: 2019.2, 2020"
    exit 1
fi

# Updates
#echo "Running apt-get update"
#apt-get -y update
#echo "Running apt-get upgrade"
#apt-get upgrade

### Check if running as root
#
#if [ "$EUID" -ne 0 ]; then
#    echo "$OUTPUT_ERROR_PREFIX Please run this installation as root"
#    exit 1
#fi

### Install dependencies
#
REQUIRED_PROGRAMS="python3-pip python3-venv git"
REQUIRED_PYTHON_PACKAGES="PyQt5 Pyro4 Pillow pyautogui"
ECELD_DEPS="eceld eceld-wireshark"

# echo "$OUTPUT_PREFIX Installing Additional Dependencies"
# if [ -x "/usr/bin/apt-get" ]; then
#     OS_VERSION="Debian"
#     #sudo apt dist-upgrade
#     sudo apt-get -y install $REQUIRED_PROGRAMS
# elif [ -x "/usr/bin/yum" ]; then
#     OS_VERSION="CentOS"
#     yum install -y $REQUIRED_PROGRAMS
# else
#     echo "$OUTPUT_ERROR_PREFIX Distribution not supported"
#     exit 1
# fi



### Create virtualenv if it doesn't currently exist
echo "$OUTPUT_PREFIX Installing python dependencies"
if [ ! -d "venv" ]; then
    $PYTHON_EXEC -m venv venv
fi

source venv/bin/activate
pip install pip --upgrade
pip install $REQUIRED_PYTHON_PACKAGES

### Creating executable

echo "Creating runner"
cat > "$INSTALLATION_DIR"/abs-gui <<EOFabs-gui
#!/bin/bash
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case \$yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}


ECEL_NETSYS_DIR="\$(find /home/kali -type d -name "eceld-netsys" )"
if [ "\$EUID" -ne 0 ]; then
echo "ECELD-NETSYS must be run as root"
exit 1
fi

cd "\$ECEL_NETSYS_DIR"
if pyro4-nsc list | grep -iq 'ecel.service'; then
   if prompt_accepted_Yn "ECELd service already running, restart the service?"; then
      echo ***** Removing Service *****
      pyro4-nsc remove ecel.service
      pkill eceld_service -f
      pkill pyro4 -f
      echo ***** Starting Service, roughly ~5 seconds *****
     ./eceld/eceld_service &
      sleep 0.1
   fi
else
   echo *****Starting Service, roughly ~5 seconds
   ./eceld/eceld_service &
   sleep 0.1
fi

ABS_DIR=$INSTALLATION_DIR
cd "\$ABS_DIR"
echo \$PWD

venv/bin/python3 main.py
EOFabs-gui


### Creating shortcut

echo "Creating shortcut"
cat > ~/Desktop/ABS.desktop <<EOFabs.desktop
[Desktop Entry]
Name=Agent Build System 
StartupABSClass=Abs
Comment=ABS Launcher
GenericName=ABS UI
Exec=sudo $INSTALLATION_DIR/abs-gui
Icon=$INSTALLATION_DIR/UI/A.png
Type=Application
Categories=System;GUIDesigner;
MimeType=image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;application/x-python-code;text/x-python;application/json;image/png;
Keywords=ABS;Agent;BuildSystem;

Path= $INSTALLATION_DIR
Terminal=true
StartupNotify=false

EOFabs.desktop


chmod +x "$INSTALLATION_DIR"/abs-gui
chmod +x ~/Desktop/ABS.desktop
chmod +x "$INSTALLATION_DIR"/main.py
echo
echo "***************************************************"
echo "Installation Complete"

