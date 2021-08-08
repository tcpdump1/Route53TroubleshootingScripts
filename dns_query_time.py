#!/usr/bin/env python2
import subprocess
import re
import sys
import time



create_file = subprocess.check_output(["touch", "dns_query_time.txt"]) #creates a file to store logs
festac = subprocess.check_output(("dig", sys.argv[1], "NS", "+short")).splitlines() #splits authoritative nameserver response into a list


aces = ["@" + festac for festac in festac] #appends @ to all of the nameservers

x = 0
while x <= 5:

    for i in aces:
        oshodi = subprocess.Popen(('dig', sys.argv[1], i), stdout=subprocess.PIPE)
        mushin = subprocess.check_output(('grep', 'Query'), stdin=oshodi.stdout).strip()
        oshodi.wait()
        benue = re.search(r"\d{1,10}\smsec", mushin)
        abuja = re.search(r"n.+[t,g,k,m]", i)
        
        output = open('dns_query_time.txt', 'a+') #writing to the file
        output.write("\n" + abuja.group() + " takes " + benue.group() + " to resolve " + sys.argv[1] + " domain")
        print abuja.group() + " takes " + benue.group() + " to resolve " + sys.argv[1] + " domain"
    print "\n"
    output.write("\n")
    output.close()
    x+=1
    time.sleep(2)
    
print "\nTHE TEST IS COMPLETE. YOU CAN VIEW THE RESULTS IN \"dns_query_time.txt\" FILE."