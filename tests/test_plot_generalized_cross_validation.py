#! /usr/bin/env python

# SPDX-FileCopyrightText: Copyright 2021, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the license found in the LICENSE.txt file in the root
# directory of this source tree.


# =======
# imports
# =======

import os
import sys

import warnings
warnings.resetwarnings()
warnings.filterwarnings("error")


# =================
# remove saved plot
# =================

def remove_saved_plot(filename):
    """
    When the option ``plot=True`` is used in :mod:`imate.correlationmatrix`, a
    file named ``CorrelationMatrix.svg`` is saved in the current directory.
    Call this function to delete this file.
    """

    save_dir = os.getcwd()
    fullname = os.path.join(save_dir, filename)

    if os.path.exists(fullname):
        try:
            os.remove(fullname)
            print('File %s is deleted.' % fullname)
        except OSError:
            pass

    else:
        print('File %s does not exists.' % fullname)


# ======================================
# test plot generalized cross validation
# ======================================

def test_plot_generalized_cross_validation():
    """
    Test for the module :mod:`examples.Plot_GeneralizedCrossValidation`.

    The function :func:`examples.Plot_GeneralizedCrossvalidation.main` is
    called with ``test=True`` argument, which evokes computation on smaller
    matrix size. The produced figures are saved with ``test_`` prefix.
    """

    # Get the root directory of the package (parent directory of this script)
    file_directory = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(file_directory)
    examples_directory = os.path.join(parent_directory, 'examples')

    # Put the examples directory on the path
    sys.path.append(parent_directory)
    sys.path.append(examples_directory)

    # Run example
    from examples import plot_generalized_cross_validation
    plot_generalized_cross_validation.main(test=True)

    # Remove saved plot
    filename = 'test_generalized_cross_validation'
    filename_svg = filename + '.svg'
    filename_pdf = filename + '.pdf'
    remove_saved_plot(filename_svg)
    remove_saved_plot(filename_pdf)


# ===========
# script main
# ===========

if __name__ == "__main__":
    sys.exit(test_plot_generalized_cross_validation())
