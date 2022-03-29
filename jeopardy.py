#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:00:29 2021

@author: alexey
Jeopardy.py - a Jeopardy game made with PyQt5
Version 22.03.28
"""

from PyQt5.QtWidgets import (
    QApplication as QApp,
    QMainWindow as QMW,
    QPushButton as QButton,
    QGridLayout as QGL,
    QWidget,
    QLabel,
    QInputDialog,
    QMessageBox
)
from PyQt5.QtGui import QFont
from teamclass import Team
import os
import json

# catspath = os.path.join('.', 'headings.txt')
# q_path = os.path.join('.', 'qs.txt')
# anspath = os.path.join('.', 'ans.txt')
# titlePath = os.path.join('.', 'title.txt')
teampath = os.path.join('.', 'teams.txt')
# finalqpath = os.path.join('.', 'final_q_a.txt')
configpath = os.path.join('.', 'config.json')

def extractTeams(path):
    f = open(path)
    c = f.read()
    f.close()
    return c.splitlines()

def getConfig(path='config.json'):
    config = json.loads(open(path).read()) # read file
    # returns list, i0 is title, i1 is list of headings, 
    # i2 is qs, i3 is ans, i4 is final q/a
    total = []
    total.append(config['title'])
    
    headings = []
    for k, v in config.items():
        if k == 'title' or k == 'final': continue # we dont want this
        headings.append(k)
    total.append(headings)
    
    qs = []
    ans = []
    for h in headings:
        questions = config[h]
        hqs = []
        has = []
        for qu, an in questions.items():
            hqs.append(qu)
            has.append(an)
        qs.append(hqs)
        ans.append(has)
    
    total.append(qs)
    total.append(ans)
    # total.append([qs])
    # total.append([ans])
    
    final = []
    
    for fq, fa in config['final'].items():
        final.append(fq)
        final.append(fa)
    total.append(final)
    
    return total

# FOLLOW THIS:
# q = questions[button.headingindex][button.questionindex]
# a = same thing ^-^


class mainWindow(QMW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()  # main setup

    def setupUi(self):
        # self.headings = extractHeadings(catspath)
        # self.questions = extractQs(q_path)
        # self.finalq = extractFQ(finalqpath)
        # self.answers = extractAns(anspath)  # get info from files
        config = getConfig(configpath)
        # print(config)
        self.headings = config[1]
        self.questions = config[2]
        self.answers = config[3]
        self.finalq = config[4]
        
        self.clickedbs = []
        
        self.save_exists = False
        if os.path.exists('save.json'):
            load = QMessageBox().question(self, 'Load', 'save.json was found. Load game from it?', QMessageBox.Yes, QMessageBox.No)
            if load == QMessageBox.Yes:
                self.save_exists = True
                print('save exists')
        
        if self.save_exists:
            data = json.loads(open('save.json').read())
            self.clickedbs = data['clicked']
        
        self.gamedone = False
        
        self.teamnames = extractTeams(teampath)
        self.makeTeams()
        
        self.fqactivated = False

        self.container = QWidget(self)
        self.baselayout = QGL(self.container)  # setup layout

        self.font = QFont()
        self.font.setPointSize(11)
        self.font.setBold(True)
        self.font.setItalic(False)  # font we'll use

        self.label = QLabel(self)
        self.label.setFont(self.font)
        self.label.setText(config[0])  # title!
        self.baselayout.addWidget(self.label, 0, 0)  # REMEMBER, Y THEN X

        self.cTeamLabel = QLabel(self)
        self.cTeamLabel.setFont(self.font)
        self.cTeamLabel.setText('Current team: ' + self.currentTeam.name)
        self.baselayout.addWidget(self.cTeamLabel, 0, 1)

        # add heading text
        self.layout = QGL(self)  # make sublayout
        for h in self.headings:  # set categories/headings (wtf is this)
            exec(
                'self.h_{0} = QLabel(self)'.format(
                    h.replace(' ', '_').replace('(', '').replace(')', '')
                )
            )  # define
            exec(
                'self.h_{0}.setFont(self.font)'.format(
                    h.replace(' ', '_').replace('(', '').replace(')', '')
                )
            )
            exec(
                'self.h_{0}.setText("|{1}")'.format(
                    h.replace(' ', '_').replace('(', '').replace(')', ''), h
                )
            )
            exec(
                'self.layout.addWidget(self.h_{0}, 1, {1})'.format(
                    h.replace(' ', '_').replace('(', '').replace(')', ''),
                    self.headings.index(h),
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
                if self.save_exists:
                    data = json.loads(open('save.json').read())
                    # print(data['clicked'])
                    if [button.cat, button.q-1] in data['clicked']:
                        button.hide()
                # print(ii, i)

        # make label for questions
        self.ql = QLabel(self)
        self.ql.setFont(self.font)
        self.ql.setText('')
        self.ql.hide()  # hide for now
        self.baselayout.addWidget(self.ql, 2, 0)  # add it

        # special button to view answer for final question
        self.fqansbtn = QButton(self)
        self.fqansbtn.setFont(self.font)
        self.fqansbtn.setText('View Final Answer')
        self.fqansbtn.clicked.connect(self.fqview)
        self.fqansbtn.hide()
        self.baselayout.addWidget(self.fqansbtn, 2, 1)

        # make button to view answer
        self.ansbtn = QButton(self)
        self.ansbtn.setFont(self.font)
        self.ansbtn.setText('View answer')
        self.ansbtn.clicked.connect(self.viewanswer)
        self.ansbtn.hide()  # hide for now
        self.baselayout.addWidget(self.ansbtn, 2, 2)

        # make button to give/deduct score for teams (right/wrong)
        self.rb = QButton(self)
        self.rb.setFont(self.font)
        self.rb.setText('Right')
        self.rb.hide()  # you don't want to see this for now
        self.rb.clicked.connect(self.rightHandler)
        self.baselayout.addWidget(self.rb, 2, 3)

        self.wb = QButton(self)
        self.wb.setFont(self.font)
        self.wb.setText('Wrong')
        self.wb.hide()
        self.wb.clicked.connect(self.wrongHandler)
        self.baselayout.addWidget(self.wb, 2, 4)

        self.baselayout.addLayout(self.layout, 1, 0)  # add sublayout

        self.fqbutton = QButton(self)
        self.fqbutton.setFont(self.font)
        self.fqbutton.setText('Final Question')
        self.fqbutton.show()
        self.fqbutton.clicked.connect(self.fq)
        self.baselayout.addWidget(self.fqbutton, 3, 0)
        

        self.teamlayout = QGL(self)
        # add team names and score for each team
        for team in self.teams:
            setattr(self, 'tlabel{0}'.format(self.teams.index(team)), QLabel(self))
            label = getattr(self, 'tlabel{0}'.format(self.teams.index(team)))
            label.setFont(self.font)
            label.setText(team.name + ' - Score: {0}'.format(team.score))
            self.teamlayout.addWidget(label, self.teams.index(team), 0)

        self.baselayout.addLayout(self.teamlayout, 4, 0)
        self.container.setLayout(self.baselayout)  # set main layout
        self.setCentralWidget(self.container)  # yeah do that
        self.setWindowTitle('Jeopardy!')  # window title
        self.show()  # obviously

    def closeEvent(self, event):
        if self.gamedone:
            event.accept()
            return
        msgb = QMessageBox()
        msgb.setWindowTitle('Exit')
        msgb.setText('Your progress will be saved to save.json')
        msgb.exec()
        event.accept()
        self.savegame()

    def savegame(self, export='save.json'):
        data = {'score': {}, 'clicked': self.clickedbs, 'cteam': None}
        
        for team in self.teams:
            data['score'][team.name] = team.score
        
        data['cteam'] = self.currentTeam.name
        
        f = open('save.json', 'w')
        f.write(json.dumps(data))
        f.close()

    def fq(self):
        self.fqactivated = True
        self.rb.hide();self.wb.hide()
        self.currentTeam = self.teams[0]
        self.updateTeamLabel(self.currentTeam.name)
        self.pointsbet = []
        
        for team in self.teams: # get amount of points each team is betting
            ok = False
            while not ok:
                points, ok = QInputDialog().getInt(self, 'Points', 'Points {0} is betting for the final question: '.format(team.name))
                if points > abs(team.score):
                    msgb = QMessageBox()
                    msgb.setWindowTitle('Error!')
                    msgb.setText('The team does not have that much points!')
                    msgb.exec()
                    ok = False
                if points < 0:
                    msgb = QMessageBox()
                    msgb.setWindowTitle('Error!')
                    msgb.setText('You cannot bet negative points!')
                    msgb.exec()
                    ok = False
            self.pointsbet.append(points)
            # print(points)
        
        self.fqansbtn.show()
        self.ql.setText(self.finalq[0])
        self.ql.show()
        

    def fqview(self):
        self.ql.setText(self.finalq[1])
        self.fqansbtn.hide()
        self.rb.show()
        self.wb.show()
        # TODO: disconnect button handlers and connect new ones
        self.rb.disconnect()
        self.wb.disconnect()
        self.rb.clicked.connect(self.fqr)
        self.wb.clicked.connect(self.fqw)
        # no point connecting to original bc the game ended
        
    
    def fqr(self):
        self.currentTeam.score += self.pointsbet[self.teams.index(self.currentTeam)]
        self.updateTeam()

    def fqw(self):
        self.currentTeam.score -= self.pointsbet[self.teams.index(self.currentTeam)]
        self.updateTeam()

    def buttonhandle(self):
        sender = self.sender()  # get sender (in this case always a button)
        #        print('cat', sender.cat)
        #        print('q', sender.q-1)
        sender.hide()  # hide the button so you can't click it twice
        self.currentq = (
            sender.cat,
            sender.q - 1,
        )  # set current question for self.viewanswer
        # print(self.currentq)
        question = self.questions[sender.cat][sender.q - 1]  # hope this works
        if len(question) > 50:
        	question = question[:50] + '\n' + question[51:]
        self.ql.setText(question)  # set text for the viewer
        self.ql.show()  # show it
        self.currentscore = int(sender.text())

        self.clickedbs.append(self.currentq)

        self.ansbtn.show()  # also show the view answer button

    def viewanswer(self):
        self.ql.setText(
            self.answers[self.currentq[0]][self.currentq[1]]
        )  # changes the question label to an answer label (wild i know)
        self.ansbtn.hide()
        self.rb.show()
        self.wb.show()

    def makeTeams(self):
        self.teams = []
        for team in self.teamnames:
            self.teams.append(Team(team))
        self.currentTeam = self.teams[0]
        
        if self.save_exists:
            data = json.loads(open('save.json').read())
            for team in self.teams:
                team.score = data['score'][team.name]
                if team.name == data['cteam']:
                    self.currentTeam = team

    def rightHandler(self):
        self.currentTeam.score += self.currentscore
        self.updateTeam()
        self.rb.hide()
        self.wb.hide()

    def wrongHandler(self, h=True):
        self.currentTeam.score -= self.currentscore
        self.updateTeam()
        self.wb.hide()
        self.rb.hide()

    def updateTeam(self):
        labelIndex = self.teams.index(self.currentTeam)
        label = getattr(self, 'tlabel{0}'.format(labelIndex))
        label.setText(
            self.currentTeam.name + ' - Score: ' + str(self.currentTeam.score)
        )
        if labelIndex == len(self.teams) - 1:
            self.currentTeam = self.teams[0]
        else:
            self.currentTeam = self.teams[labelIndex + 1]
        self.cTeamLabel.setText('Current team: ' + self.currentTeam.name)
        # self.rb.hide()
        # self.wb.hide()
        
        # if game ended
        if self.fqactivated and self.currentTeam == self.teams[0]:
            msgb = QMessageBox()
            msgb.setWindowTitle('Winner')
            
            # get highest team
            ht = Team('None')
            for t in self.teams:
                if t.score > ht.score:
                    ht = t
            
            msgb.setText('{0} won with {1} points!'.format(ht.name, ht.score))
            msgb.exec()
            self.gamedone = True
            os.remove('save.json')
            self.close()
    
    def updateTeamLabel(self, teamname):
        self.cTeamLabel.setText('Current team: ' + teamname)


if __name__ == '__main__':
    app = QApp([])
    m = mainWindow()
    #m.maximize_window()
    #    print(m.headings)
    #    print(m.questions)
    app.exec()
