# py-jeopardy
A fully customizeable Jeopardy game made with Python and PyQt5, now with Team Support!

Last update: 2022/03/27 (YYYY-MM-DD)

# What's new in update 22.03.27

 - Added Final Question
 - Added ending
 - Code is even messier, but it works!

# Setup
I assume you have Python installed, but if not, go to https://python.org and download Python.

During the installation process, make sure to check the "Add Python to PATH" checkbox to make things easier.

Anyways, we need some libraries in order to run this app. Open a Terminal (or command prompt, if you will :)

and type in _pip install PyQt5_. This will install PyQt5 for our program to use. If you're on Linux,

instead of _pip_ make sure to type in _pip3_.

That's it for libraries, now to customization.

# Customization
You may have noticed that there are files attached to this repository, and they serve a useful purpose.

_headings.txt_ names the categories of the Jeopardy questions.

NOTE: none of the headings can have special characters (-,+,", etc.)

_qs.txt_ names the questions for each category

Now this file (and _ans.txt_) in particular have a specific format you MUST follow in order to customize it:

_Start of file_

_Example question 1 through 5_

\n

\n

_Other questions 1 through 5_

_End of file_

(By the way \n means a newline)

Notice that? There _has to be 2 newlines in between the different questions in order for the program to read the file properly_. 

If you do not follow this format, the program will not work.

Anyways, here are the other files' meanings

_ans.txt_ names the answers to the questions in _qs.txt_ (there _has_ to be the same amount of questions as there is answers)

_title.txt_ names the title of the game

_final\_q\_a.txt_ has the final question and answer, question being on line 1, ans answer being on line 2

*Example Final Question*

*Example Final Answer*

If you're still confused, look at the example files you already have (you downloaded them with this).

# Launching
This is really simple, all you have to do is:

- Open a terminal in the file directory

- Type _py jeopardy.py_ for Windows and _python3 jeopardy.py_ for Linux

That's it! Now you can use this for any games you want!
