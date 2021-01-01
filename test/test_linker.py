import pytest
from depcrawler.linker_map import  LinkerMapParser
from depcrawler.dependency import  Dependency_O, Symbol
import os

def __equal__(self,other):
        return self.__dict__==other.__dict__

def __hash__(self):     
    return hash(tuple(sorted(self.__dict__.items())))




def test_linker(monkeypatch):

    
    parser = LinkerMapParser("code/exec2.map")
    a=parser.get_depends()
    abspath_to_o_file=os.path.abspath("code/extern/lib/an_extern_lib/CMakeFiles/ext_lib_normal.dir/ext_lib.c.o")

    expected1= Dependency_O("UNKNOWN",abspath_to_o_file,  symbol_file=os.path.abspath("code/CMakeFiles/exec2.dir/entry/exec2.c.o"), symbol_name="ext_lib")

    expected2= Dependency_O("/usr/lib/x86_64-linux-gnu/libc_nonshared.a","UNKNOWN", symbol_file="/usr/lib/gcc/x86_64-linux-gnu/6/../../../x86_64-linux-gnu/Scrt1.o", symbol_name="__libc_csu_init")

    
    monkeypatch.setattr(Dependency_O, "__eq__", __equal__)
    monkeypatch.setattr(Dependency_O, "__hash__", __hash__)
    monkeypatch.setattr(Symbol, "__eq__", __equal__ )
    monkeypatch.setattr(Symbol, "__hash__", __hash__ )
    
    assert set(a)==set([expected1, expected2])


    
