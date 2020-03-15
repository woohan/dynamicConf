# producer api
import os
from confluent_kafka import Producer
import numpy as np
import subprocess
import strgen
import sys
import time
import logging
import json

confName = 'video_dynamic'
with open('/home/apps/deliveryTest/dynamicConfs/'+confName+'.json') as fp:
    decisions = json.load(fp)
stageNo = int(sys.argv[2])

def getDic(target):
    return decisions[stageNo][target]

totalMsgNum = getDic("globalparas")["total.num.messages"]
msgPayload = getDic("globalparas")["message.size"]-57 # message size
proparas = getDic("producer") # Obtain the producer json
# print("totalMsgNum:",totalMsgNum,"msgPayload",msgPayload)
# sys.exit(0)
logFileName = '1212_'+confName

#-----------------------Logger1 only outputs to file-----------------------#
formatter = logging.Formatter('%(asctime)s-[%(levelname)s]-{%(filename)s-%(lineno)d} - %(message)s')
# Time, log level, filename and line, value
logger1 = logging.getLogger("logger1")
hd1 = logging.FileHandler("/home/apps/deliveryTest/recordData4/logs/"+logFileName+".log")
hd1.setFormatter(formatter)
logger1.addHandler(hd1)
logger1.setLevel(logging.DEBUG)  # Logger1 Level

logger2 = logging.getLogger("logger2")
hd2 = logging.FileHandler("/home/apps/deliveryTest/recordData4/logs/"+logFileName+".log")
hd2.setFormatter(formatter)
logger2.addHandler(hd1)
logger2.addHandler(logging.StreamHandler(sys.stdout))
logger2.setLevel(logging.DEBUG)  # Logger2 Level
#--------------Logger2 outputs to both file&console---------------------#


# TODO maybe we can change IPs automatically...
proparas["bootstrap.servers"] = ["172.29.0.3:9092,172.29.0.4:9092,172.29.0.2:9092"]
proConf = proparas

producer = Producer(proConf)
msg = ''
topicName = sys.argv[1]

def send_report(err, msg):
    if err:
        logger1.debug(err)

startTime = time.time()
for i in range(totalMsgNum):
# generate sequential and continues numbers as the first part of each message
    v1 = '{0:07}'.format(i)
# generate a message with certain bits
    v2Bit = str(msgPayload) # bit
    v2 = strgen.StringGenerator("[\d\w]{"+v2Bit+"}").render()
    msg = str(v1+','+v2)
    try:
        producer.poll(getDic("globalparas")["poll.interval"])
        producer.produce(topicName, bytes(msg, 'utf-8'),callback=send_report)
    except BufferError as bfer:
        logger2.error(bfer)
        producer.poll(getDic("globalparas")["poll.interval"])
    # logger1.debug(v1+'sent')
    # if i%100==0:
    #     time.sleep(0.001)

producer.flush()
endTime = time.time()

getDelay = float(getDic("tc")["delay"].replace("ms",""))*2
try:
    getPktloss = float(getDic("tc")["packetloss"].replace("%",""))
except ValueError:
    getPktloss = "10"

del proConf['bootstrap.servers']
proConf['message.size'] = sys.getsizeof(msg)
proConf['network.delay'] = getDelay
proConf['packet.loss'] = getPktloss
proConf['total.produce.time'] = endTime-startTime
proConf['poll.timeout.ms'] = getDic("globalparas")["poll.interval"]
with open('/home/apps/deliveryTest/parameters.json', "w") as fw:
    json.dump(proConf, fw)

logger2.info('Total time for sending messages to topic is '+ str(endTime-startTime)+' seconds')
logger2.info('The size of each message is '+str(sys.getsizeof(msg))+' bytes')

