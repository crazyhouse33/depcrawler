
# Goal 
The goal of this project is to get the minimum object dependencie of an object from the linker pov in a crossplatform way, thus being able to link to a gigantic library but still conserving a good incremental build. In a Candid world, linkers would have an option to easely output this information at symbol resolution time. In real world, it seems that nobody ever wanted to have a linker with decent logging. 

# How it work
The tool parse the linker map to extract information on the STATIC linking. There is no specification on linker maps output. Gcc for exemple even translate the information in your current language (thus complexifying the parsing). This step work by trying all format implemented (for now only gcc one, should work in any language) until it understand something. Needless to say, some hacks must be done to find the real path of the file pointed in linker maps. 

It then parses the executable format, listing needed libraries and dynamic symbols. Then each symbol is explored (We redo the job done by the linker) to find the shared library defining the symbol. Finally, we extract the dwarf information to localize the source file defining the symbol. This is done with lief and thus support https://github.com/lief-project/LIEF.

# Philospohy
This tool try to break dependencies until reaching file level. If it cant at any point (no thin archive, no dwarf, linkermap not understood), it try to reports something safe that is sure to not forget a dependencie

# What is needed
Your build system need to produce a linker map. On some platforms it also need to not move it apparently (https://stackoverflow.com/questions/65514075/force-absolute-path-in-linker-maps) and create thin archives for static libraries. 
