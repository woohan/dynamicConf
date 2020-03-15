# plot from mtr reports

import csv
import matplotlib.pyplot as plt
import numpy as np
import sys

fname = "/storage/hanwu/apps/4deliveryTest/mtrRecords/1212_msgs_default_2.csv"
dstnt = "/storage/hanwu/apps/4deliveryTest/mtrRecords/1212_plot_msgs_default_2_2.csv"

def clean_data(src, dst):
    with open(src) as f1, open(dst, "w") as f2:
        lines = f1.readlines()
        length = len(lines)
        data_lines = lines[1:length:2]
        f2.write(lines[0])
        for data_line in data_lines:
            f2.write(data_line)

def get_col(fname, cname):
    res = []
    with open(fname) as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            res.append(row[cname])
    return np.asarray(res, np.float)


clean_data(fname, dstnt)
rawTime = get_col(dstnt, 'Start_Time')
xAxis = rawTime - rawTime[0]

delay = get_col(dstnt, 'Last')
pktloss = get_col(dstnt, 'Loss%')

fig = plt.figure(1,(6,3.5))
ax1 = fig.add_subplot(1,1,1)

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Network delay (ms)')
ax1.plot(xAxis, delay, color='#255F85', linestyle=':', linewidth=0.85, label ='delay')
ax2 = ax1.twinx()
ax2.set_ylabel('Network packet loss rate (%)')
ax2.plot(xAxis, pktloss, color='#E55812', linewidth=0.85, alpha=0.85,label='packet loss')
ax1.set_ylim(0,200)
ax2.set_ylim(-5,50)
ax1.legend(loc=2)
ax2.legend(loc=1)
plt.show()


