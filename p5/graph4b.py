#!/usr/bin/python3

import sys
import os
import time
from matplotlib import pyplot as plt
import numpy as np

# associtivity range
assoc_range = [4]
# block size range
bsize_range = [b for b in range(2,15)]
# capacity range
cap_range = [16]
# number of cores (1, 2, 4)
cores = [1, 2, 4]
# coherence protocol: (none, vi, or msi)
protocol='none'

expname='exp1'
figname='graph4b.png'


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

    miss_rate = {a:[] for a in cores}

    for a in assoc_range:
        for b in bsize_range:
            for c in cap_range:
                for d in cores:
                    logfile = folder+"%s-%02d-%02d-%02d-%02d.out" % (
                            protocol, d, c, b, a)
                    run_exp(logfile, d, c, b, a)
                    miss_rate[d].append(get_stats(logfile, 'miss_rate'))

    plots = []
    for a in miss_rate:
        p,=plt.plot([2**i for i in bsize_range], miss_rate[a])
        plots.append(p)
    plt.legend(plots, ['Miss Rate in Core 0 for %d cores' % i for i in cores])
    plt.xscale('log', base=2)
    plt.title('Graph #4b: Miss Rate vs Block Size')
    plt.xlabel('Block Size')
    plt.ylabel('Miss Rate')
    plt.ylim(0, 25)
    plt.savefig(figname)

    # # Set the ticks and labels for the y-axis
    # num_ticks = 10
    # y_ticks = np.linspace(0, 1, num_ticks)
    # plt.yticks(y_ticks)

    # plt.savefig(figname)
    plt.show()

graph()