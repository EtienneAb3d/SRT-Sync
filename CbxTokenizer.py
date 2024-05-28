#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 10:43:12 2024

@author: cubAIx
"""

import re

class CbxToken:
    UNK = 0
    WORD = 1
    PUNCT = 2
    TAG = 3
    def __init__(self,token,index):
        self.kind = self.TAG if re.match(r'^<[^<>]*>$', token) else self.WORD if re.match(r'^\w+$', token) else self.PUNCT if re.match(r'^[^\w]$', token) else self.UNK
        self.token = token
        self.index = index
        
    def __repr__(self):
        return f"CbxToken(token={self.token})kind={self.kind}"
    
    def __str__(self):
        return repr(self)

class CbxTokenizer:
    def tokenize_xml(self,text):
        # Temporary quick & durty: use a simple regex
        tokens = re.findall(r'<[^<>]*>|\w+|&[a-zA-Z]+;|&#[0-9]+;|[^\w]', text)
        # Empty tokens filtration
        tokens = [CbxToken(token,t) for t,token in enumerate(tokens) if token]
        return tokens
    
    def test(self):
        # Example
        text = "<a href='index.html'>Bonjour!</a> 😁 &amp; Comment ça va C&amp;A ? J'espère que <b>tout</b> va bien."
        tokens = self.tokenize_xml(text)
        print(tokens)
        print("-----")
        for t in tokens:
            print(f"[{t.kind}][{t.token}]")
        print("-----")

# CbxTokenizer().test();