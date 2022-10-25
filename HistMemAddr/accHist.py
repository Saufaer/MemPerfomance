#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys

class Histogram:
    def __init__(self, filename, access_size=4, measure=' Kb', first_skip_access_count=0, last_skip_access_count=0, extremum_size=-1):
        self.filename = filename
        self.address_count = 0
        self.access_size = access_size
        self.measure = measure
        self.first_skip_access_count = first_skip_access_count
        self.last_skip_access_count = last_skip_access_count
        self.linspace_left = 0
        self.linspace_right = 0
        self.extremum_size = extremum_size

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

        self.linspace_left = (self.first_skip_access_count + 1) * self.access_size
        self.linspace_right = (len(accesses) + 1 - self.last_skip_access_count) * self.access_size
        if self.first_skip_access_count != 0:
            accesses = accesses[self.first_skip_access_count:]
        if self.last_skip_access_count != 0:
            accesses = accesses[:-self.last_skip_access_count]
        print("The addresses is: ", addresses)
        print("The accesses is: ", accesses)
        return accesses

    def PlotHistogram(self, lines=True, points=False, xscale=True, yscale=False, extremum=False): 
        accesses = self.GetAddrAccess()       
        address_bytes = np.arange(self.linspace_left, self.linspace_right , self.access_size)

        print("The len(accesses) is: ", len(accesses))
        print("The len(address_bytes) is: ", len(address_bytes))
        print("The address_bytes is: ", address_bytes)

        fig = plt.figure(figsize = (10, 5))
        if points:
            # create points histogram
            plt.plot(address_bytes, accesses, 'ro', markersize=1)   
        if lines:
            # create max lines histogram
            plt.plot(address_bytes, accesses, linewidth=0.5)

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

        if extremum and extremum_size != -1:
            size_point = self.extremum_size
            accesses_point = accesses[np.where(address_bytes==size_point)]
            plt.axvline(x=size_point, color='b', ls='--', lw=0.5, label='size = ' + str(size_point) + self.measure)
            plt.axhline(y=accesses_point, color='g', ls='--', lw=0.5, label='accesses = ' + str(accesses_point)[1:-1])
            plt.legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')

        plt.xlabel('Size ('+ str(access_size) +' Kb)')
        plt.ylabel('Accesses')



        testInfo = self.filename.split('-')
        plt.title('Histogram sorted by number of accesses, \n test name = ' + str(testInfo[1]) +', raw addresses = ' + str(self.address_count))
        fig.savefig(self.filename +'_hist.png', dpi = 300)


filename = str(sys.argv[1])
access_size = 4 # count of Bytes for associated with 1 memory access
measure = ' Kb'
first_skip_access_count = 0 # count of first memory accesses for skipping (e.g. for starting from 200KB)
last_skip_access_count = 0 # count of last memory accesses for skipping
extremum_size = 1536 # point on OX for drawing straight lines around extremum, should be a multiple of access_size value

x = Histogram(filename, access_size, measure, first_skip_access_count, last_skip_access_count, extremum_size)
x.PlotHistogram(lines=True, points=True, xscale=True, yscale=True, extremum=True)