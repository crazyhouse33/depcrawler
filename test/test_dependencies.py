import pytest
from depcrawler.linker_map import  LinkerMapParser
from depcrawler.dependency import  Dependency_Group, Dependency_O
import os

def __equal__(self,other):
        return self.__dict__==other.__dict__



def test_depend_group():

    
    abspath_to_o_file=os.path.abspath("code/extern/lib/an_extern_lib/CMakeFiles/ext_lib_normal.dir/ext_lib.c.o")
    abspath_to_o_file2=os.path.abspath("../test_linker.py")
    dep1 = Dependency_O("UNKNOWN",abspath_to_o_file,  symbol_file=os.path.abspath("code/CMakeFiles/exec2.dir/entry/exec2.c.o"), symbol_name="ext_lib")
    dep3 = Dependency_O("UNKNOWN",abspath_to_o_file,  symbol_file=os.path.abspath("code/CMakeFiles/exec2.dir/entry/exec2.c.o"), symbol_name="ext_lib_bis")

    dep2= Dependency_O(abspath_to_o_file2,"UNKNOWN", symbol_name="__libc_csu_init")

    deps= Dependency_Group()
    deps.add_depend(dep1)
    deps.add_depend(dep2)
    deps.add_depend(dep3)
    assert sorted(deps.get_depends())  == sorted ([abspath_to_o_file, abspath_to_o_file2])

    a= str(deps) # Calling it just to check it does not crash

def test_merge(monkeypatch):

    abspath_to_o_file=os.path.abspath("code/extern/lib/an_extern_lib/CMakeFiles/ext_lib_normal.dir/ext_lib.c.o")
    
    abspath_to_o_file2=os.path.abspath("../test_linker.py")
    
    dep1 = Dependency_O("UNKNOWN",abspath_to_o_file,  symbol_file=os.path.abspath("code/CMakeFiles/exec2.dir/entry/exec2.c.o"), symbol_name="ext_lib")

    dep2= Dependency_O(abspath_to_o_file2,"UNKNOWN", symbol_name="__libc_csu_init")
    deps= Dependency_Group()
    deps.add_depend(dep1)
    deps.add_depend(dep2)

    deps2=Dependency_Group()
    deps2.add_depend(dep1)
    
    deps3= Dependency_Group()
    deps3.add_depend(dep2)

    deps2.merge(deps3)

     
    monkeypatch.setattr(Dependency_O, "__eq__", __equal__)

    assert deps2.deps == deps.deps
    

    

    


    
