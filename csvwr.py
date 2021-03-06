#!/usr/bin/env python3
import csv
import re
import sys
import os

count = 0
hasFailed = False
namePattern = 'function(.*)thread'
linePattern = 'line(.*)function'
fileNamePattern = 'FILE](.*)'
funcVeriPattern = 'FUNCTION](.*)'
fileName = ''
funcVeri = ''
functionName = ''
functionLine = ''
errorPattern = 'Violated property'
errorName = ''
DIRECTORY = "output"

print("Saving Output...")

with open(os.path.join(DIRECTORY,'output.csv'), mode='w') as csv_file:
    fieldnames = ['fileName', 'functionVerified', 'functionName', 'functionLine', 'status', 'error']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator = '\n')
    writer.writeheader()

    with open(os.path.join(DIRECTORY, "output.log")) as fp: 
        lines = fp.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            
            if('FILE' in line):
                match = re.search(fileNamePattern, line)
                if(match):
                    fileName = match.group(1)
            
            if('FUNCTION' in line):
                match = re.search(funcVeriPattern, line)
                if(match):
                    funcVeri = match.group(1)

            if('Counterexample' in line):
                hasFailed = True
            
            if(hasFailed):
                match = False
                functionName = ''
                functionLine = ''
                errorName = ''
                
                # Find Line
                match = re.search(linePattern, line, re.IGNORECASE)
                if(match):
                    functionLine = match.group(1)

                # Find function name
                match = re.search(namePattern, line, re.IGNORECASE)
                if(match):
                    functionName = match.group(1)

                    # Find error name
                    for j in range(1,6):
                        newLine = lines[i + j]
                        match = re.search(errorPattern, newLine, re.IGNORECASE)
                        if(match):
                            errorName = lines[i + j + 2].rstrip()

                            if(functionName != '' or errorName != ''):
                                writer.writerow({'fileName': fileName, 'functionVerified': funcVeri, 'functionName': functionName, 
                                'functionLine': functionLine, 'status' : 'Failed', 'error' : errorName})

                

csv_file.close()
