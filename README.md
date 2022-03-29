# py-jeopardy
A fully customizeable Jeopardy game made with Python and PyQt5!

Last update: 2022/03/28 (YYYY-MM-DD)

# What's new in update 22.03.28

 - Added save system (automatically saves when you close unfinished game)
 - Added ending (last update actually, oops)
 - Remade configuration system (it's 2 files now instead of 6 or something)

# Setup
I assume you have Python installed, but if not, go to https://python.org and download Python.

During the installation process, make sure to check the "Add Python to PATH" checkbox to make things easier.

Anyways, we need some libraries in order to run this app. Open a Terminal (or command prompt, if you will :)

and type in _pip install PyQt5_. This will install PyQt5 for our program to use. If you're on Linux,

instead of _pip_ make sure to type in _pip3_.

That's it for libraries, now to customization.

# Customization

Most of the configuration is stored in _config.json_. Now, if you don't know how to

edit JSON files, I recommend you google it or check the included _config.json_.

Team names are stored in _teams.txt_. Each team name is on each line (again, check included files).

# Launching
This is really simple, all you have to do is:

- Open a terminal in the file directory

- Type _py jeopardy.py_ for Windows and _python3 jeopardy.py_ for Linux

If this doesn't work on Windows, try the next optional step.

# Compiling to an EXE (Optional, Windows Only)

If you want to shorten the launching process (I do), then you can compile this into

an exe file (if you're on Windows). All you have to do is:

1 - Open CMD (press Win+R and type _cmd_)

2 - Change directory to where the .py file is located (cd _c:\path\to\your\py\file_, mine is _C:\Users\name\Downloads\py-jeopardy-main_)

3 - Execute _pyinstaller_. Type into CMD: _pyinstaller --onefile jeopardy.py_

This will compile the program into an exe. If there's an error such as "pyinstaller is not recognized as a command", then type

_pip install pyinstaller_ and try again.

I assume you have added Python to PATH, right? If you haven't, go to Start -> Search -> and type "Edit system environment variables"

Then click Environment Variables, double-click PATH, click New, and type your Python Scripts directory (usually _C:\PythonDirectory\Scripts_)

Click save, and you're done. Then you can repeat the above steps to compile the program into an exe file.

If you're lost or something doesn't work, open up an issue and I'd be happy to help you!
