import lief
import argparse

parser = argparse.ArgumentParser(description='Compute when possible minimal MODULE dependencie of a module from the given object file and corresponding linker map.' )
parser.add_argument('--module', help="A module to parse dynamic dependencies")
parser.add_argument('--map',help="The module's linker map to parse static dependencies")
parser.add_argument('-d',"--debug",help="Report every recolted information on stderr. Format is : -> Path to ofile being depended on (path to the lib containing it):\n\tsymbols", action="store_true")
args = parser.parse_args()
if args.module==None and args.map==None:
    parser.exit(status=1, message="--module or --map is required\n")

