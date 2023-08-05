# qaffeine

Little tool that prevents your computer from entering inactivity modes. Can run in a terminal or in the notification area. Written in Python 3 and Qt 5.

Compatible with Linux, OS/X and Windows.

## Requirements

- Python 3
- PySide2
- pyautogui

## Usage

## Installation
### Using PIP

```
#pip install qaffeine
```

### Manually
Download this source and run qaffeine.py with Python 3.

### Command line

Syntax:
```
$ python qaffeine.py -h
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

Running 'python qaffeine.py' without any argument starts the graphical interface. Qaffeine then runs in the notification area.

![Screenshot](http://www.lorteau.fr/images/qaffeine_tray.png)

![Screenshot](http://www.lorteau.fr/images/qaffeine_settings.png)
