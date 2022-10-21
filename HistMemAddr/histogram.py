import numpy as np
import matplotlib.pyplot as plt
import pathlib
import sys

class Histogram:
    def __init__(self, filename, access_size, first_skip_access_count, last_skip_access_count):
        self.filename = filename
        self.address_count = 0
        self.access_size = access_size
        self.first_skip_access_count = first_skip_access_count
        self.last_skip_access_count = last_skip_access_count
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
    
    def GetMemSizes(self):
        array = self.GetArray()
        values, counts = np.unique(array, return_counts=True)
        count_sort_ind = np.argsort(counts) # sort by count of accesses
        addresses = values[count_sort_ind]
        accesses = counts[count_sort_ind]
        mem_sizes = accesses * self.access_size
        print("The addresses is: ", addresses)
        print("The accesses is: ", accesses)
        print("The mem_sizes is: ", mem_sizes)
        return mem_sizes
    
    
    def GetSizeFreq(self):
        mem_sizes = self.GetMemSizes()
        uniq_sizes, freq = np.unique(mem_sizes, return_counts=True)

        uniq_sizes = uniq_sizes[self.first_skip_access_count:]
        freq = freq[self.first_skip_access_count:]

        if self.last_skip_access_count!=0:
            uniq_sizes = uniq_sizes[:-self.last_skip_access_count]
            freq = freq[:-self.last_skip_access_count]

        self.linspace_left = uniq_sizes[0]
        self.linspace_right = uniq_sizes[-1]
    
        print("The uniq_sizes is: ", uniq_sizes)
        print("The freq is: ", freq)
    
        freq_sort_ind = np.argsort(freq) # sort by freq of accesses
        uniq_sizes = uniq_sizes[freq_sort_ind]
        freq = freq[freq_sort_ind]
    
        return uniq_sizes, freq
    
    def GetMaxSizeFreq(self):
        uniq_sizes, freq = self.GetSizeFreq()
        size_tmp = uniq_sizes[0]
        freq_tmp = freq[0]
    
        uniq_freq = []
        uniq_freq_size = []
        for s, f in zip(uniq_sizes, freq):
            if size_tmp < s and freq_tmp == f:
                size_tmp = s
            if freq_tmp != f:
                uniq_freq.append(freq_tmp)
                freq_tmp = f
                uniq_freq_size.append(size_tmp)
                size_tmp = s
            if s == uniq_sizes[-1]:
                uniq_freq.append(freq_tmp)
                uniq_freq_size.append(size_tmp)
    
        print("The uniq_freq_size is: ", uniq_freq_size)
        print("The uniq_freq is: ", uniq_freq)
    
        return uniq_freq_size, uniq_freq
    
    def PlotHistogram(self, lines=True, points=False):     
        if points:
            uniq_sizes, freq = self.GetSizeFreq()
            # create points histogram
            plt.plot(uniq_sizes, freq, 'ro', markersize=3)   
        if lines:
            uniq_freq_size, uniq_freq = self.GetMaxSizeFreq()
            # create max lines histogram
            plt.plot(uniq_freq_size, uniq_freq)

        plt.yscale('log')

        testInfo = self.filename.split('-')
        
        access_ticks = np.linspace(self.linspace_left, self.linspace_right, 5)
        labels = [str(sub) + ' KB' for sub in access_ticks]
        plt.xticks(access_ticks, labels)

        plt.xlabel('Addresses ('+ str(access_size) +' KB)')
        plt.ylabel('Accesses')

        plt.title('Histogram sorted by number of accesses, \n test name = ' + str(testInfo[1]) +', raw addresses = ' + str(self.address_count))
        plt.savefig(self.filename +'_hist.png')
    

filename = str(sys.argv[1])
access_size = 4 # count of KB for associated with 1 memory access
first_skip_access_count = 0 # count of first minimum memory accesses for skipping (e.g. skip 4KB, 8KB, .. 100KB and save other)
last_skip_access_count = 0 # count of last maximum memory accesses for skipping

x = Histogram(filename, access_size, first_skip_access_count, last_skip_access_count)

x.PlotHistogram(True, True) # lines=True, points=True
