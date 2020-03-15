# automatically run tests on Kafka kfk4
import uuid
import os
import numpy as np
import subprocess
from time import sleep
import logging
import sys
import json

# delay/packet loss rate of out going packages
# impacts = np.arange(30,150,10)
impacts = [0]
confName = 'video_dynamic'
logFileName = '1213_'+confName

#-----------------------Logger1 only outputs to file-----------------------#
formatter = logging.Formatter('%(asctime)s-[%(levelname)s]-{%(filename)s-%(lineno)d} - %(message)s')
# Time, log level, filename and line, value
logger1 = logging.getLogger("logger1")
hd1 = logging.FileHandler("/storage/hanwu/apps/4deliveryTest/recordData4/logs/"+logFileName+".log")
hd1.setFormatter(formatter)
logger1.addHandler(hd1)
logger1.setLevel(logging.INFO)  # Logger1 Level

logger2 = logging.getLogger("logger2")
hd2 = logging.FileHandler("/storage/hanwu/apps/4deliveryTest/recordData4/logs/"+logFileName+".log")
hd2.setFormatter(formatter)
logger2.addHandler(hd1)
logger2.addHandler(logging.StreamHandler(sys.stdout))
logger2.setLevel(logging.INFO)  # Logger2 Level
#--------------Logger2 outputs to both file&console---------------------#

def synrun_cmd(cmd):
    return subprocess.run(cmd.split(" "))

def asyrun_cmd(cmd):
    return subprocess.Popen(cmd.split(" "))

class netEmulate:
    def __init__(self, containers, tcparas):
        self.containers = containers
        self.tcparas = tcparas
    def startCmd(self):
        for c in self.containers:
            start_tc_cmd = "docker exec -it "+c+" tc qdisc add dev eth0 root netem delay "+self.tcparas['delay']+" "+self.tcparas['jitter']+" "+self.tcparas['correlation']+" "+self.tcparas['distribution']+" loss "+self.tcparas['packetloss']+" "+self.tcparas['gemodel']+" "+self.tcparas['p']+" "+self.tcparas['r']+" "+self.tcparas['1-h']+" "+self.tcparas['1-k']
            print(start_tc_cmd)
            os.system(start_tc_cmd)
    def stopCmd(self):
        for c in self.containers:
            stop_tc_cmd = f"docker exec -it {c} tc qdisc delete dev eth0 root"
            os.system(stop_tc_cmd)

with open('/storage/hanwu/apps/4deliveryTest/dynamicConfs/'+confName+'.json') as fp:
    faults = json.load(fp)

def runImpactsTests(stageNo):
    stageNo = stageNo
    tcparas = faults[stageNo]["tc"] # obtain tc parameters for current loop
    topic_name = str(uuid.uuid4()).replace("-", "")
    del_topic_cmd = ["docker",
        "exec", "kfk4_pro_1",
        "/home/apps/deliveryTest/deleteTopic.sh",
        topic_name]
    create_topic_cmd =["docker",
        "exec", "kfk4_pro_1",
        "/home/apps/deliveryTest/createTopic.sh",
        "3", "1", topic_name]

    p1 = netEmulate(["kfk4_pro_1", "kfk4_node_1", "kfk4_node_2", "kfk4_node_3"], tcparas) # The fault we want to inject in this loop
    con_cmd = ["docker",
            "exec", "kfk4_con_1", "python3",
            "/home/apps/deliveryTest/conTest4.py", topic_name, str(stageNo)]
    pro_cmd = ["docker",
            "exec", "kfk4_pro_1", "python3",
            "/home/apps/deliveryTest/proTest4.py", topic_name, str(stageNo)]
    mtr_cmd = ["docker", "exec", "kfk4_pro_1", "python3", "/home/apps/deliveryTest/mtrReport4.py"]

    subprocess.run(create_topic_cmd)
    logger2.info('Created Topic: '+topic_name)
    sleep(10)
    p1.startCmd()
    logger2.info('Network Fault Injected ...')
    logger2.info('Starting Producer ...')
    mtr_report = subprocess.Popen(mtr_cmd) # start mtr reporting
    pro_process = subprocess.Popen(pro_cmd)
    pro_process.wait()
    sleep(10)
    mtr_report.kill()
    p1.stopCmd()

    logger2.info('Network Fault stopped')
    logger2.info('Starting Consumer ...')
    sleep(20)
    con_process = subprocess.Popen(con_cmd)
    con_process.wait()

    subprocess.run(del_topic_cmd)
    logger2.info('Topic deleted')

for i in range(len(faults)):
    runImpactsTests(i)


