# qaffeine

Little tool that prevents your computer from entering inactivity modes. Can run in a terminal or in the notification area. Written in Python 3 and Qt 5.

Compatible with Linux, OS/X and Windows.

## Requirements

- Python 3
- PySide2
- pyautogui

## Installation
### Using PIP

```
#pip3 install qaffeine
```

This will pull the dependencies automatically.

### Using the setup.py supplied in the source tree
```
#python3 setup.py install
```

## Usage
### Command line

Syntax:
```
$ qaffeine-cli -h
usage: Prevent computer inactivity by simulating key presses
       [-h] [-n] [-d DELAY] [-k KEY] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -n, --nogui           Don't start a GUI, only a operate in text mode
  -d DELAY, --delay DELAY
                        Delay between key presses in seconds [default: 5] -
                        only valid with --nogui
  -k KEY, --key KEY     Key to press [default: altright]; see keys.txt for a
                        list of valid values - only valid with --nogui
  -v, --version         Show version number and exit
```

### GUI

Running qaffeine without any argument starts the graphical interface. Qaffeine then runs in the notification area.

![Screenshot](http://www.lorteau.fr/images/qaffeine_tray.png)

![Screenshot](http://www.lorteau.fr/images/qaffeine_settings.png)
