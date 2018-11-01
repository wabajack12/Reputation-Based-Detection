#!/usr/bin/env python
#Owen Sheets
#CSCI497L

import requests
import csv
import re

dataURL = "http://www.malwaredomainlist.com/mdlcsv.php"
ipURL = "http://www.malwaredomainlist.com/hostslist/ip.txt"

data = requests.get(dataURL)
ips = requests.get(ipURL)

dataList = []
ipList = []

categoryDict = {}
ipDict = {}

temp = csv.reader(data.text.splitlines(), delimiter=',')
dataList = list(temp)

temp2 = csv.reader(ips.text.splitlines(), delimiter="\n")
ipList = list(temp2)
for line in ipList:
   ipDict[line[0]] = 1
   

categories = []

count = 1

for line in dataList:
   if len(line) > 2:
      ip = re.search(r'[0-9]+(?:\.[0-9]+){3}' , line[2]).group(0)
      
      category = line[4]
      if ipDict[ip] < 127:
         ipDict[ip] += 1
      
      if category in categoryDict:
         categoryDict.get(category)[1].append(ip)
      else:
         categoryDict[category] = (count, [])
         categoryDict.get(category)[1].append(ip)
         count = count + 1
         
for category, value in categoryDict.items():
   categoryDict[category] = (value[0], set(value[1]))

      
file = open("mdl.list", "w")
count = 1
for ip, value in ipDict.items():
      file.write(ip + "," + str(count) + "," + str(value) + "\n")

#for category, value in categoryDict.items():
 #  categoryFile.write(str(count) + "," + category + "," + category + "\n")
  # count = count + 1
   
file.close()

