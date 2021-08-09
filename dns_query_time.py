from typing import List
import subprocess
import re
import sys
import time

DOMAIN_NAME = sys.argv[1]
RESULT_LIST = []

'''
Retrieves the authoritative nameservers for a
domain name

Args: Takes a domain name eg. ogbonosoup.com

Returns: A List of authoritative nameservers,
eg. [ns-1.awsdns-30.com, ns-2.awsdns-30.com,
ns-3.awsdns-30.com, ns-4.awsdns-30.com]
]
'''
def retrieve_auth_nameservers(DOMAIN_NAME : str) -> List:
    auth_nameservers = subprocess.check_output(["dig", DOMAIN_NAME, "NS", "+short"]).splitlines()
    auth_nameservers = [f'@{i.decode("utf-8")}' for i in auth_nameservers]
    
    return auth_nameservers


def query_nameservers(auth_nameservers : List, DOMAIN_NAME : str ):

    for nameservers in retrieve_auth_nameservers(DOMAIN_NAME):
        query_nameservers = subprocess.Popen(('dig', DOMAIN_NAME, nameservers), stdout=subprocess.PIPE)
        grep_query_output = subprocess.check_output(('grep', 'Query'), stdin=query_nameservers.stdout).strip()
        output_query_time = re.search(r"\d{1,10}\smsec", grep_query_output.decode("utf-8"))
        output_nameserver = nameservers.replace("@","")
        
        RESULT_LIST.append(f'{output_nameserver} takes {output_query_time.group()} to resolve {DOMAIN_NAME} domain')
 
    return("\n".join(RESULT_LIST))

if __name__ == "__main__":        
 
    exec = query_nameservers(auth_nameservers=retrieve_auth_nameservers(DOMAIN_NAME), DOMAIN_NAME=DOMAIN_NAME)
    print(exec)

'''
Opts, DOMAIN_NAME=DOMAIN_NAMEonal: Option to write output to text

Step 1: Create File
create_file = subprocess.check_output(["touch", "dns_query_time.txt"]) #creates a file to store logs

Step 2: Open File
output = open('dns_query_time.txt', 'a+') #writing to the file

Step 3: Write to File
output.write("\n" + abuja.group() + " takes " + benue.group() + " to resolve " + sys.argv[1] + " domain")
'''