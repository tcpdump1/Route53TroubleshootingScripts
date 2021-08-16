from argparse import ArgumentParser
from subprocess import (
    check_output,
    Popen,
    PIPE
)
from typing import List



class Route53Base():

    TIMEOUT=2

    def __init__(self, domain_name):
        self.domain_name = domain_name


    @staticmethod
    def retrieve_auth_nameservers(domain_name) -> List: 
        '''
        Retrieves the authoritative nameservers for a
        domain name

        Args: Takes a domain name eg. ogbonosoup.com

        Returns: A List of authoritative nameservers,
        eg. [ns-1.awsdns-30.com, ns-2.awsdns-30.com,
        ns-3.awsdns-30.com, ns-4.awsdns-30.com]
        ]
        '''
        auth_nameservers = check_output(["dig", domain_name, "NS", "+short"]).splitlines()
        auth_nameservers = [f'@{i.decode("utf-8")}' for i in auth_nameservers]
    
        return auth_nameservers
    

    def run_dns_query(self, nameserver : str):
        query_nameservers = Popen(
                                ('dig', self.domain_name, nameserver),
                                stdout=PIPE
                            )
        
        return query_nameservers
    
    def write_query_to_file(self, name_of_file : str):
        '''
        Args: Takes a text file eg. dns_query.txt

        Step 1: Create file to store output
        Step 2: Open File
        '''
        create_file = check_output(["touch", name_of_file])
        output = open(name_of_file, 'a+')
        
        return output


class Parser():

    parser = ArgumentParser(
        description="Set Options for DNS queries",
        )

    parser.add_argument(
        "domain",
        type=str,
        help="Write to test file"
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help="Write to test file",
        required=False,
        default=None
    )

    args = parser.parse_args()