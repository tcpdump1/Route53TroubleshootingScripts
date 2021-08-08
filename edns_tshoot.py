import subprocess
import re
import sys
import time


create_file = subprocess.check_output(["touch", "edns_tshoot.txt"]) #creates a file to store logs

x = 0
while x <= 15:
    public_ip = subprocess.check_output(["curl", "-s", "checkip.amazonaws.com"]).strip() #Retrieves Public IP address of the user
    print "Your Public IP address is: " + public_ip
    
    dns_resolver = subprocess.check_output(["dig", "resolver-identity.cloudfront.net", "+short"]).strip()
    print "Your Public DNS Resolver IP address is: " + dns_resolver #Retrieves Public IP address of the resolver
    
    edns_support = subprocess.check_output(["dig", "edns-client-sub.net", "TXT", "+short",]).strip()
    local_time=time.asctime( time.localtime(time.time()) )
    
    if "True" in edns_support:
        print "Your Public DNS Resolver supports EDNS0 Client Subnet Extension."
        output = open('edns_tshoot.txt', 'a+')
        output.write("\nYour Public IP address is: " + public_ip + "\n" +
                     "Your Public DNS Resolver IP address is: " + dns_resolver + "\n" + 
                     "Your Public DNS Resolver supports EDNS0 Client Subnet Extension." + "\n" + #Checks for EDNS support
                     "The Local Time and Date is: " + local_time )
        output.close()
        
    
    else:
        print "Your DNS Resolver does not support EDNS0 Client Subnet Extension."
        output = open('edns_tshoot.txt', 'a+')
        output.write("\nYour Public IP address is: " + public_ip + "\n" +
                     "Your Public DNS Resolver IP address is: " + dns_resolver + "\n" +
                     "Your Public DNS Resolver does not support EDNS0 Client Subnet Extension." + "\n" +
                     "The Local Time and Date is: " + local_time + "\n" +
                     "       ")
        output.close()
        
    print "The Local Time and Date is: " + local_time + "\n"   
    x += 1
    time.sleep(2)
    
print "\nTHE TEST IS COMPLETE. YOU CAN VIEW THE RESULTS IN \"edns_tshoot.txt\" FILE."

