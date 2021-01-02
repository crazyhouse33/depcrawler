
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
            except IndexError as e:
                raise IndexError("The linker map is not supported by any implemented format") from e
        return res

    def get_next_parser(self):
        """Get next parser"""
        return self.parsers.pop()

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


        

class LinkerMapDependencies(Dependency_Group):

    def __init__(self, path):
        Dependency_Group.__init__(self)
        self.path=path
        self._compute_dependencies()

    def _compute_dependencies(self):
        parser= LinkerMapParser(self.path)
        for dep in parser.get_depends():
            self.deps.add_depend(dep)

# Loading all different parsers
from depcrawler.static.platform_specific_linker_map_parser import *








