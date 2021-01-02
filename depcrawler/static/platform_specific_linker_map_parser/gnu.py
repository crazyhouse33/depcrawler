import sys
import os
import re
from depcrawler.static.linker_map import LinkerMapParser
from depcrawler.dependency import Dependency_O


class LinkerMapGNUParser(LinkerMapParser):
    """Target GCC tool chain linker map"""
    start_pattern = re.compile(r"^.*\(.*\)\s*$")

    def __init__(self, file):
        LinkerMapParser.__init__(self,file)

        self.linker_dir = os.path.dirname(os.path.abspath(file.name))
        self.lines=file.readlines() # We dont care about lazy parsing for simplicity and just load the whole file
        self.cur=0
    
    def skip_the_useless_part(self):
        line=None
        while not line:
            line=LinkerMapGNUParser._start_motif(self.lines[self.cur])
            self.cur+=1
        while not self.lines[self.cur].strip():# skipping empty lines
            self.cur+=1

    def next_entry(self):
        lib, ofile=self._parse_first(self.lines[self.cur])
        symbol_file, symbol_name =self._parse_second(self.lines[self.cur+1])
        self.cur+=2
        try:
            return Dependency_O(lib, ofile, symbol_file=symbol_file, symbol_name=symbol_name, relative_path= self.linker_dir) 
        except FileNotFoundError:
            return None


    def _parse_first(self,line):
        ofile,sep,sym=self.lines[self.cur].partition('(')
        ofile=ofile.strip()
        if sep:# This is a normal format. I cant get path to ofile
            lib= ofile
            ofile="UNKNOWN"
        else:
            lib="UNKNOWN"# This is a thin format. Cant get the lib
        return lib, ofile

    def _parse_second(self,line):
        trigger, sep,symbol= self.lines[self.cur+1].partition(" (")
        symbol_file=trigger.strip()
        symbol_name= symbol[:-2]
        return symbol_file, symbol_name
        


    def _start_motif(line):
        """Return true if a line could be the start signal"""
        return LinkerMapGNUParser.start_pattern.search(line)


    def recognize():
        return 1 # You never know with this format
