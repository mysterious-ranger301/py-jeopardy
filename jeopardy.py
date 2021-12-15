#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:00:29 2021

@author: alexey
Jeopardy.py - a Jeopardy game made with PyQt5
"""

from PyQt5.QtWidgets import (
    QApplication as QApp,
    QMainWindow as QMW,
    QPushButton as QButton,
    QGridLayout as QGL,
    QWidget,
    QLabel,
)
from PyQt5.QtGui import QFont
import os

catspath = os.path.join('.', 'headings.txt')
q_path = os.path.join('.', 'qs.txt')
anspath = os.path.join('.', 'ans.txt')
titlePath = os.path.join('.', 'title.txt')


def extractHeadings(path):  # list
    f = open(path)
    content = f.read()
    f.close()
    return content.splitlines()


def extractQs(path):  # list of lists
    f = open(path)
    content = f.read()
    f.close()
    # format goes like this: *spam*\n\n*spam*\n\n
    # every \n\n is a separator, every \n is joining
    cats = content.split('\n\n')
    total = []
    for cat in cats:
        cat = cat.split('\n')
        if '' in cat:
            cat.remove('')
        total.append(cat)
    return total


def extractTitle(path):
    f = open(path)
    c = f.read()
    f.close()
    return c


def extractAns(path):
    f = open(path)
    content = f.read()
    f.close()

    cats = content.split('\n\n')
    total = []
    for cat in cats:
        cat = cat.split('\n')
        if '' in cat:
            cat.remove('')
        total.append(cat)
    return total

# FOLLOW THIS:
# q = questions[button.headingindex][button.questionindex]
# a = same thing ^-^


class mainWindow(QMW):
    def __init__(self, catspath, q_path, parent=None):
        super().__init__(parent)
        self.setupUi()
        # button code goes here

    def setupUi(self):
        self.headings = extractHeadings(catspath)
        self.questions = extractQs(q_path)
        self.answers = extractAns(anspath)
        self.container = QWidget(self)
        self.baselayout = QGL(self.container)
        self.font = QFont()
        self.font.setPointSize(20)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.label = QLabel(self)
        self.label.setFont(self.font)
        self.label.setText(extractTitle(titlePath))
        self.baselayout.addWidget(self.label, 0, 0)  # REMEMBER, Y THEN X
        # add heading text
        self.layout = QGL(self)
        for h in self.headings:
            exec('self.h_{0} = QLabel(self)'.format(h.replace(' ', '_').replace('(','').replace(')', '')))  # define
            exec('self.h_{0}.setFont(self.font)'.format(h.replace(' ', '_').replace('(','').replace(')', '')))
            exec('self.h_{0}.setText("|{1}")'.format(h.replace(' ', '_').replace('(','').replace(')', ''), h))
            exec(
                'self.layout.addWidget(self.h_{0}, 1, {1})'.format(
                    h.replace(' ', '_').replace('(','').replace(')', ''), self.headings.index(h)
                )
            )

        # something different :)
        for i in range(len(self.headings)):
            for ii in range(2, 5 + 2):  # 5 questions (ii-1)
                setattr(self, 'b{0}_{1}'.format(i, ii - 1), QButton(self))
                button = getattr(self, 'b{0}_{1}'.format(i, ii - 1))
                button.setFont(self.font)
                button.setText(str(ii - 1) + '00')
                setattr(button, 'cat', i)
                setattr(button, 'q', ii - 1)
                # TODO: fix this somehow ;)
                button.clicked.connect(self.buttonhandle)
                self.layout.addWidget(button, ii, i)
                # print(ii, i)

        # make label for questions
        self.ql = QLabel(self)
        self.ql.setFont(self.font)
        self.ql.setText('')
        self.ql.hide()
        self.baselayout.addWidget(self.ql, 2, 0)  # add it

        # make button to view answer
        self.ansbtn = QButton(self)
        self.ansbtn.setFont(self.font)
        self.ansbtn.setText('View answer')
        self.ansbtn.clicked.connect(self.viewanswer)
        self.ansbtn.hide()
        self.baselayout.addWidget(self.ansbtn, 2, 1)

        self.baselayout.addLayout(self.layout, 1, 0)
        self.container.setLayout(self.baselayout)
        self.setCentralWidget(self.container)
        self.setWindowTitle('Jeopardy!')  # window title
        self.show()

    def buttonhandle(self):
        sender = self.sender()
        print('cat', sender.cat)
        print('q', sender.q-1)
        sender.hide()
        self.currentq = (sender.cat, sender.q-1)
        question = self.questions[sender.cat][sender.q-1]  # i hope this works
        self.ql.setText(question)
        self.ql.show()

        self.ansbtn.show()

    def viewanswer(self):
        self.ql.setText(self.answers[self.currentq[0]][self.currentq[1]])

if __name__ == '__main__':
    app = QApp([])
    m = mainWindow(catspath, q_path)
    print(m.headings)
    print(m.questions)
    app.exec()
