#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse

class HistogramWssData:
    def __init__(self, filename, access_size = 4, measure=' Kb', left_skip_access_count=0, right_skip_access_count=0, extremum_size=-1):
        self.filename = filename # file with raw memory addresses, filename = <prefix>-<testname>
        self.testInfo = self.filename.split('-')
        if len(self.testInfo) < 2:
            print("incorrect filename template, please use: <prefix>-<testname>")
            exit(1)
        self.access_size = access_size # size of measure associated with 1 memory access on OX
        self.measure = measure # unit of measure for the amount of memory on OX
        self.left_skip_access_count = left_skip_access_count # number of first memory accesses to skip while drawing
        self.right_skip_access_count = right_skip_access_count # number of last memory accesses to skip while drawing
        self.extremum_size = extremum_size # point on OX for drawing straight lines around extremum, should be a multiple of access_size value
        self.address_count = 0 
        self.linspace_left = 0
        self.linspace_right = 0

    def GetArray(self):
        with open(self.filename, 'r') as f:
          lines = f.readlines()
        self.address_count = len(lines)
        lines = [line.replace(' ', '') for line in lines]  
        with open(self.filename, 'w') as f:  
            f.writelines(lines)
        array = []  
        with open(self.filename) as my_file:  
            array = my_file.read().splitlines()
        return array
    
    def GetAddrAccess(self):
        array = self.GetArray()
        values, counts = np.unique(array, return_counts=True)
        count_sort_ind = np.argsort(-counts) # sort by number of accesses
        #count_sort_ind = np.argsort(values) # sort by addresses
        addresses = values[count_sort_ind]
        accesses = counts[count_sort_ind]

        self.linspace_left = (self.left_skip_access_count + 1) * self.access_size
        self.linspace_right = (len(accesses) + 1 - self.right_skip_access_count) * self.access_size
        if self.left_skip_access_count != 0:
            accesses = accesses[self.left_skip_access_count:]
        if self.right_skip_access_count != 0:
            accesses = accesses[:-self.right_skip_access_count]
        print("The addresses is: ", addresses)
        print("The accesses is: ", accesses)
        return accesses

    def PlotHistogram(self, lines=True, points=False, xscale=True, yscale=False): 
        accesses = self.GetAddrAccess()       
        address_sizes = np.arange(self.linspace_left, self.linspace_right , self.access_size)

        print("The len(accesses) is: ", len(accesses))
        print("The len(address_sizes) is: ", len(address_sizes))
        print("The address_sizes is: ", address_sizes)

        fig = plt.figure(figsize = (10, 5))
        if points:
            # create points histogram
            plt.plot(address_sizes, accesses, 'ro', markersize=1)   
        if lines:
            # create max lines histogram
            plt.plot(address_sizes, accesses, linewidth=0.5)

        if xscale:
            plt.xscale('log')        
            access_ticks = np.logspace(np.log10(self.linspace_left), np.log10(self.linspace_right), 7, dtype = int)
            labels = [str(sub) + self.measure for sub in access_ticks]
            plt.xticks(access_ticks, labels)
        else:
            access_ticks = np.linspace(self.linspace_left, self.linspace_right, 7, dtype = int)
            labels = [str(sub) + self.measure for sub in access_ticks]
            plt.xticks(access_ticks, labels)

        if yscale:
            plt.yscale('log')

        if self.extremum_size !=-1:
            if extremum_size % self.access_size != 0:
                print("Plot extremum lines, incorrect condition: extremum_size should be a multiple of access_size value, skip")
            else:
                size_point = self.extremum_size
                accesses_point = accesses[np.where(address_sizes==size_point)]
                plt.axvline(x=size_point, color='b', ls='--', lw=0.5, label='size = ' + str(size_point) + self.measure)
                plt.axhline(y=accesses_point, color='g', ls='--', lw=0.5, label='accesses = ' + str(accesses_point)[1:-1])
                plt.legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')

        plt.xlabel('Size ('+ str(access_size) +' Kb)')
        plt.ylabel('Accesses')
        plt.title('Histogram sorted by number of accesses, \n test name = ' + str(self.testInfo[1]) +', raw addresses = ' + str(self.address_count))
        hist_name = self.filename +'_hist.png'
        fig.savefig(hist_name, dpi = 300)
        print("Saving a histogram: ", hist_name)


parser = argparse.ArgumentParser("HWSW-36",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", type=str, required=True, metavar="file_path",
    help='File with memory addresses.')
parser.add_argument("-s", "--size", type=int, default=4,
    help='Size of measure in Kb associated with 1 memory access')
parser.add_argument("-sl", "--skip_left", type=int, default=0,
    help='Number of first memory accesses to skip while drawing')
parser.add_argument("-sr", "--skip_right", type=int, default=0,
    help='Number of last memory accesses to skip while drawing')
parser.add_argument("-e", "--extremum", type=int, default=-1,
    help='Point on OX for drawing straight lines around extremum, should be a multiple of size value. Can be found by hands.')
args = parser.parse_args()

data_file = args.file
filename = data_file.rsplit("/")[-1]
if not os.path.isfile(data_file):
    print("Invalid file path: {0}".format(data_file))
    exit(1)

access_size = args.size
measure = ' Kb'
left_skip_access_count = args.skip_left
right_skip_access_count = args.skip_right
extremum_size = args.extremum

x = HistogramWssData(filename, access_size, measure, left_skip_access_count, right_skip_access_count, extremum_size)
x.PlotHistogram(lines=True, points=True, xscale=True, yscale=True)