import lief
from collections import OrderedDict
from depcrawler.dependency import Dependency_Group


"""This should be lief job"""
class My_bin(lief.Binary):
    def libraries_deps():
        """ Return a list of direct and indirect dependencies libs. This should be in the same order as loader"""

    def libraries_path():
        """Return list of direct shared libs deps but in form of an absolute ppath. SHould be in same order than the loader """


class Shared_lib_group:
    """Help saving the load order to map symbols against the good libs"""
    def __init__(self, group):
        self.dico={}
        for lib in group:
            lib_symbols=lief.parse(lib).exported_symbols
            for symbol in lib_symbols:
                if not symbol in self.dico:
                    self.dico[symbol] = lib 

    def symbol_to_dep(self, symbol):
        """Take symbol and get the resulting dependencies"""
        return  Dependency_O(self.dico[symbol], "unknown", symbol)


class LoaderDependencies(Dependency_Group):
    def __init__(self, path):
        Dependency_Group.__init__(self)
        self.path=path
        self._compute_dependencies()

    def _compute_dependencies(self):
        binary= My_bin(lief.parse(self.path))
        loader= Shared_lib_group( binary.libraries_path())
        for symbol in binary.imported_symbols:
            self.deps.add_depend( loader.symbol_to_dep( symbol))


