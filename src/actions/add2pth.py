#!/usr/bin/python
#################################################

# Adds current Directory to Site packages and looks for relevant .pth files
# Description:
# ------------------------------------------------------------------
# 1. Get current file path.
# 2. Get the Directory path current file is in.
# 3. Add this Directory to sys paths.
# Original Author: Akul S - akurnya@gmail.com
#################################################

import os
import inspect
import site

site.addsitedir(os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe())))))
