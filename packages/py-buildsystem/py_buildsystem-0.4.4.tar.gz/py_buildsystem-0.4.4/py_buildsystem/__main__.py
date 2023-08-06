import os
import sys
import argparse

from py_buildsystem.common import logger, levels

from py_buildsystem.Project.Project import Project
from py_buildsystem.Toolchain.Toolchain import Toolchain


sys.tracebacklimit = 0


parser = argparse.ArgumentParser(prog="py_buildsystem", description='Python based build system.', allow_abbrev=True)

parser.add_argument('-pcc', '--project_compiler_config', type=str, nargs=1, required=True,
                    help='Project specific toolchain configuration file')

parser.add_argument('-pc', '--project_config', type=str, nargs=1, default=os.getcwd(), required=True,
                    help='Project configuration file')

parser.add_argument('compiler_path', metavar='compiler path', type=str, nargs='?', default='',
                    help='Path to compiler')

parser.add_argument('-v', '--verbose', action='store_true', dest="verbose",
                    help='verbose mode')

args = parser.parse_args()

if args.verbose is True:
    logger.setLevel(levels["DEBUG"])
else:
    logger.setLevel(levels["INFO"])

toolchain = Toolchain(args.project_compiler_config[0], args.compiler_path)
project = Project(args.project_config[0], toolchain)
