from collections import defaultdict 
import os


class Symbol:
    def __init__(self, file, line, name):
        self.file=file
        self.line=line
        self.name=name

    def __str__(self):
        to_print=filter(None, [self.file, self.line,self.name])
        return ":".join(to_print)

class Dependency_O:
    """Dependencie of a .o. Set an attribute to UNKNOW if the information cant be given. Path specify a place to look from relative paths"""
    def __init__(self, lib, module, symbol_file=None, symbol_name=None, symbol_line=None, relative_path=None):
        self.lib=Dependency_O.enforce_existence(lib, relative_path) # The static lib pulled in
        self.module=Dependency_O.enforce_existence(module, relative_path) # The o file pulled in
        self.symbol= Symbol(Dependency_O.enforce_existence(symbol_file, relative_path), symbol_line, symbol_name)

    def enforce_existence(attribute, path):
        if attribute and attribute!="UNKNOWN" and not os.path.isfile(attribute):
            if path:
                attribute= os.path.join(path,attribute)
                if os.path.isfile(attribute):
                    return attribute
            raise FileNotFoundError(attribute+" Could not be found. This dependencie can not exist")
        return attribute

    def get_minimal_file(self):
        if self.module and self.module != "UNKNOWN":
            return self.module
        elif self.lib and self.lib!= "UNKNOWN":
            return self.lib
        else:
            raise ValueError("The file dependencie of "+str(self)+ "is not set")





class Dependency_Group:
    """Structure to organize and print file dependencies"""
    def __init__(self):
        self.deps= defaultdict(list)

    def add_depend(self, dep):
        self.deps[dep.get_minimal_file()].append(dep)

    def get_depends(self):
        """Return the minimal set of ofile dependencies"""
        return list(self.deps.keys())

    def __str__(self):
        ext_mod=[]
        for module, dep_list in self.deps.items():
            dep= dep_list[0]
            in_mod=["-> {} ({}):".format(dep.module, dep.lib)]
            in_mod.extend([str(dep.symbol) for dep in dep_list])
            ext_mod.append("\n\t".join(in_mod))
        return "\n".join(ext_mod)

    def merge(self, other):
        for ofile, deps in other.deps.items():
            for dep in deps:
                self.add_depend(dep)




