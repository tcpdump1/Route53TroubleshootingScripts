from helpers.generic import (
    Parser,
    Route53Base
)
from helpers.constants import (
    LIST_OF_DNS_RESOLUTION,
    RESULT_LIST,
    WEIGHTED_REGEX
)
from subprocess import check_output
from re import search
import collections
import time

RESULT_LIST.append(f'This test was carried out 10 times')

def _collection_of_resolution(domain_name):
    retrieve_auth_name_server_ip = search(WEIGHTED_REGEX, Route53Base.run_check_output(['dig', domain_name, '+trace', '+short']))
    retrieve_auth_name_server = Route53Base.run_check_output(['dig','-x', retrieve_auth_name_server_ip.group(2), '+short'])
    RESULT_LIST.append(f'This test was done using {retrieve_auth_name_server} authoritative nameserver.\n') 
    
    for i in range(10):
        a_record = Route53Base.run_check_output(['dig', domain_name, f'@{retrieve_auth_name_server_ip.group(2)}', '+short']).splitlines()
        LIST_OF_DNS_RESOLUTION.append(tuple(sorted(a_record)))
        time.sleep(2)
        
    return LIST_OF_DNS_RESOLUTION

def main():
    args = Parser.args
    dict_of_resolution=collections.Counter(_collection_of_resolution(args.domain))

    for dns_resolution, count_of_resolution in dict_of_resolution.items():
        percent = f'{round(((float(count_of_resolution)/10) * 100),2)}%'
        RESULT_LIST.append(f'The DNS record {args.domain} resolved to {list(dns_resolution)} {count_of_resolution} times with {percent} ratio.')
        
        if args.write:
            create_file = Route53.write_query_to_file('weighted.txt')
            create_file.write(f'\nThe DNS record {args.domain} resolved {list(dns_resolution)} {count_of_resolution} times with {percent} ratio.')

    return("\n".join(RESULT_LIST))

if __name__ == '__main__':
    print(main())