#!/usr/bin/python3

import sys
import os
import time
from matplotlib import pyplot as plt
import numpy as np

# associtivity range
assoc_range = [1, 2, 4]
# block size range
bsize_range = [b for b in range(6, 7)]
# capacity range
cap_range = [c for c in range(11, 21)]
# number of cores (1, 2, 4)
cores = [1]
# coherence protocol: (none, vi, or msi)
protocol='none'

expname='exp1'
figname='graph2.png'


def get_stats(logfile, key):
    for line in open(logfile):
        if line[2:].startswith(key):
            line = line.split()
            return float(line[1])
    return 0

def run_exp(logfile, core, cap, bsize, assoc):
    trace = 'trace.%dt.long.txt' % core
    cmd="./p5 -t %s -p %s -n %d -cache %d %d %d >> %s" % (
            trace, protocol, core, cap, bsize, assoc, logfile)
    print(cmd)
    os.system(cmd)

def graph():
    timestr = time.strftime("%m.%d-%H_%M_%S")
    folder = "results/"+expname+"/"+timestr+"/"
    os.system("mkdir -p "+folder)

    byte_traffic = {a:[] for a in assoc_range}

    for a in assoc_range:
        for b in bsize_range:
            for c in cap_range:
                for d in cores:
                    logfile = folder+"%s-%02d-%02d-%02d-%02d.out" % (
                            protocol, d, c, b, a)
                    run_exp(logfile, d, c, b, a)
                    byte_traffic[a].append(get_stats(logfile, 'B_written_cache_to_bus_wb'))

    plots = []
    for a in byte_traffic:
        p,=plt.plot([2**i for i in cap_range], byte_traffic[a])
        plots.append(p)
    plt.legend(plots, ['assoc %d' % a for a in assoc_range])
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)
    plt.title('Graph #2: CtB Byte Traffic vs Cache Size')
    plt.xlabel('Capacity')
    plt.ylabel('Cache to Bus Byte Traffic')
    plt.savefig(figname)

    # # Set the ticks and labels for the y-axis
    # num_ticks = 10
    # y_ticks = np.linspace(0, 1, num_ticks)
    # plt.yticks(y_ticks)

    # plt.savefig(figname)
    plt.show()

graph()