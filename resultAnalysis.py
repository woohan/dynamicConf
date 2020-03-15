# analyze the results of duplicate, lost messages
from termcolor import colored

totalMsgNum = 500100 # total number of messages sent from producer

fo = open('receivedMsgs')

sum_expect = totalMsgNum - 100 # the number of expected messages received

v1s = fo.readlines() # all messages received
v1_actual = set(v1s) # all different messages
sum_actual = len(v1_actual) # the actual number of different messages
sum_lost = sum_expect - sum_actual # the number of lost messages
per_lost = sum_lost/sum_expect # the percentage of lost messages
sum_duplicate = len(v1s) - sum_actual # the number of duplicated messages
per_duplicate = sum_duplicate/sum_expect # the percentage of duplicated msgs

print('Result analysis:-----------------------------------------------------')
print('The total number of messages received is', colored(len(v1s), 'yellow'))
print('The number of all different messages is', colored(sum_actual, 'magenta'))
print('The number of lost messages is', colored(sum_lost, 'red'), ', lost percentage:', colored(per_lost*100, 'red'), '%')
print('The number of duplicated messages is', colored(sum_duplicate, 'cyan'), ', duplicated percentage:', colored(per_duplicate*100, 'cyan'),'%')
print('---------------------------------------------------------------------')