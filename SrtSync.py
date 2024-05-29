#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:19:48 2024

@author: cubaix
"""
import argparse
import re
from CbxAligner import CbxAligner

class SrtSync:
    def __init__(self):
        self.aligner = CbxAligner()
        
    def toXml(self,srt):
        xml = "\n"+srt+"\n"
        xml = re.sub(r'[\n\r]+','\n',xml)
        xml = re.sub(r'&','&amp;',xml)
        xml = re.sub(r'<','&lt;',xml)
        xml = re.sub(r'>','&gt;',xml)
        xml = re.sub(r'\n([0-9]+)\n([0-9]+:[0-9]+:[0-9]+[,.][0-9]+ --&gt; [0-9]+:[0-9]+:[0-9]+[,.][0-9]+)\n'
                     ,r'<time id="\1" stamp="\2"/>'
                     ,xml)
        return xml
        
    def sync(self,pathSrt,pathTxt):
        self.pathSrt = pathSrt
        self.pathTxt = pathTxt
        
        # Load files
        with open(self.pathSrt, 'r', encoding='utf-8') as f:
            self.srt = f.read()
        
        with open(self.pathTxt, 'r', encoding='utf-8') as f:
            self.txt = f.read()
        
        # Convert
        self.xml = self.toXml(self.srt)
        
        # Align
        self.synced = self.aligner.syncMarks1to2(self.xml, self.txt)
        self.synced = re.sub(r'\n*<time id="([0-9]+)" stamp="([^\"]+)"/>\n*'
                             , r'\n\n\1\n\2\n'
                             , self.synced)
        self.synced = re.sub(r'&amp;'
                             , r'&'
                             , self.synced)
        self.synced = re.sub(r'&lt;'
                             , r'<'
                             , self.synced)
        self.synced = re.sub(r'&gt;'
                             , r'>'
                             , self.synced)
        self.synced = self.synced.strip()
        print(self.synced)
        
        with open(self.pathTxt+".srt", 'w', encoding='utf-8') as f:
            f.write(self.synced)
        
    def test(self):
        self.sync("./data/KatyPerry-Firework.mp3.srt", "./data/KatyPerry-Firework.txt")


def main():
    try:
        parser = argparse.ArgumentParser(description="Synchronize SRT timestamps over an existing accurate transcription.")
        parser.add_argument('pathSrt', type=str, help="Path to the SRT file with good timestamps")
        parser.add_argument('pathTxt', type=str, help="Path to the TXT file with good text")
        parser.add_argument('lng', type=str, help="language", nargs='?')
        args = parser.parse_args()
        
        SrtSync().sync(args.pathSrt, args.pathTxt)
    except BaseException:
        print("")
    

if __name__ == "__main__":
    main()