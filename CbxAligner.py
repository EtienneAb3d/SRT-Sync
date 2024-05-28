#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:23:19 2024

@author: cubAIx
"""

from CbxTokenizer import CbxTokenizer
from CbxTokenizer import CbxToken

class CbxAligner:
    _COST_INCREDIBLE = 1000000
    compressPosFactor = 1.0/100000.0
    
    def __init__(self):
        self.tokenizer = CbxTokenizer()
    
    def syncMarks1to2(self,xml1,xml2):
        pairs = self.alignXml(xml1,xml2)
        fused = []
        for p in pairs:
            t1 = "---"
            if p[0] is not None:
                t1 = "["+str(p[0].index)+"|"+p[0].token+"]"
                if p[0].kind == CbxToken.TAG:
                    fused.append(p[0])
            t2 = "---"
            if p[1] is not None:
                t2 = "["+str(p[1].index)+"|"+p[1].token+"]"
                fused.append(p[1])
            print(f"{t1}\t{t2}")
        return "".join([t.token for t in fused])

    
    def alignXml(self,xml1,xml2):
        toks1 = self.tokenizer.tokenize_xml(xml1)
        toks2 = self.tokenizer.tokenize_xml(xml2)
        return self.alignToks(toks1,toks2)
        
    def alignToks(self,toks1,toks2):
        # Init
        choices = [[0 for y in range(0,len(toks2)+1)] for x in range(0,len(toks1)+1)]
        costs = [[0 for y in range(0,len(toks2)+1)] for x in range(0,len(toks1)+1)]
        for x in range(1,len(toks1)+1):
            choices[x][0] = 1 # Left
            costs[x][0] = x
        for y in range(1,len(toks2)+1):
            choices[0][y] = 2 # Up
            costs[0][y] = y
        # Eval costs
        for x in range(1,len(toks1)+1):
            for y in range(1,len(toks2)+1):
                cost = self.cost(toks1[x-1],toks2[y-1])
                # For equivalent matches, prefer the earlier
                cost += (toks1[x-1].index + toks2[y-1].index)*self.compressPosFactor
                cost0 = costs[x-1][y-1] + 0.99 * cost
                cost1 = costs[x-1][y] + 1
                cost2 = costs[x][y-1] + 1
                if cost0 <= cost1 and cost0 <= cost2:
                    choices[x][y] = 0 # Match
                    costs[x][y] = cost0
                elif cost1 < cost2:
                    choices[x][y] = 1 # Left
                    costs[x][y] = cost1
                else:
                    choices[x][y] = 2 # Up
                    costs[x][y] = cost2
        
        # BackProp
        x = len(toks1)
        y = len(toks2)
        pairs = []
        while x > 0 or y > 0:
            if choices[x][y] == 0:
                x -= 1
                y -= 1
                pairs.append([toks1[x],toks2[y]])
            elif choices[x][y] == 1:
                x -= 1
                pairs.append([toks1[x],None])
            else:
                y -= 1
                pairs.append([None,toks2[y]])
        # Revert
        pairs = [pairs[p] for p in range(len(pairs)-1,-1,-1)]
        return pairs
                  
    def cost(self,tok1,tok2):
        if tok1.kind != tok2.kind:
            return self._COST_INCREDIBLE
        if tok1.token == tok2.token:
            return 0
        lc1 = tok1.token.lower()
        lc2 = tok2.token.lower()
        if lc1 == lc2:
            return 0.01
        if lc1.startswith(lc2) or lc1.endswith(lc2) or lc2.startswith(lc1) or lc2.endswith(lc1):
            return 1.0
        if len(lc1) > 2 and len(lc2) > 2 and (lc1.find(lc2) >= 0 or lc2.find(lc1) >= 0):
            return 1.0
        return 2.0 - 2.0*(min(len(lc1),len(lc2))/(len(lc1)+len(lc2)))
    
    def tracePairs(self,pairs):
        for p in pairs:
            t1 = "---"
            if p[0] is not None:
                t1 = "["+str(p[0].index)+"|"+p[0].token+"]"
            t2 = "---"
            if p[1] is not None:
                t2 = "["+str(p[1].index)+"|"+p[1].token+"]"
            print(f"{t1}\t{t2}")    
    
    def test(self):
        self.tracePairs(
            self.alignXml("- <a>Bonjour</a> ! Comment ça va, <i>aujourd'hui</i> ?"
                          ,"<a>Salut</a> ! Comment ça va super bien <i>aujourd'hui</i> ?.."))

# CbxAligner().test()
