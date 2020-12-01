#! /usr/bin/env python

# =======
# Imports
# =======

import os
from os import path
import sys
import numpy
import scipy
from scipy import sparse
from TraceInv import GenerateMatrix
from TraceInv import InterpolateTraceOfInverse

# For plotting, we disable interactive display
os.environ['DISPLAY'] = ':0.0'

# =================
# Remove Saved Plot
# =================

def RemoveSavedPlot():
    """
    When the option ``Plot=True`` is used in :mod:`TraceInv.GenerateMatrix`, a file named
    ``CorrelationMatrix.svg`` is saved in the current directory. Call this function
    to delete this file.
    """

    SaveDir = os.getcwd()
    Filename_SVG = 'InterpolationResults' + '.svg'
    SaveFullname_SVG = os.path.join(SaveDir,Filename_SVG)

    if os.path.exists(SaveFullname_SVG):
        try:
            os.remove(SaveFullname_SVG)
        except:
            pass

    print('File %s is deleted.'%SaveFullname_SVG)

# =================================
# Test Interpolate Trace Of Inverse
# =================================

def test_InterpolateTraceOfInverse():
    """
    Test for :mod:`TraceInv.InterpolateTraceOfInverse` sub-package.
    """

    # Compute trace of inverse of K using dense matrix
    print('Using dense matrix')
    A = GenerateMatrix(NumPoints=20,UseSparse=False)
    B = GenerateMatrix(NumPoints=20,UseSparse=False,DecorrelationScale=0.05)

    Verbose = True
    InterpolantPoints = [1e-4,1e-3,1e-2,1e-1,1,1e+1]
    InquiryPoint = 0.4
    ComputeOptions={'ComputeMethod':'cholesky','UseInverseMatrix':True}

    # Compute exact trace without interpolation
    TI00 = InterpolateTraceOfInverse(A,B=B,InterpolationMethod='EXT',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace00 = TI00.Interpolate(InquiryPoint)
    Error00 = 0

    # Eigenvalues Method
    TI01 = InterpolateTraceOfInverse(A,B=B,InterpolationMethod='EIG',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace01 = TI01.Interpolate(InquiryPoint)
    Error01 = 100.0 * numpy.abs(Trace01 - Trace00) / Trace00

    # Monomial Basis Functions
    TI02 = InterpolateTraceOfInverse(A,B=B,InterpolationMethod='MBF',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace02 = TI02.Interpolate(InquiryPoint)
    Error02 = 100.0 * numpy.abs(Trace02 - Trace00) / Trace00

    # Root Monomial Basis Functions, basis type: NonOrthogonal
    TI03 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RMBF',BasisFunctionsType='NonOrthogonal',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace03 = TI03.Interpolate(InquiryPoint)
    Error03 = 100.0 * numpy.abs(Trace03 - Trace00) / Trace00

    # Root Monomial Basis Functions, basis type: Orthogonal
    TI04 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RMBF',BasisFunctionsType='Orthogonal',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace04 = TI04.Interpolate(InquiryPoint)
    Error04 = 100.0 * numpy.abs(Trace04 - Trace00) / Trace00

    # Root Monomial Basis Functions, basis type: Orthogonal2
    TI05 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RMBF',BasisFunctionsType='Orthogonal2',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace05 = TI05.Interpolate(InquiryPoint)
    Error05 = 100.0 * numpy.abs(Trace05 - Trace00) / Trace00

    # Radial Basis Functions, FunctionType 1
    TI06 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RBF',FunctionType=1,ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace06 = TI06.Interpolate(InquiryPoint)
    Error06 = 100.0 * numpy.abs(Trace06 - Trace00) / Trace00

    # Radial Basis Functions, FunctionType 2
    TI07 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RBF',FunctionType=2,ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace07 = TI07.Interpolate(InquiryPoint)
    Error07 = 100.0 * numpy.abs(Trace07 - Trace00) / Trace00

    # Radial Basis Functions, FunctionType 3
    TI08 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RBF',FunctionType=3,ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace08 = TI08.Interpolate(InquiryPoint)
    Error08 = 100.0 * numpy.abs(Trace08 - Trace00) / Trace00

    # Rational Polynomial with two interpolating points
    InterpolantPoints = [1e-1,1e+1]
    TI09 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RPF',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace09 = TI09.Interpolate(InquiryPoint)
    Error09 = 100.0 * numpy.abs(Trace09 - Trace00) / Trace00

    # Rational Polynomial with four interpolating points
    InterpolantPoints = [1e-2,1e-1,1,1e+1]
    TI10 = InterpolateTraceOfInverse(A,B=B,InterpolantPoints=InterpolantPoints,InterpolationMethod='RPF',ComputeOptions=ComputeOptions,Verbose=Verbose)
    Trace10 = TI10.Interpolate(InquiryPoint)
    Error10 = 100.0 * numpy.abs(Trace10 - Trace00) / Trace00

    print("")
    print("---------------------------------------")
    print("Method  Options         TraceInv  Error")
    print("------  -------------   --------  -----")
    print("EXT     N/A             %0.4f  %0.2f%%"%(Trace00,Error00))
    print("EIG     N/A             %0.4f  %0.2f%%"%(Trace01,Error01))
    print("MBF     N/A             %0.4f  %0.2f%%"%(Trace02,Error02))
    print("RMBF    NonOrthogonal   %0.4f  %0.2f%%"%(Trace03,Error03))
    print("RMBF    Orthogonal      %0.4f  %0.2f%%"%(Trace04,Error04))
    print("RMBF    Orthogonal2     %0.4f  %0.2f%%"%(Trace05,Error05))
    print("RBF     Type 1          %0.4f  %0.2f%%"%(Trace06,Error06))
    print("RBF     Type 2          %0.4f  %0.2f%%"%(Trace07,Error07))
    print("RBF     Type 3          %0.4f  %0.2f%%"%(Trace08,Error08))
    print("RPF     2-Points        %0.4f  %0.2f%%"%(Trace09,Error09))
    print("RPF     4-Points        %0.4f  %0.2f%%"%(Trace10,Error10))
    print("---------------------------------------")
    print("")

    # Compare with exact soluton and plot results
    InquiryPoints = numpy.logspace(numpy.log10(InterpolantPoints[0]),numpy.log10(InterpolantPoints[-1]),5)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI00.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI01.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI02.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI05.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI08.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)
    Trace_Interpolated,Trace_Exact,Trace_RelativeError = TI09.Interpolate(InquiryPoints,CompareWithExact=True,Plot=True)

    # Remove saved plot
    RemoveSavedPlot()

# ===========
# System Main
# ===========

if __name__ == "__main__":
    sys.exit(test_InterpolateTraceOfInverse())
