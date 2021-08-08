# Route53TroubleshootingScripts

I created some python scripts that can easily get the required data for troubleshooting when having DNS issues with Route53. Since most Linux hosts have python interpreters already installed in them, its easy to run them. I will explain how to use them shortly:

PYTHON LIBRARIES/MODULES USED:
1) Collections
2) Subprocess
3) Regular Expressions (re)
4) Sys
5) Time

GEOLOCATION/LATENCY BASED ROUTING TROUBLESHOOTING: The python script used to troubleshoot geolocation/latency related cases is called edns_tshoot.py. It is very easy to use. Save the file in a linux host, then run this on the command line interface of the Linux host: "python edns_tshoot.py" (without quotations). The script will display the output containing the details needed to troubleshoot and also save the output in a file called edns_tshoot.txt. 
#####################

Your Public IP address is: 34.240.231.139

Your Public DNS Resolver IP address is: 54.154.201.186

Your Public DNS Resolver does not support EDNS0 Client Subnet Extension.

The Local Time and Date is: Mon Dec 17 08:23:01 2018

#####################

The output above shows you the Public IP address of the host, the DNS Resolver Public IP address for the host, DNS Resolver support for ECS and the local time when this test was performed. To locate the text file containing the output, check the current working directory.

SLOW DNS RESPONSE: Having slow responses when accessing websites ? This latency can be as a result of multiple factors such as the customers local DNS server, web server response time, loadbalancers, etc. However, some users conclude that the high response time is because of slow DNS responses which is not the case most times.

The script used to troubleshoot this is called dns_query_time.py . The script performs a DNS lookup against four authoritative nameservers that Route53 provides for that domain name, displays this output and saves it in this file dns_query_time.txt . For example, if the apex domain name is "example.com", run the script this way "python dns_query_time.py example.com" (without quotations). This script must be used with the customer's APEX DOMAIN and not any other record in the zone. The output below can help prove that Route53 nameservers are responding to DNS requests within a short time.

#######################

ns-247.awsdns-30.com takes 17 msec to resolve example.com domain

ns-837.awsdns-40.net takes 1 msec to resolve example.com domain

ns-1407.awsdns-47.org takes 10 msec to resolve example.com domain

ns-1906.awsdns-46.co.uk takes 11 msec to resolve example.com domain

#######################



WEIGHTED ROUTING POLICY TROUBLESHOOTING: Customers using Route53 complain about uneven distribution of DNS requests. The weighted routing policy does a good job in distributing DNS requests. A very important point to note is you need to consider the impact of TTL on a DNS record when using Route53 weighted routing policy. Once the customer's resolver caches the response. The TTL of the record must first expire before the local DNS resolver attempts to request for the record again.

The best way to test a weighted record is to query the authoritative nameservers directly and by-pass the local DNS resolvers which cache the response. To do this, use the script weighted.py . For example, if the weighted record is i.love.weight.route53.example.com . Run the script this way: "python weighted.py i.love.weight.example.com" (without quotations). The output looks like this:

#######################

Weighted routing policy test going on 30 times. Please wait for the final result.

Weighted routing policy test going on 30 times. Please wait for the final result.

Weighted routing policy test going on 30 times. Please wait for the final result.

Weighted routing policy test going on 30 times. Please wait for the final result.

FINAL RESULTS

This test was done using ns-1906.awsdns-46.co.uk authoritative nameserver.

The DNS record i.love.weight.example.com resolved to ['34.254.237.39', '34.255.24.0'] 6 times with 60.0% ratio.

The DNS record i.love.weight.example.com resolved to ['54.229.28.115'] 4 times with 40.0% ratio.

#######################