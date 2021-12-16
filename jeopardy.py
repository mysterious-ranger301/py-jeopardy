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
from teamclass import Team
import os

catspath = os.path.join('.', 'headings.txt')
q_path = os.path.join('.', 'qs.txt')
anspath = os.path.join('.', 'ans.txt')
titlePath = os.path.join('.', 'title.txt')
teampath = os.path.join('.', 'teams.txt')


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


def extractTeams(path):
    f = open(path)
    c = f.read()
    f.close()
    return c.splitlines()

# FOLLOW THIS:
# q = questions[button.headingindex][button.questionindex]
# a = same thing ^-^


class mainWindow(QMW):
    def __init__(self, catspath, q_path, parent=None):
        super().__init__(parent)
        self.setupUi()  # main setup

    def setupUi(self):
        self.headings = extractHeadings(catspath)
        self.questions = extractQs(q_path)
        self.answers = extractAns(anspath)  # get info from files
        self.teamnames = extractTeams(teampath)
        self.makeTeams()

        self.container = QWidget(self)
        self.baselayout = QGL(self.container)  # setup layout

        self.font = QFont()
        self.font.setPointSize(20)
        self.font.setBold(True)
        self.font.setItalic(False)  # font we'll use

        self.label = QLabel(self)
        self.label.setFont(self.font)
        self.label.setText(extractTitle(titlePath))  # title!
        self.baselayout.addWidget(self.label, 0, 0)  # REMEMBER, Y THEN X

        self.cTeamLabel = QLabel(self)
        self.cTeamLabel.setFont(self.font)
        self.cTeamLabel.setText('Current team: ' + self.currentTeam.name)
        self.baselayout.addWidget(self.cTeamLabel, 0, 1)

        # add heading text
        self.layout = QGL(self)  # make sublayout
        for h in self.headings:  # set categories/headings
            exec('self.h_{0} = QLabel(self)'.format(h.replace(' ', '_').replace('(','').replace(')', '')))  # define
            exec('self.h_{0}.setFont(self.font)'.format(h.replace(' ', '_').replace('(','').replace(')', '')))
            exec('self.h_{0}.setText("|{1}")'.format(h.replace(' ', '_').replace('(','').replace(')', ''), h))
            exec(
                'self.layout.addWidget(self.h_{0}, 1, {1})'.format(
                    h.replace(' ', '_').replace('(','').replace(')', ''), self.headings.index(h)
                )
            )

        # something different :)
        for i in range(len(self.headings)):  # column
            for ii in range(2, 5 + 2):  # 5 questions (ii-1)
                setattr(self, 'b{0}_{1}'.format(i, ii - 1), QButton(self))
                button = getattr(self, 'b{0}_{1}'.format(i, ii - 1))
                button.setFont(self.font)
                button.setText(str(ii - 1) + '00')
                setattr(button, 'cat', i)
                setattr(button, 'q', ii - 1)
                button.clicked.connect(self.buttonhandle)
                self.layout.addWidget(button, ii, i)
                # print(ii, i)

        # make label for questions
        self.ql = QLabel(self)
        self.ql.setFont(self.font)
        self.ql.setText('')
        self.ql.hide()  # hide for now
        self.baselayout.addWidget(self.ql, 2, 0)  # add it

        # make button to view answer
        self.ansbtn = QButton(self)
        self.ansbtn.setFont(self.font)
        self.ansbtn.setText('View answer')
        self.ansbtn.clicked.connect(self.viewanswer)
        self.ansbtn.hide()  # hide for now
        self.baselayout.addWidget(self.ansbtn, 2, 1)

        # make button to give/deduct score for teams (right/wrong)
        self.rb = QButton(self)
        self.rb.setFont(self.font)
        self.rb.setText('Right')
        self.rb.hide()  # you don't want to see this for now
        self.rb.clicked.connect(self.rightHandler)
        self.baselayout.addWidget(self.rb, 2, 2)

        self.wb = QButton(self)
        self.wb.setFont(self.font)
        self.wb.setText('Wrong')
        self.wb.hide()
        self.wb.clicked.connect(self.wrongHandler)
        self.baselayout.addWidget(self.wb, 2, 3)

        self.baselayout.addLayout(self.layout, 1, 0)  # add sublayout

        self.teamlayout = QGL(self)
        # add team names and score for each team
        for team in self.teams:
#            label = QLabel(self)
#            label.setFont(self.font)
#            label.setText(team.name + ' - Score: {0}'.format(team.score))
            setattr(self, 'tlabel{0}'.format(self.teams.index(team)), QLabel(self))
            label = getattr(self, 'tlabel{0}'.format(self.teams.index(team)))
            label.setFont(self.font)
            label.setText(team.name + ' - Score: {0}'.format(team.score))
            self.teamlayout.addWidget(label, self.teams.index(team), 0)

        self.baselayout.addLayout(self.teamlayout, 3, 0)
        self.container.setLayout(self.baselayout)  # set main layout
        self.setCentralWidget(self.container)  # yeah do that
        self.setWindowTitle('Jeopardy!')  # window title
        self.show()  # obviously

    def buttonhandle(self):
        sender = self.sender()  # get sender (in this case always a button)
#        print('cat', sender.cat)
#        print('q', sender.q-1)
        sender.hide()  # hide the button so you can't click it twice
        self.currentq = (sender.cat, sender.q-1)  # set current question for self.viewanswer
        question = self.questions[sender.cat][sender.q-1]  # i hope this works
        self.ql.setText(question)  # set text for the viewer
        self.ql.show()  # show it
        self.currentscore = int(sender.text())

        self.ansbtn.show()  # also show the view answer button

    def viewanswer(self):
        self.ql.setText(self.answers[self.currentq[0]][self.currentq[1]])  # changes the question label to an answer label (wild i know)
        self.ansbtn.hide()
        self.rb.show()
        self.wb.show()

    def makeTeams(self):
        self.teams = []
        for team in self.teamnames:
            self.teams.append(Team(team))
        self.currentTeam = self.teams[0]

    def rightHandler(self):
        self.currentTeam.score += self.currentscore
        self.updateTeam()
        self.rb.hide()

    def wrongHandler(self):
        self.currentTeam.score -= self.currentscore
        self.updateTeam()
        self.wb.hide()

    def updateTeam(self):
        labelIndex = self.teams.index(self.currentTeam)
        label = getattr(self, 'tlabel{0}'.format(labelIndex))
        label.setText(self.currentTeam.name + ' - Score: ' + str(self.currentTeam.score))
        if labelIndex == len(self.teams) - 1:
            self.currentTeam = self.teams[0]
        else:
            self.currentTeam = self.teams[labelIndex + 1]
        self.cTeamLabel.setText('Current team: ' + self.currentTeam.name)
        self.rb.hide()
        self.wb.hide()

if __name__ == '__main__':
    app = QApp([])
    m = mainWindow(catspath, q_path)
#    print(m.headings)
#    print(m.questions)
    app.exec()
