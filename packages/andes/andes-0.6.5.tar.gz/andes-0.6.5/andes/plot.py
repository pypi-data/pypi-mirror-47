#!/usr/bin/env python3

# ANDES, a power system simulation tool for research.
#
# Copyright 2015-2018 Hantao Cui
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Andes plotting tool
"""

import os
import re
import sys
import numpy as np

import logging
from argparse import ArgumentParser
from distutils.spawn import find_executable

logger = logging.getLogger(__name__)

try:
    from matplotlib import rc
    from matplotlib import pyplot as plt
except ImportError:
    logger.critical('Package <matplotlib> not found')
    sys.exit(1)

lfile = []
dfile = []


class TDSData(object):
    """
    A time-domain simulation data container for loading, extracing and
    plotting data
    """

    def __init__(self, file_name_full, path=None):
        # paths and file names
        self._path = path if path else os.getcwd()

        file_name, _ = os.path.splitext(file_name_full)

        self._dat_file = os.path.join(self._path, file_name + '.dat')
        self._lst_file = os.path.join(self._path, file_name + '.lst')

        # data members for raw data
        self._idx = []  # indices of variables
        self._uname = []  # unformatted variable names
        self._fname = []  # formatted variable names
        self._data = []  # data loaded from dat file

        # auxillary data members for fast query
        self.t = []
        self.nvars = 0  # total number of variables including `t`

        # TODO: consider moving the loading calls outside __init__
        self.load_lst()
        self.load_dat()

    def load_lst(self):
        """
        Load the lst file into internal data structures

        """
        with open(self._lst_file, 'r') as fd:
            lines = fd.readlines()

        idx, uname, fname = list(), list(), list()

        for line in lines:
            values = line.split(',')
            values = [x.strip() for x in values]

            # preserve the idx ordering here in case variables are not
            # ordered by idx
            idx.append(int(values[0]))  # convert to integer
            uname.append(values[1])
            fname.append(values[2])

        self._idx = idx
        self._fname = fname
        self._uname = uname
        self.nvars = len(uname)

    def find_var(self, query, formatted=False):
        """
        Return variable names and indices matching ``query``
        """

        # load the variable list to search in
        names = self._uname if formatted is False else self._fname

        found_idx, found_names = list(), list()

        for idx, name in zip(self._idx, names):
            if re.search(query, name):
                found_idx.append(idx)
                found_names.append(name)

        return found_idx, found_names

    def load_dat(self, delimiter=','):
        """
        Load the dat file into internal data structures, ``self._data``
        """
        try:
            data = np.loadtxt(self._dat_file, delimiter=',')
        except ValueError:
            data = np.loadtxt(self._dat_file)

        self._data = data

    def get_values(self, idx):
        """
        Return the variable values at the given indices
        """
        if isinstance(idx, list):
            idx = np.array(idx, dtype=int)

        return self._data[:, idx]

    def get_header(self, idx, formatted=False):
        """
        Return a list of the variable names at the given indices
        """
        header = self._uname if not formatted else self._fname
        return [header[x] for x in idx]

    def export_csv(self, path, idx=None, header=None, formatted=False,
                   sort_idx=True, fmt='%.18e'):
        """
        Export to a csv file

        Parameters
        ----------
        path : str
            path of the csv file to save
        idx : None or array-like, optional
            the indices of the variables to export. Export all by default
        header : None or array-like, optional
            customized header if not `None`. Use the names from the lst file
            by default
        formatted : bool, optional
            Use LaTeX-formatted header. Does not apply when using customized
            header
        sort_idx : bool, optional
            Sort by idx or not, # TODO: implement sort
        fmt : str
            cell formatter
        """
        if not idx:
            idx = self._idx
        if not header:
            header = self.get_header(idx, formatted=formatted)

        assert len(idx) == len(header), \
            "Idx length does not match header length"

        body = self.get_values(idx)

        with open(path, 'w') as fd:
            fd.write(','.join(header) + '\n')
            np.savetxt(fd, body, fmt=fmt, delimiter=',')

    def plot(self, xidx, yidx, xname=None, yname=None, xlabel=None, ylabel=None,
             left=None, right=None, ytimes=1, yoffset=0,
             legend=True, grid=False, fig=None, ax=None,
             latex=True, dpi=200, save=None, exit=False
             ):
        # TODO: split this function into multiple so that manipulated data
        # can be used
        pass

    def _data_calc(self):
        """
        Manipulate the data such as adding, multiplying, differencing,
        and calculating rate of change
        """
        # TODO: split this function into multiple
        pass

    def _check_latex(self):
        """Check if latex is available"""
        pass

    def data_to_df(self):
        """Convert to pandas.DataFrame"""
        pass

    def guess_event_time(self):
        """Guess the event starting time from the input data by checking
        when the values start to change
        """
        pass


def cli_parse():
    """command line input parser"""
    parser = ArgumentParser(prog='andesplot')
    parser.add_argument('datfile', nargs=1, default=[], help='dat file name.')
    parser.add_argument('x', nargs=1, type=int, help='x axis variable index')
    parser.add_argument('y', nargs='*', help='y axis variable index')
    parser.add_argument('--xmax', type=float, help='x axis maximum value')
    parser.add_argument('--ymax', type=float, help='y axis maximum value')
    parser.add_argument('--ymin', type=float, help='y axis minimum value')
    parser.add_argument('--xmin', type=float, help='x axis minimum value')
    parser.add_argument(
        '--checkinit', action='store_true', help='check initialization value')
    parser.add_argument(
        '-x', '--xlabel', type=str, help='manual set x-axis text label')
    parser.add_argument('-y', '--ylabel', type=str, help='y-axis text label')
    parser.add_argument(
        '-s', '--save', action='store_true', help='save to file')
    parser.add_argument('-g', '--grid', action='store_true', help='grid on')
    parser.add_argument(
        '-d',
        '--no_latex',
        action='store_true',
        help='disable LaTex formatting')
    parser.add_argument(
        '-u',
        '--unattended',
        action='store_true',
        help='do not show the plot window')
    parser.add_argument('--ytimes', type=str, help='y times')
    parser.add_argument(
        '--dpi', type=int, help='image resolution in dot per inch (DPI)')
    args = parser.parse_args()
    return vars(args)


def parse_y(y, upper, lower=0):
    """
    Parse command-line input for Y indices and return a list of indices

    Parameters
    ----------
    y : Union[List, Set, Tuple]
        Input for Y indices. Could be single item (with or without colon), or
         multiple items

    upper : int
        Upper limit. In the return list y, y[i] <= uppwer.

    lower : int
        Lower limit. In the return list y, y[i] >= lower.

    Returns
    -------

    """
    if len(y) == 1:
        if isint(y[0]):
            y[0] = int(y[0])
            return y
        elif ':' in y[0]:
            y = y[0].split(':')

            # convert to integers
            for i in range(len(y)):
                if y[i] == '':
                    continue
                try:
                    y[i] = int(y[i])
                except ValueError:
                    logger.warning('y[{}] contains non-empty, non-numerical values {}.'.format(i, y[i]))
                    return []

            if y[0] == '':
                y[0] = 1
            elif not (lower <= y[0] <= upper + 1):
                logger.warning('y[0]={} out of limit. Reset to 1.'.format(y[0]))
                y[0] = 1

            if y[1] == '':
                y[1] = upper + 1
            elif not (lower <= y[1] <= upper + 1):
                logger.warning('y[1]={} out of limit. Reset to maximum={}'.format(y[1], upper + 1))
                y[1] = upper + 1

            # y may contain a third field in the list
            if len(y) == 3:
                if y[2] == '':
                    y[2] = 1
            return list(range(*y))
    else:
        for i in range(len(y)):
            try:
                y[i] = int(y[i])

            except ValueError:
                logger.warning('y contains non-numerical values. Parsing could not proceed.')
                return []

        y = [i for i in y if lower <= i <= upper]
        return list(y)


def get_nvars(dat):
    try:
        with open(dat, 'r') as f:
            line1 = f.readline()

        delim = ',' if ',' in line1 else ' '
        line1 = line1.strip().split(delim)
        return len(line1), delim
    except IOError:
        print('* Error while opening the dat file')


def read_dat(dat, x, y, delim=','):
    global dfile
    errid = 0
    xv = []
    yv = [list() for _ in range(len(y))]

    try:
        dfile = open(dat)
        dfile_raw = dfile.readlines()
        dfile.close()
    except IOError:
        print('* Error while opening the dat file')
        return None, None

    for _, line in enumerate(dfile_raw):
        thisline = line.rstrip('\n').split(delim)
        if not (x[0] <= len(thisline) and max(y) <= len(thisline)):
            errid = 1
            break

        xv.append(float(thisline[x[0]]))

        for idx, item in enumerate(y):
            yv[idx].append(float(thisline[item]))

    if errid:
        raise IndexError('x or y index out of bound')

    return xv, yv


def read_label(lst, x, y):
    global lfile
    xl = [list() for _ in range(2)]
    yl = [list() for _ in range(2)]
    yl[0] = [''] * len(y)
    yl[1] = [''] * len(y)

    xy = list(x)
    xy.extend(y)

    try:
        lfile = open(lst)
        lfile_raw = lfile.readlines()
        lfile.close()
    except IOError:
        print('* Error while opening the lst file')
        return None, None

    xidx = sorted(range(len(xy)), key=lambda i: xy[i])
    xsorted = sorted(xy)
    at = 0

    for line in lfile_raw:
        thisline = line.rstrip('\n').split(',')
        thisline = [item.lstrip() for item in thisline]
        if not isfloat(thisline[0].strip()):
            continue

        varid = int(thisline[0])
        if varid == xsorted[at]:
            if xsorted[at] == xy[0]:
                xl[0] = thisline[1]
                xl[1] = thisline[2].strip('#')
            else:
                yl[0][xidx[at] - 1] = thisline[1]
                yl[1][xidx[at] - 1] = thisline[2].strip('#')
            at += 1

        if at >= len(xy):
            break

    return xl, yl


def do_plot(xdata,
            ydata,
            xname=None,
            yname=None,
            fig=None,
            ax=None,
            dpi=200,
            xmin=None,
            xmax=None,
            ymin=None,
            ymax=None,
            xlabel=None,
            ylabel=None,
            no_latex=False,
            legend=True,
            grid=False,
            save=False,
            unattended=False,
            datfile='',
            noshow=False,
            **kwargs):

    # set styles and LaTex
    rc('font', family='Arial', size=12)
    linestyles = ['-', '--', '-.', ':'] * len(ydata)
    if not no_latex and find_executable('dvipng'):
        # use LaTex
        LATEX = True
        rc('text', usetex=True)
    else:
        LATEX = False
        rc('text', usetex=False)

    # get variable names from lst
    def get_lst_name(lst, LATEX):
        idx = 1 if LATEX else 0
        if lst is not None:
            return lst[idx]
        else:
            return None

    xl_data = get_lst_name(xname, LATEX)
    yl_data = get_lst_name(yname, LATEX)

    # set default x min based on simulation time
    if not xmin:
        xmin = xdata[0] - 1e-6
    if not xmax:
        xmax = xdata[-1] + 1e-6

    if not (fig and ax):
        fig = plt.figure(dpi=dpi)
        ax = plt.gca()

    for idx in range(len(ydata)):
        yl_data_idx = yl_data[idx] if yl_data else None
        ax.plot(xdata, ydata[idx], label=yl_data_idx, ls=linestyles[idx])

    if not xlabel:
        if xl_data is not None:
            ax.set_xlabel(xl_data)
    else:
        if LATEX:
            xlabel = '$' + xlabel.replace(' ', '\\ ') + '$'
        ax.set_xlabel(xlabel)

    if ylabel:
        if LATEX:
            ylabel = '$' + ylabel.replace(' ', '\\ ') + '$'
        ax.set_ylabel(ylabel)

    ax.ticklabel_format(useOffset=False)

    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(ymin=ymin, ymax=ymax)

    if grid:
        ax.grid(b=True, linestyle='--')
    if legend and yl_data:
        legend = ax.legend(loc='upper right')

    plt.draw()

    # output to file

    if save or unattended:
        name, _ = os.path.splitext(datfile[0])
        count = 1
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.startswith(name) and file.endswith('.png'):
                count += 1

        outfile = name + '_' + str(count) + '.png'

        try:
            fig.savefig(outfile, dpi=1200)
            print('Figure saved to file {}'.format(outfile))
        except IOError:
            print('* Error occurred. Try disabling LaTex with "-d".')
            return

    if unattended:
        noshow = True

    if not noshow:
        plt.show()

    return fig, ax


def add_plot(x, y, xl, yl, fig, ax, LATEX=False, linestyle=None, **kwargs):
    """Add plots to an existing plot"""
    if LATEX:
        # xl_data = xl[1]  # NOQA
        yl_data = yl[1]
    else:
        # xl_data = xl[0]  # NOQA
        yl_data = yl[0]

    for idx in range(len(y)):
        ax.plot(x, y[idx], label=yl_data[idx], linestyle=linestyle)

    ax.legend(loc='upper right')
    ax.set_ylim(auto=True)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def main(cli=True, **args):
    if cli:
        args = cli_parse()
    name, _ = os.path.splitext(args['datfile'][0])
    if 'out' in name:
        tds_plot(name, args)
    elif 'eig' in name:
        eig_plot(name, args)


def eig_plot(name, args):
    fullpath = os.path.join(name, '.txt')
    raw_data = []
    started = 0
    fid = open(fullpath)
    for line in fid.readline():
        if '#1' in line:
            started = 1
        elif 'PARTICIPATION FACTORS' in line:
            started = -1

        if started == 1:
            raw_data.append(line)
        elif started == -1:
            break
    fid.close()

    for line in raw_data:
        # data = line.split()
        # TODO: complete this function
        pass


def tds_plot(name, args):
    dat = os.path.join(os.getcwd(), name + '.dat')
    lst = os.path.join(os.getcwd(), name + '.lst')

    nvars, delim = get_nvars(dat)

    y = parse_y(args['y'], nvars, lower=0)
    try:
        xval, yval = read_dat(dat, args['x'], y, delim=delim)
    except IndexError:
        print('* Error: X or Y index out of bound')
        return

    xl, yl = read_label(lst, args['x'], y)

    if args.pop('checkinit', False):
        check_init(yval, yl[0])
        return
    ytimes = args.pop('ytimes', False)
    if ytimes:
        times = float(ytimes)
        new_yval = []
        for val in yval:
            new_yval.append([i * times for i in val])
        yval = new_yval

    args.pop('x')
    args.pop('y')
    do_plot(xval, yval, xl, yl, **args)


def check_init(yval, yl):
    """"Check initialization by comparing t=0 and t=end values"""
    suspect = []
    for var, label in zip(yval, yl):
        if abs(var[0] - var[-1]) >= 1e-6:
            suspect.append(label)
    if suspect:
        print('Initialization failure:')
        print(', '.join(suspect))
    else:
        print('Initialization is correct.')


if __name__ == "__main__":
    main(cli=True)
