import numpy as np
import matplotlib.pyplot as plt
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
    
    def GetAddrAccess(self):
        array = self.GetArray()
        values, counts = np.unique(array, return_counts=True)
        count_sort_ind = np.argsort(-counts) # sort by count of accesses
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

    def PlotHistogram(self, lines=True, points=False, xscale=True, yscale=False): 
        accesses = self.GetAddrAccess()       
        address_bytes = np.arange(self.linspace_left, self.linspace_right , self.access_size)

        print("The len(accesses) is: ", len(accesses))
        print("The len(address_bytes) is: ", len(address_bytes))
        print("The address_bytes is: ", address_bytes)

        fig = plt.figure(figsize = (10, 5))
        if points:
            # create points histogram
            plt.plot(address_bytes, accesses, 'ro', markersize=3)   
        if lines:
            # create max lines histogram
            plt.plot(address_bytes, accesses)

        if xscale:
            plt.xscale('log')        
            access_ticks = np.logspace(np.log10(self.linspace_left), np.log10(self.linspace_right), 7, dtype = int)
            labels = [str(sub) + ' B' for sub in access_ticks]
            plt.xticks(access_ticks, labels)
        if yscale:
            plt.yscale('log')

        plt.xlabel('Addresses ('+ str(access_size) +' Bytes)')
        plt.ylabel('Accesses')

        testInfo = self.filename.split('-')
        plt.title('Histogram sorted by number of accesses, \n test name = ' + str(testInfo[1]) +', raw addresses = ' + str(self.address_count))
        fig.savefig(self.filename +'_hist.png', dpi = 100)


filename = str(sys.argv[1])
access_size = 1 # count of Bytes for associated with 1 memory access
first_skip_access_count = 40 # count of first minimum memory accesses for skipping (e.g. for starting from 200KB)
last_skip_access_count = 0 # count of last maximum memory accesses for skipping

x = Histogram(filename, access_size, first_skip_access_count, last_skip_access_count)
x.PlotHistogram(lines=True, points=True, xscale=True, yscale=False)