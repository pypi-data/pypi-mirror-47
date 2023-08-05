#!/usr/bin/env python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import sys
import os


def get_parser():

    parser = argparse.ArgumentParser(description="Singularity Client",
                                formatter_class=argparse.RawTextHelpFormatter,
                                add_help=False)

    # Global Options
    parser.add_argument('--debug','-d', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet','-q', dest="quiet", 
                        help="suppress all normal output", 
                        default=False, action='store_true')

    parser.add_argument('--version', dest="version", 
                        help="show singularity and spython version", 
                        default=False, action='store_true')

    subparsers = parser.add_subparsers(help='description',
                                       title='actions',
                                       description='actions for Singularity',
                                       dest="command", metavar='general usage')

          
    # Recipes

    recipe = subparsers.add_parser("recipe",
                                   help="Recipe conversion and parsing")

    recipe.add_argument('--entrypoint', dest="entrypoint",
                         help="define custom entry point and prevent discovery", 
                         default=None, type=str)

    recipe.add_argument("files", nargs='*',
                        help="the recipe input file and [optional] output file", 
                        type=str)

    parser.add_argument("-i", "--input", type=str, 
                        default="auto", dest="input",
                        choices=["auto", "docker", "singularity"],
                        help="Is the input a Dockerfile or Singularity recipe?")

    # General Commands

    subparsers.add_parser("shell", help="Interact with singularity python")
    subparsers.add_parser("test", help='''Container testing (TBD)''')

    return parser


def set_verbosity(args):
    '''determine the message level in the environment to set based on args.
    '''
    level = "INFO"

    if args.debug is True:
        level = "DEBUG"
    elif args.quiet is True:
        level = "QUIET"

    os.environ['MESSAGELEVEL'] = level
    os.putenv('MESSAGELEVEL', level)
    os.environ['SINGULARITY_MESSAGELEVEL'] = level
    os.putenv('SINGULARITY_MESSAGELEVEL', level)
    
    # Import logger to set
    from spython.logger import bot
    bot.debug('Logging level %s' %level)
    import spython

    bot.debug("Singularity Python Version: %s" % spython.__version__)


def version():
    '''version prints the version, both for the user and help output
    '''
    import spython
    return spython.__version__
    

def main():

    parser = get_parser()

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''
        v = version()
        print("\nSingularity Python [v%s]\n" %(v))
        parser.print_help()
        sys.exit(return_code)
    
    if len(sys.argv) == 1:
        help()
    try:
        # We capture all primary arguments, and take secondary to pass on
        args, options = parser.parse_known_args()
    except:
        sys.exit(0)

    # The main function
    main = None

    # If the user wants the version
    if args.version is True:
        print(version())
        sys.exit(0)

    # if environment logging variable not set, make silent
    set_verbosity(args)

    # Does the user want help for a subcommand?
    if args.command == 'recipe': from .recipe import main 
    elif args.command == 'shell': from .shell import main 
    elif args.command == 'test': from .test import main 
    else: help()

    # Pass on to the correct parser
    if args.command is not None:
        main(args=args, options=options, parser=parser)


if __name__ == '__main__':
    main()
