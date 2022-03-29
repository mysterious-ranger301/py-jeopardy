# py-jeopardy
A fully customizeable Jeopardy game made with Python and PyQt5!

Last update: 2022/03/28 (YYYY-MM-DD)

# What's new in update 22.03.28

 - Added save system (automatically saves when you close unfinished game)
 - Added ending (last update actually)
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

That's it! Now you can use this for any games you want!
