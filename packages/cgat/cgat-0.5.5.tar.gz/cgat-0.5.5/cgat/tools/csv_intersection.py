'''
csv_intersection.py - intersect two tables
======================================================

:Tags: Python

Purpose
-------

.. todo::
   
   describe purpose of the script.

Usage
-----

Example::

   python csv_intersection.py --help

Type::

   python csv_intersection.py --help

for command line help.

Command line options
--------------------

'''
import sys
import cgatcore.experiment as E
import cgatcore.iotools as iotools
from cgatcore.csvutils import readTable
import csv
import hashlib


class UniqueBuffer:
    mKeys = {}

    def __init__(self, outfile):
        self.mOutfile = outfile

    def write(self, out):
        key = hashlib.md5(out).digest()
        if key not in self.mKeys:
            self.mKeys[key] = True
            self.mOutfile.write(out)


def main(argv=None):
    """script main.

    parses command line options in sys.argv, unless *argv* is given.
    """

    if argv is None:
        argv = sys.argv

    parser = E.OptionParser(
        version="%prog version: $Id: csv_intersection.py 2782 2009-09-10 11:40:29Z andreas $")

    parser.add_option("-u", "--unique", dest="unique", action="store_true",
                      help="output rows are uniq.")

    parser.set_defaults(
        remove=False,
        unique=False,
    )

    (options, args) = E.start(parser, add_csv_options=True)

    if len(args) != 2:
        raise ValueError("please specify two files to join")

    options.filename1, options.filename2 = args

    table1 = readTable(iotools.open_file(options.filename1, "r"))
    table2 = readTable(iotools.open_file(options.filename2, "r"))

    if options.unique:
        outfile = UniqueBuffer(sys.stdout)
    else:
        outfile = options.stdout

    # build new field list
    new_fields = []

    for x in options.join_fields1:
        new_fields.append(x)

    for x in fields1:
        if x not in options.join_fields1:
            new_fields.append(x)
        if x not in options.join_fields2:
            new_fields.append(x)

        writer = csv.DictWriter(outfile,
                                fields,
                                dialect=options.csv_dialect,
                                lineterminator=options.csv_lineterminator,
                                extrasaction='ignore')

    if len(lines) > 0:

        old_fields = lines[0][:-1].split("\t")

        if options.remove:
            fields = []
            for x in old_fields:
                if x not in input_fields:
                    fields.append(x)
        else:
            fields = input_fields

        reader = csv.DictReader(lines,
                                dialect=options.csv_dialect)

        print("\t".join(fields))

        first_row = True
        for row in reader:
            row = iotools.convertDictionary(row)
            writer.writerow(row)

    E.stop()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
