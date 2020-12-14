#! /usr/bin/env python

# =======
# Imports
# =======

import os
import sys

# ==================================
# Test Plot TraceInv Ill Conditioned
# ==================================

def test_Plot_TraceInv_IllConditioned():
    """
    Test for the module :mod:`examples.Plot_TraceInv_IllConditioned`.

    The function :func:`examples.Plot_TraceInv_IllConditioned.main` is called
    with ``test=True`` argument, which evokes computation on smaller matrix
    size. The produced figures are saved with ``test_`` prefix.
    """
 
    # Get the root directory of the package (parent directory of this script)
    FileDirectory = os.path.dirname(os.path.realpath(__file__))
    ParentDirectory = os.path.dirname(FileDirectory)  
    ExamplesDirectory = os.path.join(ParentDirectory,'examples')

    # Put the examples directory on the path
    sys.path.append(ExamplesDirectory) 

    # Run example
    from examples import Plot_TraceInv_IllConditioned
    Plot_TraceInv_IllConditioned.main(test=True)

# ===========
# System Main
# ===========

if __name__ == "__main__":
    sys.exit(test_Plot_TraceInv_IllConditioned())