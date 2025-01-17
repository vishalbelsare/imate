#! /usr/bin/env python

# =======
# Imports
# =======

import os
import getopt
from os.path import join
import sys
import pickle
import numpy
from imate import traceinv
from imate import Matrix
from imate import AffineMatrixFunction                             # noqa: F401
import subprocess
import multiprocessing
import platform
import re
from datetime import datetime


# ===============
# parse arguments
# ===============

def parse_arguments(argv):
    """
    Parses the argument of the executable and obtains the filename.

    Input file is netcdf nc file or ncml file.
    """

    # -----------
    # print usage
    # -----------

    def print_usage(exec_name):
        usage_string = "Usage: " + exec_name + " <arguments>"
        options_string = """
At least, one of the following arguments are required:

    -c --cpu      Runs the benchmark on CPU. Default is not to run on cpu.
    -g --gpu      Runs the benchmark on GPU. Default is not to run in gpu.
        """

        print(usage_string)
        print(options_string)

    # -----------------

    # Initialize variables (defaults)
    arguments = {
        'use_cpu': False,
        'use_gpu': False
    }

    # Get options
    try:
        opts, args = getopt.getopt(argv[1:], "cg", ["cpu", "gpu"])
    except getopt.GetoptError:
        print_usage(argv[0])
        sys.exit(2)

    # Assign options
    for opt, arg in opts:
        if opt in ('-c', '--cpu'):
            arguments['use_cpu'] = True
        elif opt in ('-g', '--gpu'):
            arguments['use_gpu'] = True

    if len(argv) < 2:
        print_usage(argv[0])
        sys.exit()

    return arguments


# ==================
# get processor name
# ==================

def get_processor_name():
    """
    Gets the name of CPU.

    For windows operating system, this function still does not get the full
    brand name of the cpu.
    """

    if platform.system() == "Windows":
        return platform.processor()

    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.getoutput(command).strip()

    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.getoutput(command).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)[1:]

    return ""


# ============
# get gpu name
# ============

def get_gpu_name():
    """
    Gets the name of gpu device.
    """

    command = 'nvidia-smi -a | grep -i "Product Name" -m 1 | grep -o ":.*"' + \
              ' | cut -c 3-'
    return subprocess.getoutput(command).strip()


# =======================
# get num all gpu devices
# =======================

def get_num_all_gpu_devices():
    """
    Get number of all gpu devices
    """

    command = ['nvidia-smi', '--list-gpus', '|', 'wc', '-l']
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    error_code = process.poll()

    # Error code 127 means nvidia-smi is not a recognized command. Error code
    # 9 means nvidia-smi could not find any device.
    if error_code != 0:
        num_gpu = 0
    else:
        num_gpu = int(stdout)

    return num_gpu


# =========
# benchmark
# =========

def benchmark(argv):
    """
    Test for :mod:`imate.traceinv` sub-package.
    """

    # Settings
    benchmark_dir = '..'
    directory = join(benchmark_dir, 'matrices')
    # data_names = ['Queen_4147', 'G3_circuit', 'Flan_1565', 'Bump_2911',
    #              'cvxbqp1', 'StocF-1465', 'G2_circuit', 'gridgena',
    #              'parabolic_fem']
    data_names = ['nos5', 'mhd4800b', 'bodyy6', 'G2_circuit', 'parabolic_fem',
                  'StocF-1465', 'Bump_2911', 'Queen_4147']
    # data_names = ['nos7', 'nos5', 'plat362', 'bcsstk21', 'mhd4800b', 'aft01',
    #               'bodyy6', 'ted_B', 'G2_circuit', 'parabolic_fem',
    #               'StocF-1465', 'Bump_2911', 'Queen_4147']
    # data_types = ['32', '64', '128']
    data_types = ['32', '64']  # OpenBlas does not support 128-bit

    config = {
        'gram': False,
        'num_samples': 200,
        'lanczos_degree': 80,
        'lanczos_tol':  None,
        'orthogonalize': 0,
        'error_rtol': 1e-3,
        'error_atol': 0,
        'outlier_significance_level': 0.01,
        'verbose': False,
        'plot': False
    }

    devices = {
        'cpu_name': get_processor_name(),
        'gpu_name': get_gpu_name(),
        'num_all_cpu_threads': multiprocessing.cpu_count(),
        'num_all_gpu_devices': get_num_all_gpu_devices()
    }

    data_results = []
    arguments = parse_arguments(argv)

    # Loop over data filenames
    for data_name in data_names:

        data_result = {
            'data_name': data_name,
            'type_results': [],
        }

        # For each data, loop over float type, such as 32-bit, 64-bit, 128-bit
        for data_type in data_types:

            filename = data_name + '_float' + data_type + '.pickle'
            filepath = join(directory, filename)
            with open(filepath, 'rb') as h:
                M = pickle.load(h)
            print('loaded %s.' % filename)

            Mop = Matrix(M)
            # Mop = AffineMatrixFunction(M)

            type_result = {
                'data_type': data_type,
                'cpu_results': [],
                'gpu_results': []
            }

            # --------------
            # Compute on CPU
            # --------------

            if arguments['use_cpu']:

                log2_num_cpu = numpy.log2(devices['num_all_cpu_threads'])
                # if log2_num_cpu != int(log2_num_cpu):
                #     raise RuntimeWarning("Num CPUs isn't a power of two.")

                # Loop over number of cpu threads
                for i in range(1, int(log2_num_cpu)+1):
                    num_threads = int(2**i)
                    print('\tComputing on cpu with %d threads ...'
                          % num_threads)
                    trace_cpu, info_cpu = traceinv(
                            Mop,
                            method='slq',
                            min_num_samples=config['num_samples'],
                            max_num_samples=config['num_samples'],
                            lanczos_degree=config['lanczos_degree'],
                            lanczos_tol=config['lanczos_tol'],
                            orthogonalize=config['orthogonalize'],
                            error_rtol=config['error_rtol'],
                            error_atol=config['error_atol'],
                            gram=config['gram'],
                            outlier_significance_level=config[
                                'outlier_significance_level'],
                            verbose=config['verbose'],
                            plot=config['plot'],
                            gpu=False,
                            num_threads=num_threads)

                    cpu_result = {
                        'num_threads': num_threads,
                        'trace': trace_cpu,
                        'info': info_cpu
                    }
                    type_result['cpu_results'].append(cpu_result)

            # --------------
            # Compute on GPU
            # --------------

            if arguments['use_gpu']:

                # Loop over number of gpu devices
                if data_type != '128':

                    log2_num_gpu = numpy.log2(devices['num_all_gpu_devices'])
                    if log2_num_gpu != int(log2_num_gpu):
                        raise RuntimeError('Num GPUs is not a power of two.')

                    for i in range(0, int(log2_num_gpu)+1):
                        num_gpu_devices = int(2**i)
                        print('\tComputing on gpu with %d devices ...'
                              % num_gpu_devices)
                        trace_gpu, info_gpu = traceinv(
                                Mop,
                                method='slq',
                                min_num_samples=config['num_samples'],
                                max_num_samples=config['num_samples'],
                                lanczos_degree=config['lanczos_degree'],
                                lanczos_tol=config['lanczos_tol'],
                                orthogonalize=config['orthogonalize'],
                                error_rtol=config['error_rtol'],
                                error_atol=config['error_atol'],
                                gram=config['gram'],
                                outlier_significance_level=config[
                                    'outlier_significance_level'],
                                verbose=config['verbose'],
                                plot=config['plot'],
                                gpu=True,
                                num_gpu_devices=num_gpu_devices)

                        gpu_result = {
                            'num_gpu_devices': num_gpu_devices,
                            'trace': trace_gpu,
                            'info': info_gpu
                        }
                        type_result['gpu_results'].append(gpu_result)

            print('')
            data_result['type_results'].append(type_result)

        data_results.append(data_result)

    now = datetime.now()

    # Final object of all results
    benchmark_results = {
        'config': config,
        'devices': devices,
        'data_results': data_results,
        'date': now.strftime("%d/%m/%Y %H:%M:%S")
    }

    # Save to file
    pickle_dir = 'pickle_results'
    output_filename = 'benchmark_results'
    if arguments['use_cpu']:
        output_filename += '_cpu'
    if arguments['use_gpu']:
        output_filename += '_gpu'
    output_filename += '.pickle'
    output_full_filename = join(benchmark_dir, pickle_dir, output_filename)
    with open(output_full_filename, 'wb') as file:
        pickle.dump(benchmark_results, file, protocol=pickle.HIGHEST_PROTOCOL)
    print('Results saved to %s.' % output_full_filename)


# ===========
# System Main
# ===========

if __name__ == "__main__":
    sys.exit(benchmark(sys.argv))
