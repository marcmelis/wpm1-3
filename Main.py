from __future__ import print_function
from Formula import Formula
from Clause import Clause
import sys

if __name__ == '__main__':
    f = Formula()
    f.read_file('dimacs.txt')
    print (str(f.to_1_3()), file=open("out.txt", "w"))
