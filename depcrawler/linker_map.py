import sys
import os
import re
from depcrawler.dependency import Dependency_Group, Dependency_O

# All the sub parsers are in the same file to avoid circular dependencies
class UnsupportedError(Exception):
    pass
  
class LinkerMapParser:
    """Factory for linker map specific code. Parsers are first called to quickely check if they think they handle properly. Then during process they can switch to another one if something is wrong"""

    def __init__(self, file):
        if isinstance( file, str):
            self.file=open(file)
        self.current=0
        self.parsers=sorted(LinkerMapParser.__subclasses__(), key= lambda x: x.recognize())



    # TODO separate this in another real factory class out of base class
    def get_depends(self):
        res=[]
        while True:
            try:
                parser=self.get_next_parser()(self.file)
                parser.skip_the_useless_part()
                entry=parser.next_entry()
                while entry:
                    res.append(entry)
                    entry=parser.next_entry()
                break
            except UnsupportedError:
                pass
        return res

    def get_next_parser(self):
        """Get next parser"""
        try:
            return self.parsers.pop()
        except IndexError:
            sys.exit("The linker map is not supported by any implemented format")

    #Overide
    def skip_the_useless_part(self):
        pass


    #Overide
    def next_entry(self):
        return None


    #Overide
    def recognize():
        """Return int representing how certain the parser is to be in front of a file he recognize. 
        0 is not. 
        1 may be. 
        2 cant be something else"""
        return 0

            

    def unsuported_format(self, msg):
        """Call from subclass to signal this file is in fact not supported"""
        raise UnsupportedError(self.file.name+" linker map format not supported by parser:\n "+ msg)


# GNU
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
        





class LinkerMapDependencies(Dependency_Group):

    def __init__(self, path):
        Dependency_Group.__init__(self)
        self.path=path
        self._compute_dependencies()

    def _compute_dependencies(self):
        parser= LinkerMapParser(self.path)
        for dep in parser.get_depends():
            self.deps.add_depend(dep)








