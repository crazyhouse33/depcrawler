from depcrawler.bin.parser import args
from depcrawler.linker_map import LinkerMapDependencies
from depcrawler.dyndep import LoaderDependencies
from depcrawler.dependency import Dependency_Group

dependencies= Dependency_Group()
if args.map:
    dependencies.merge(LinkerMapDependencies(args.map))

if args.module:
    dependencies.merge= LoaderDependencies(args.module)

if args.debug:
    print(dependencies, file=sys.stderr)

print (" ".join(dependencies.get_depends()))
