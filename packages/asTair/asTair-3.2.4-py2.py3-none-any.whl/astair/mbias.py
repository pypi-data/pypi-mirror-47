#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division

import re
import sys
import csv
import pdb
import numpy
import click
import logging
import warnings
from os import path
from math import ceil
from datetime import datetime

if sys.version[0] == '3':
    from itertools import zip_longest
elif sys.version[0] == '2':
    from itertools import izip_longest as zip_longest
else:
    raise Exception("This is not the python we're looking for (version {})".format(sys.version[0]))

try:
    import matplotlib as mplot
    mplot.use('Agg')
    import matplotlib.pyplot as pyp
    import matplotlib.ticker as ticker
    pyp.style.use('seaborn-whitegrid')
    pyp.ioff()
except Exception:
    warnings.warn("Matplotlib was not found, visualisation output will not be supported.", ImportWarning)

from astair.safe_division import non_zero_division
from astair.bam_file_parser import bam_file_opener
from astair.DNA_sequences_operations import complementary
from astair.simple_fasta_parser import fasta_splitting_by_sequence


@click.command()
@click.option('reference', '--reference', '-f', required=True, help='Reference DNA sequence in FASTA format.')
@click.option('input_file', '--input_file', '-i', required=True, help='BAM|CRAM format file containing sequencing reads.')
@click.option('directory', '--directory', '-d', required=True, help='Output directory to save files.')
@click.option('read_length', '--read_length', '-l', type=int, required=True, help='The read length is needed to calculate the Mbias.')
@click.option('method', '--method', '-m',  required=False, default='mCtoT', type=click.Choice(['CtoT', 'mCtoT']), help='Specify sequencing method, possible options are CtoT (unmodified cytosines are converted to thymines, bisulfite sequencing-like) and mCtoT (modified cytosines are converted to thymines, TAPS-like). (Default mCtoT).')
@click.option('per_chromosome', '--per_chromosome', '-chr', default=None, type=str, help='When used, it calculates the modification rates only per the chromosome given. (Default None).')
@click.option('single_end', '--se', '-se', default=False, is_flag=True, required=False, help='Indicates single-end sequencing reads (Default False).')
@click.option('plot', '--plot', '-p', required=False, is_flag=True, help='Phred scores will be visualised and output as a pdf file. Requires installed matplotlib.')
@click.option('colors', '--colors', '-c', default=['teal', 'gray', 'maroon'], type=list, required=False, help="List of color values used for visualistion of CpG, CHG and CHH modification levels per read, which are given as color1,color2,color3. Accepts valid matplotlib color names, RGB and RGBA hex strings and  single letters denoting color {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}. (Default 'teal','gray','maroon').")
@click.option('N_threads', '--N_threads', '-t', default=1, required=True, help='The number of threads to spawn (Default 1).')
def mbias(reference, input_file, directory, read_length, method, single_end, plot, colors, N_threads, per_chromosome):
    """Generate modification per read length information (Mbias). This is a quality-control measure."""
    Mbias_plotting(reference, input_file, directory, read_length, method, single_end, plot, colors, N_threads, per_chromosome)


warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

#logging.basicConfig(level=logging.WARNING)
logs = logging.getLogger(__name__)

time_b = datetime.now()

def initialise_data_counters(read_length):
    """Clean initialisation of empty dictionaries used for counters."""
    all_read_data = list(({}, {}, {}))
    for read_data in all_read_data:
        for i in range(0, read_length):
            read_data[i] = 0
    return all_read_data[0], all_read_data[1], all_read_data[2]


def strand_and_method(flag, ref_sequence, read_sequence, method, single_end):
    """Takes the positions of interest in the read given the flag and the method."""
    try:
        if single_end == False:
            if flag == 99 or flag == 147:
                ref, alt = 'C', 'T'
            elif flag == 163 or flag == 83:
                ref, alt, = 'G', 'A'
        else:
            if flag == 0:
                ref, alt = 'C', 'T'
            elif flag == 16:
                ref, alt, = 'G', 'A'
        cytosines_reference = [m.start() for m in re.finditer(ref, ref_sequence, re.IGNORECASE)]
        thymines_read = [m.start() for m in re.finditer(alt, read_sequence, re.IGNORECASE)]
        if method == 'mCtoT':
            positions = list(set(thymines_read).intersection(set(cytosines_reference)))
        elif method == 'CtoT':
            positions = list(set(cytosines_reference).difference(set(thymines_read)))
        return positions
    except (IndexError, TypeError, ValueError):
            logs.error('The input file does not contain a MD tag column.', exc_info=True)
            sys.exit(1)


def mbias_calculator(flag, ref_sequence, read_sequence, read_length, read_mods_CpG, read_mods_CHG, read_mods_CHH, read_umod_CpG, read_umod_CHG, read_umod_CHH, method, single_end):
    """Calculates the modification level per read position, pair orientation and cytosine context."""
    positions = strand_and_method(flag, ref_sequence, read_sequence, method, single_end)
    if single_end == False:
        OT, OB = [99, 147], [83, 163]
    else:
        OT, OB = [0], [16]
    if flag in OT:
        cpg_all = [m.start() for m in re.finditer(r'CG', ref_sequence, re.IGNORECASE)]
        chg_all = [m.start() for m in re.finditer(r'C(A|C|T)G', ref_sequence, re.IGNORECASE)]
        chh_all = [m.start() for m in re.finditer(r'C(A|C|T)(A|T|C)', ref_sequence, re.IGNORECASE)]
    elif flag in OB:
        cpg_all = [m.start() + 1 for m in re.finditer(r'CG', ref_sequence, re.IGNORECASE)]
        chg_all = [m.end()-1 for m in re.finditer(r'C(A|G|T)G', ref_sequence, re.IGNORECASE)]
        chh_all = list()
        for chh_ in ['AAC', 'CAC', 'TAC', 'ACC', 'CCC', 'TCC', 'ATC', 'CTC', 'TTC']:
            chh_all.extend([m.end()-1 for m in re.finditer(chh_, complementary(ref_sequence), re.IGNORECASE)])
    if len(positions) >= 1:
        cpg_mods = [x for x in positions if x in cpg_all]
        chg_mods = [x for x in positions if x in chg_all]
        chh_mods = [x for x in positions if x in chh_all]
        if len(read_sequence) <= read_length:
            for i in range(0, len(read_sequence)):
                if i in chh_mods:
                    read_mods_CHH[i] += 1
                elif i in chg_mods:
                    read_mods_CHG[i] += 1
                elif i in cpg_mods:
                    read_mods_CpG[i] += 1
                elif i in chh_all:
                    read_umod_CHH[i] += 1
                elif i in chg_all:
                    read_umod_CHG[i] += 1
                elif i in cpg_all:
                    read_umod_CpG[i] += 1
    else:
        if len(read_sequence) <= read_length:
            for i in range(0, len(read_sequence)):
                if i in chh_all:
                    read_umod_CHH[i] += 1
                if i in chg_all:
                    read_umod_CHG[i] += 1
                if i in cpg_all:
                    read_umod_CpG[i] += 1
    return read_mods_CpG, read_mods_CHG, read_mods_CHH, read_umod_CpG, read_umod_CHG, read_umod_CHH


def mbias_evaluater(input_file, read_length, method, single_end, N_threads, fastas, per_chromosome):
    """Outputs the modification levels per read position, pair orientation and cytosine context."""
    read1_mods_CHH, read1_mods_CHG, read1_mods_CpG = initialise_data_counters(read_length)
    read1_umod_CHH, read1_umod_CHG, read1_umod_CpG = initialise_data_counters(read_length)
    read2_mods_CHH, read2_mods_CHG, read2_mods_CpG = initialise_data_counters(read_length)
    read2_umod_CHH, read2_umod_CHG, read2_umod_CpG = initialise_data_counters(read_length)
    for read in bam_file_opener(input_file, 'fetch', N_threads):
        if single_end == False:
            exp1, exp2 = [99, 83], [147, 163]
        else:
            exp1, exp2 = [0], [16]
        if read.reference_length != 0:
            if (per_chromosome == None and read.flag in exp1) or (per_chromosome != None and read.reference_name == per_chromosome and read.flag in exp1):
                mbias_calculator(read.flag, fastas[read.reference_name][read.reference_start:read.reference_start+read.qlen], read.query_sequence, read_length, read1_mods_CpG, read1_mods_CHG, read1_mods_CHH, read1_umod_CpG, read1_umod_CHG, read1_umod_CHH, method, single_end)
            elif (per_chromosome == None and read.flag in exp2) or (per_chromosome != None and read.reference_name == per_chromosome and read.flag in exp2):
                mbias_calculator(read.flag, fastas[read.reference_name][read.reference_start:read.reference_start+read.qlen], read.query_sequence, read_length,read2_mods_CpG, read2_mods_CHG, read2_mods_CHH, read2_umod_CpG, read2_umod_CHG, read2_umod_CHH, method, single_end)
    return read1_mods_CpG, read1_mods_CHG, read1_mods_CHH, read1_umod_CpG, read1_umod_CHG, read1_umod_CHH,\
           read2_mods_CpG, read2_mods_CHG, read2_mods_CHH, read2_umod_CpG, read2_umod_CHG, read2_umod_CHH



def context_calculator(i, read_mods, read_umods, read_values):
    """Calculates summary statistics per context and read orientation."""
    read_values[i] = non_zero_division(read_mods[i], read_umods[i] + read_mods[i]) * 100
    values = [(keys + 1, round(vals[0], 3)) if isinstance(vals, list) else (keys + 1, round(vals, 3)) for keys, vals in read_values.items()]
    umod_counts = [(keys + 1, round(vals[0], 3)) if isinstance(vals, list) else (keys + 1, round(vals, 3)) for keys, vals in read_umods.items()]
    mod_counts = [(keys + 1, round(vals[0], 3)) if isinstance(vals, list) else (keys + 1, round(vals, 3)) for keys, vals in read_mods.items()]
    return read_values, values, umod_counts, mod_counts


def mbias_statistics_calculator(fastas, input_file, name, directory, read_length, method, single_end, N_threads, per_chromosome):
    """Creates a summary statistics of the modification levels per read position, pair orientation and cytosine context,
    and then writes them as a text file that can be used for independent visualisation."""
    read1_mods_CpG, read1_mods_CHG, read1_mods_CHH, read1_umod_CpG, read1_umod_CHG, read1_umod_CHH,\
    read2_mods_CpG, read2_mods_CHG, read2_mods_CHH, read2_umod_CpG, read2_umod_CHG, read2_umod_CHH \
        = mbias_evaluater(input_file, read_length, method, single_end, N_threads, fastas, per_chromosome)
    read_values_1_CpG, read_values_1_CHG, read_values_1_CHH = initialise_data_counters(read_length)
    read_values_2_CpG, read_values_2_CHG, read_values_2_CHH = initialise_data_counters(read_length)
    if single_end == True:
        for i in range(0, read_length):
            read1_mods_CpG[i] = read1_mods_CpG[i] + read2_mods_CpG[i]
            read1_mods_CHG[i] = read1_mods_CHG[i] + read2_mods_CHG[i]
            read1_mods_CHH[i] = read1_mods_CHH[i] + read2_mods_CHH[i]
            read1_umod_CpG[i] = read1_umod_CpG[i] + read2_umod_CpG[i]
            read1_umod_CHG[i] = read1_umod_CHG[i] + read2_umod_CHG[i]
            read1_umod_CHH[i] = read1_umod_CHH[i] + read2_umod_CHH[i]
    for i in range(0, read_length):
        read_values_1_CHH, values_1_CHH, umod_counts_1_CHH, mod_counts_1_CHH = context_calculator(i, read1_mods_CHH, read1_umod_CHH, read_values_1_CHH)
        read_values_1_CHG, values_1_CHG, umod_counts_1_CHG, mod_counts_1_CHG = context_calculator(i, read1_mods_CHG, read1_umod_CHG, read_values_1_CHG)
        read_values_1_CpG, values_1_CpG, umod_counts_1_CpG, mod_counts_1_CpG = context_calculator(i, read1_mods_CpG, read1_umod_CpG, read_values_1_CpG)
        read_values_2_CHH, values_2_CHH, umod_counts_2_CHH, mod_counts_2_CHH = context_calculator(i, read2_mods_CHH, read2_umod_CHH, read_values_2_CHH)
        read_values_2_CHG, values_2_CHG, umod_counts_2_CHG, mod_counts_2_CHG = context_calculator(i, read2_mods_CHG, read2_umod_CHG, read_values_2_CHG)
        read_values_2_CpG, values_2_CpG, umod_counts_2_CpG, mod_counts_2_CpG = context_calculator(i, read2_mods_CpG, read2_umod_CpG, read_values_2_CpG)
    all_values = [(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18) for
                  a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18 in
                  zip_longest(values_1_CpG, umod_counts_1_CpG, mod_counts_1_CpG, values_2_CpG,
                                            umod_counts_2_CpG, mod_counts_2_CpG,values_1_CHG, umod_counts_1_CHG,
                                            mod_counts_1_CHG,  values_2_CHG, umod_counts_2_CHG, mod_counts_2_CHG,
                                            values_1_CHH, umod_counts_1_CHH, mod_counts_1_CHH,  values_2_CHH, umod_counts_2_CHH, mod_counts_2_CHH)]
    all_values = [(all_values[i][0][0], all_values[i][0][1], all_values[i][1][1], all_values[i][2][1], all_values[i][3][1],
                   all_values[i][4][1], all_values[i][5][1], all_values[i][6][1], all_values[i][7][1], all_values[i][8][1],
                   all_values[i][9][1], all_values[i][10][1], all_values[i][11][1], all_values[i][12][1], all_values[i][13][1],
                   all_values[i][14][1], all_values[i][15][1], all_values[i][16][1], all_values[i][17][1]) for i in range(0, len(all_values))]
    try:
        with open(directory + name + "_Mbias.txt", 'w') as stats_file:
            line = csv.writer(stats_file, delimiter='\t', lineterminator='\n')
            if single_end == False:
                first, second = '1', '2'
            else:
                first, second = 'OT', 'OB'
            line.writerow(['POSITION_(bp)', 'MOD_LVL_CpG_READ_{}'.format(first), 'UNMOD_COUNT_CpG_READ_{}'.format(first), 'MOD_COUNT_CpG_READ_{}'.format(first),
                           'MOD_LVL_CpG_READ_{}'.format(second), 'UNMOD_COUNT_CpG_READ_{}'.format(second), 'MOD_COUNT_CpG_READ_{}'.format(second),
                           'MOD_LVL_CHG_READ_{}'.format(first), 'UNMOD_COUNT_CHG_READ_{}'.format(first), 'MOD_COUNT_CHG_READ_{}'.format(first),
                           'MOD_LVL_CHG_READ_{}'.format(second), 'UNMOD_COUNT_CHG_READ_{}'.format(second), 'MOD_COUNT_CHG_READ_{}'.format(second),
                           'MOD_LVL_CHH_READ_{}'.format(first), 'UNMOD_COUNT_CHH_READ_{}'.format(first), 'MOD_COUNT_CHH_READ_{}'.format(first),
                           'MOD_LVL_CHH_READ_{}'.format(second), 'UNMOD_COUNT_CHH_READ_{}'.format(second), 'MOD_COUNT_CHH_READ_{}'.format(second)])
            for row in all_values:
                line.writerow(row)
    except IOError:
        logs.error('asTair cannot write to Mbias file.', exc_info=True)
    return values_1_CpG, values_2_CpG, values_1_CHG, values_2_CHG, values_1_CHH, values_2_CHH

def Mbias_plotting(reference, input_file, directory, read_length, method, single_end, plot, colors, N_threads, per_chromosome):
    """The general M-bias calculation and statistics output function, which might be also visualised if the plotting module is enabled."""
    time_s = datetime.now()
    logs.info("asTair's M-bias summary function started running. {} seconds".format((time_s - time_b).total_seconds()))
    name = path.splitext(path.basename(input_file))[0]
    if list(directory)[-1]!="/":
        directory = directory + "/"
    if path.exists(directory) == False:
        raise Exception("The output directory does not exist.")
        sys.exit(1)
    keys, fastas = fasta_splitting_by_sequence(reference, per_chromosome, None)
    values_1_CpG, values_2_CpG, values_1_CHG, values_2_CHG, values_1_CHH, values_2_CHH = mbias_statistics_calculator(fastas, input_file, name, directory, read_length, method, single_end, N_threads, per_chromosome)
    try:
        if plot:
            if colors != ['teal', 'gray', 'maroon']:
                colors = "".join(colors).split(',')
            y_axis_CpG1, y_axis_CHG1, y_axis_CHH1, y_axis_CpG2, y_axis_CHG2, y_axis_CHH2 = list(), list(), list(), list(), list(), list()
            for row in values_1_CpG:
                y_axis_CpG1.append(row[1])
            for row in values_1_CHG:
                y_axis_CHG1.append(row[1])
            for row in values_1_CHH:
                y_axis_CHH1.append(row[1])
            for row in values_2_CpG:
                y_axis_CpG2.append(row[1])
            for row in values_2_CHG:
                y_axis_CHG2.append(row[1])
            for row in values_2_CHH:
                y_axis_CHH2.append(row[1])
            x_axis = [x for x in range(1,read_length+1)]
            pyp.figure()
            if single_end == False:
                fig, fq = pyp.subplots(2, 1)
            else:
                fig, fq = pyp.subplots(1, 1)
            fig.suptitle('Sequencing M-bias', fontsize=14)
            if single_end == False:
                pyp.subplots_adjust(hspace=0.4)
                pyp.subplots_adjust(right=1)
                fq[0].set_ylabel('Modification level, %', fontsize=12)
                fq[0].set_xlabel('First in pair base positions', fontsize=12)
                fq[0].plot(x_axis, y_axis_CpG1, linewidth=1.0, linestyle='-', color=colors[0])
                fq[0].plot(x_axis, y_axis_CHG1, linewidth=1.0, linestyle='-', color=colors[1])
                fq[0].plot(x_axis, y_axis_CHH1, linewidth=1.0, linestyle='-', color=colors[2])
                fq[0].xaxis.set_ticks(numpy.arange(0, read_length + 1, step=ceil(read_length / 10)))
                fq[0].yaxis.set_ticks(numpy.arange(0, 101, step=10))
                fq[0].grid(color='lightgray', linestyle='solid', linewidth=1)
                fq[1].set_ylabel('Modification level, %', fontsize=12)
                fq[1].set_xlabel('Second in pair base positions', fontsize=12)
                fq[1].plot(x_axis, y_axis_CpG2, linewidth=1.0, linestyle='-', color=colors[0])
                fq[1].plot(x_axis, y_axis_CHG2, linewidth=1.0, linestyle='-', color=colors[1])
                fq[1].plot(x_axis, y_axis_CHH2, linewidth=1.0, linestyle='-', color=colors[2])
                fq[1].xaxis.set_ticks(numpy.arange(0, read_length + 1, step=ceil(read_length/10)))
                fq[1].yaxis.set_ticks(numpy.arange(0, 101, step=10))
                fq[1].grid(color='lightgray', linestyle='solid', linewidth=1)
                pyp.figlegend(['CpG', 'CHG', 'CHH'], loc='center left', bbox_to_anchor=(1, 0.5))
            else:
                fq.set_ylabel('Modification level, %', fontsize=12)
                fq.set_xlabel('Base positions', fontsize=12)
                fq.plot(x_axis, y_axis_CpG1, linewidth=1.0, linestyle='-', color=colors[0])
                fq.plot(x_axis, y_axis_CHG1, linewidth=1.0, linestyle='-', color=colors[1])
                fq.plot(x_axis, y_axis_CHH1, linewidth=1.0, linestyle='-', color=colors[2])
                fq.xaxis.set_ticks(numpy.arange(0, read_length + 1, step=ceil(read_length / 10)))
                fq.yaxis.set_ticks(numpy.arange(0, 101, step=10))
                fq.grid(color='lightgray', linestyle='solid', linewidth=1)
                pyp.figlegend(['CpG', 'CHG', 'CHH'], loc='center left', bbox_to_anchor=(0.9, 0.5))
            pyp.savefig(directory + name + '_M-bias_plot.pdf', figsize=(16, 12), dpi=330, bbox_inches='tight', pad_inches=0.15)
            pyp.close()
    except Exception:
        logs.error('asTair cannot output the Mbias plot.', exc_info=True)
    else:
        pass
    time_m = datetime.now()
    logs.info("asTair's M-bias summary function finished running. {} seconds".format((
    time_m - time_b).total_seconds()))


if __name__ == '__main__':
    mbias()




