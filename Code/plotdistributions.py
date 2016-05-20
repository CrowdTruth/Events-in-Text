import numpy as np
import scipy.stats as stats
import pylab as pl


def plot_distributions(sortedlist, title):
    fit = stats.norm.pdf(sortedlist, np.mean(sortedlist), np.std(sortedlist))  #this is a fitting indeed
    pl.title(title)
    pl.plot(sortedlist,fit,'-o')

    pl.hist(sortedlist,normed=True)      #use this to draw histogram of your data
    pl.savefig(title)
    pl.show()                   #use may also need add this 
