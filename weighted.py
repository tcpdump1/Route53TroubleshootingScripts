import collections
import subprocess
import re
import sys
import time

####This sections retrieves the nameserver to perform the test
create_file = subprocess.check_output(["touch", "weighted.txt"]) #creates a file to store logs
festac = subprocess.check_output(("dig", sys.argv[1], "+trace", "+short"))
ojodu = re.search(r"(A.+r)\s(\S+)", festac)

farum = subprocess.check_output(("dig","-x", ojodu.group(2), "+short")).strip()
benin = "@" + ojodu.group(2)

droppy = []

####This sections queries the authoritative nameservers
for i in range(30):
    auchi = subprocess.check_output(("dig", sys.argv[1], benin, "+short")).strip().splitlines()
    droppy.append(tuple(sorted(auchi)))
    time.sleep(2)
    print "Weighted routing policy test going on thirty times. Please wait for the final result."


####This sections counts the output of the result and presents it to the user.
delta=collections.Counter(droppy) #counts the number of items in the tuple list and create a dictionary based on that. Dict = {items:no of items}
print "\n"
output = open('weighted.txt', 'a+')
output.write("\nFINAL RESULTS")
output.write("\n=============")
print "FINAL RESULTS"
print "============="
print "This test was done using " + farum[:-1] + " authoritative nameserver."

output.write("\nThis test was done using " + farum[:-1] + " authoritative nameserver.\n")

for k,v in delta.items():
    blame = ((float(v)/30) * 100)
    cele = round(blame,2)
    percent = str(cele) + "%"
    output.write("\nThe DNS record %s resolved to %s %s times with %s ratio." % (sys.argv[1], list(k), str(v), percent))
    print "The DNS record %s resolved to %s %s times with %s ratio." % (sys.argv[1], list(k), str(v), percent)
output.write("\n")
output.close()

print "\nYOU CAN ALSO VIEW THE RESULTS IN \"weighted.txt\" FILE."