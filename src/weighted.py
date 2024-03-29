from typing import List
from collections import Counter
from re import search
from subprocess import check_output
from time import sleep
from helpers.generic import (
    args,
    Route53,
    Route53Base
)
from helpers.constants import (
    LIST_OF_DNS_RESOLUTION,
    RESULT_LIST,
    WEIGHTED_REGEX
)


def _list_of_weighted_records(domain_name : str, write : str, Route53 : Route53) -> List:
    '''
    This function returns a list of tuples containing A records for the weighted record.
    eg: [('1.1.1.1',), ('1.1.1.1',), ('2.2.2.2',), ('1.1.1.1',), ('2.2.2.2',),
         ('2.2.2.2',), ('2.2.2.2',), ('1.1.1.1',), ('2.2.2.2',), ('2.2.2.2',)]
    '''
    retrieve_auth_name_server_ip = search(WEIGHTED_REGEX, Route53Base.run_check_output(['dig', domain_name, '+trace', '+short']))
    retrieve_auth_name_server = Route53Base.run_check_output(['dig','-x', retrieve_auth_name_server_ip.group(2), '+short'])
    RESULT_LIST.append(f'This test was carried out ten times.\nThis test was done using {retrieve_auth_name_server} authoritative nameserver.\n')
    
    if write:
        Route53.write_query_to_file(
            'weighted.txt',
            f'This test was carried out ten times.\nThis test was done using {retrieve_auth_name_server} authoritative nameserver.\n'
        )
        
    for count_of_resolution in range(10):
        a_record = Route53Base.run_check_output(['dig', domain_name, f'@{retrieve_auth_name_server_ip.group(2)}', '+short']).splitlines()
        LIST_OF_DNS_RESOLUTION.append(tuple(sorted(a_record)))
        sleep(2)
        
    return LIST_OF_DNS_RESOLUTION


def _calculate_dns_resolution_percentage(dict_of_resolution : dict, domain_name : str, write : str, Route53 : Route53) -> str:
    '''
    This function returns a string containing the percentage ratio for DNS resolutions.
    Example:
    The DNS record weighted.ogbonosoup.com resolved to ['1.1.1.1'] 8 times with 80.0% ratio.
    The DNS record weighted.ogbonosoup.com resolved to ['2.2.2.2'] 2 times with 20.0% ratio.
    '''
    for dns_resolution, count_of_resolution in dict_of_resolution.items():
        percent = f'{round(((float(count_of_resolution)/10) * 100),2)}%'
        RESULT_LIST.append(f'The DNS record {domain_name} resolved to {list(dns_resolution)} {count_of_resolution} times with {percent} ratio.')
        
        if write:
            Route53.write_query_to_file(
                'weighted.txt',
                f'\nThe DNS record {domain_name} resolved {list(dns_resolution)} {count_of_resolution} times with {percent} ratio.'
            )

    if write:
        Route53.write_query_to_file(
            'weighted.txt',
            f'\n'
    )
    return("\n".join(RESULT_LIST))


def main():
    
    dict_of_resolution = Counter(
        _list_of_weighted_records(
            args.domain,
            args.write,
            Route53
        )
    )

    return _calculate_dns_resolution_percentage(
        dict_of_resolution,
        args.domain,
        args.write,
        Route53
    )


if __name__ == '__main__':
    print(main())
