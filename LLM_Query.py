# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:16:36 2024

@author: cavsf
"""

from models import Character, Party, Floor, Location, Item, History, db

def LLM_query(query,current_scene):
    with open('./data/preprompt_summarized.txt','r',encoding="utf-8") as file:
        preprompt=file.read()
    prompt=preprompt
Character.query.all()

#Doesn't work without running the whole thing. Maybe rethink how DB used? rewrite?