#! /usr/bin/python2
"""
* jupyter2org.py - Convert Jupyter Notebooks to Org Mode

  Usage: jypyter2org.py [options] FILE.ipynb FILE.org

  Input files:
        - notebook-file -  ipynb file

  Output files:
        - Org with imbedded babel source code blocks

  Source/home:

     - https://github.com/eludom/jupyter2org

"""

"""
** Python Imports and Constants
"""

import json
from pprint import pprint
import sys
import os
from optparse import OptionParser


"""
** Helper functions
"""
def info(msg):
        if opts.verbose:
                sys.stderr.write("%s: info: %s\n" % (os.path.basename(__file__), msg))

def warn(msg):
        sys.stderr.write("%s: warn: %s\n" % (os.path.basename(__file__), msg))

def debug(msg):
        if opts.debug:
                sys.stderr.write("%s: debug: %s\n" % (os.path.basename(__file__), msg))

def error(msg):
        sys.stderr.write("%s: error: %s\n" % (os.path.basename(__file__), msg))

def die(msg):
        sys.stderr.write("%s: fatal: %s\n" % (os.path.basename(__file__), msg))
        sys.exit(1)


def md_2_org(md_text):
    """Convert select markdown text to equivilant org mode markup

    pandoc may be a more complete colution.

    Keyword arguments:
    md_text -- a blob of markdown text

    Returns:
    org mode text as a string
    """

    # convert markdown to org

    org_text = ""

    for line in md_text.split("\n"):

        # relplace markdown section headers

        replaced = len(line) - len(line.lstrip("#"))
        if (replaced > 0):
            line =  "*"*replaced + line[replaced:]

        org_text += line + "\n"

    return org_text

def process_markdown_cell(cell):
        """
*** process_markdown_cell - do something useful with jupyter markdown
        """

        print """

# begin markdown
%s
# end markdown

"""  % (md_2_org("".join(cell["source"])))

        # Currently ignoring anything but source in the markdown cell


def print_ob_ipyton_preamble():
        """
*** print_ob_ipython_preamble - spit out preamble, includes for ob ipython
        """

        print """
#+BEGIN_SRC ipython :session week3
  %matplotlib inline
  import matplotlib.pyplot as plt
  import numpy as np
#+END_SRC
"""


def process_code_cell(cell, base):
        """
*** process_markdown_cell - do something useful with jupyter markdown
        """

        print """
#+begin_src ipython :session %s
%s
#+end_src
"""  % (base, "".join(cell["source"]).encode('utf-8').strip())

        # Currently ignoring anything but source in the markdown cell
        # may want to inclclude output as #+RESULT: or #+begin_example



def jupyter_file_2_org(filename):
        """
** jupyter_file_2_org(filename) - convert jupyter json to org
        """
        debug("in jupyter_file_2_org")
        debug(filename)

        base=os.path.basename(os.path.splitext('/home/user/somefile.txt')[0])
        debug("base is" + base)

        print_ob_ipyton_preamble()

        nb_json = json.load(open(filename))

        for cell in nb_json["cells"]:
                if cell["cell_type"] == "markdown":
                        process_markdown_cell(cell)
                elif cell["cell_type"] == "code":
                        process_code_cell(cell, base)
                else:
                        warn("Unhandled cell type: %s" % (cell["cell_type"]))
                        warn("cell: /%s/" % (json.dumps(cell, indent=2)))
                        exit(1)


def parse_args(argv):
        """
** parse_args - command line parsing
        """

        parser = OptionParser(usage='%prog [options] [files]', description='''progname

Does foo...
''')
        parser.add_option('-d', '--debug', action='store_true',
                                          help='debug output')
        parser.add_option('-v', '--verbose', action='store_true',
                                          help='verbose output')

        opts, args = parser.parse_args(argv)

        # validate options

        if not len(args) > 1:
                die("Need at least one input file")

        return opts, args

"""
** main - parse options and process input files
"""
def main():
        for filename in args[1:]:
                jupyter_file_2_org(filename)

if __name__ == '__main__':
        global opts, args

        opts, args = parse_args(sys.argv)

        main()
