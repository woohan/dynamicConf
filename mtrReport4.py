import os

confName = "video_dynamic"
fname = "/home/apps/deliveryTest/mtrRecords/"+confName+".csv"
target = "kfk4_node_1"
cmd = "mtr -C -c 1000 -i 0.01 "+target+" >> "+fname

for i in range(500):
    os.system(cmd)
