#!/usr/bin/env python3

""" argv[1]= log to analyze"""

import re
import csv
import sys
import operator

error = {}
per_user = {}

def define_group(line):
    #Divide in loglines in (type,message, user)
    pattern = r"(INFO|ERROR) ([\w' ]+|[\w\[\]#' ]+) (\(\w+\)|\(\w+\.\w+\))$"
    m=re.search(pattern,line)
    user=str(m.group(3)[1:-1])
    log_type=m.group(1)
    message=m.group(2)
    return(user,log_type,message)

def combine_error(file):
    # add error to dictionary
    with open(file, 'r') as log_file:
        for logline in log_file.readlines():
            user, log_type, message = define_group(logline)
            if log_type == 'ERROR':
                if message in error:
                    error[message] += 1
                else:
                    error[message] =1
    log_file.close
    error_ = sorted(error.items(),key=operator.itemgetter(1),reverse=True)
    return error_  

def user_stat(file):
    #add user stats
    with open(file, 'r') as f:
        for logline in f.readlines():
            user, log_type, message = define_group(logline)
            if user not in per_user:
                if log_type == "ERROR":
                    per_user[user]={"ERROR":1,"INFO":0}
                else:
                    per_user[user]={"ERROR":0,"INFO":1}
            else:
                per_user[user][log_type] += 1      
    f.close  
    per_user_= sorted(per_user.items())
    return per_user_               


def to_cvs(per_user_,error_):
    #convert to csv
    with open ("user_statistics.csv", 'w') as user_csv:
        writer = csv.writer(user_csv)
        writer.writerow(["Username", "INFO", "ERROR"])
        for item in per_user_: 
            user, typelog = item
            line_ = [user,typelog["INFO"],typelog["ERROR"]]
            writer.writerow(line_)   

    with open ("error_message.csv", 'w') as error_report:
        writer = csv.writer(error_report)
        writer.writerow(["Error","Count"])
        writer.writerows(error_)        
            
if __name__ == "__main__":
    logfile = sys.argv[1]          
    error_list = combine_error(logfile)
    user_list = user_stat(logfile)
    to_cvs(user_list,error_list)
