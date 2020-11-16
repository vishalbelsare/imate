# =======
# Imports
# =======

import os
import matplotlib
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes,InsetPosition,mark_inset
import matplotlib.ticker
from matplotlib.ticker import ScalarFormatter,NullFormatter,FormatStrFormatter
import matplotlib.pyplot as plt
from distutils.spawn import find_executable

# Remove plt.tight_layput() warning
import logging
logging.captureWarnings(True)
import warnings
warnings.filterwarnings(action='ignore',module='matplotlib',category=UserWarning,message=('This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.'))

# ==================
# Load Plot Settings
# ==================

def LoadPlotSettings():
    """
    General settings for the plot.
    """

    # Color palette
    import seaborn as sns
    # sns.set()

    # Axes font size
    sns.set(font_scale=1.2)

    # LaTeX
    if find_executable('latex'):
        try:
            # plt.rc('text',usetex=True)
            matplotlib.rcParams['text.usetex'] = True
            matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
            matplotlib.font_manager._rebuild()
        except:
            pass

    # Style sheet
    sns.set_style("white")
    sns.set_style("ticks")

    # Font (Note: this should be AFTER the plt.style.use)
    plt.rc('font',family='serif')
    plt.rcParams['svg.fonttype'] = 'none'  # text in svg file will be text not path.

    #from cycler import cycler
    #matplotlib.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

# =========
# Save Plot
# =========

def SavePlot(plt,Filename):
    """
    """

    # Get the root directory of the package (parent directory of this script)
    FileDirectory = os.path.dirname(os.path.realpath(__file__))
    ParentDirectory = os.path.dirname(FileDirectory)
    SecondParentDirectory = os.path.dirname(ParentDirectory)

    # Try to save in the docs/images dirctory. Check if exists and writable
    SaveDir = os.path.join(SecondParentDirectory,'docs','images')
    if (not os.path.isdir(SaveDir)) or (not os.access(SaveDir,os.W_OK)):

        # Write in the current working directory
        SaveDir = os.getcwd()

    # Save plot in both svg and pdf format
    Filename_PDF = Filename + '.pdf'
    Filename_SVG = Filename + '.svg'
    if os.access(SaveDir,os.W_OK):
        SaveFullname_SVG = os.path.join(SaveDir,Filename_SVG)
        SaveFullname_PDF = os.path.join(SaveDir,Filename_PDF)
        plt.savefig(SaveFullname_SVG,transparent=True,bbox_inches='tight')
        plt.savefig(SaveFullname_PDF,transparent=True,bbox_inches='tight')
        print('')
        print('Plot saved to "%s".'%(SaveFullname_SVG))
        print('Plot saved to "%s".'%(SaveFullname_PDF))
    else:
        print('Cannot save plot to %s. Directory is not writable.'%SaveDir)