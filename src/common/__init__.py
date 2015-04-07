import os
import sys
import inspect

cur_path = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
sys.path.insert(1, cur_path)
print "common pkg dir name {} added to sys path".format(sys.path[cur_path])


