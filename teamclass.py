#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 08:00:04 2021

@author: alexey
Teamclass.py - provides team support for jeopardy.py
"""


class Team():
    score = 0

    def __init__(self, name):
        self.name = name
