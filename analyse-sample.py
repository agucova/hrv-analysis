import serial
import numpy as np
import heartpy as hp
import matplotlib
import csv
import pprint
from hrvanalysis import *

file = "samples/example.csv"

print("\nLoading sample data from", file + "\n")
data = np.loadtxt(file, delimiter=",", skiprows=(1), usecols=[1])
timer = np.loadtxt(file, delimiter=",", skiprows=(1), usecols=[0])
timer = timer*1000
fp = hp.get_samplerate_mstimer(timer)
print("Detected sampling frequency of", str(round(fp, 2)), "hertz.\n")
print("Preprocessing ECG data.\n")
data = hp.preprocess_ecg(data, fp)
print("Processing resulting data through heartpy.\n")
working_data, measures = hp.process(
    data, fp*2, reject_segmentwise=True, calc_freq=True)
print("Resulting measures (heartpy):\n")
pprint.pprint(measures)
print("\nProcessing heartpy's data using hrvanalysis.\n")
rrintervals = working_data["RR_list_cor"]

rrintervalswo = remove_outliers(rr_intervals=rrintervals,
                                low_rri=300, high_rri=2000)

intervals = interpolate_nan_values(rr_intervals=rrintervalswo,
                                   interpolation_method="linear")
tdFeatures = get_time_domain_features(intervals)
gFeatures = get_geometrical_features(intervals)
fdFeatures = get_frequency_domain_features(intervals)
ccFeatures = get_csi_cvi_features(intervals)

pprint.pprint(tdFeatures)
pprint.pprint(fdFeatures)
pprint.pprint(gFeatures)

hp.plotter(working_data, measures)
plot_poincare(intervals)
plot_timeseries(intervals)
