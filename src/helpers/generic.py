from argparse import ArgumentParser
from subprocess import (
    check_output,
    Popen,
    PIPE
)
from typing import List



class Route53Base():
    
    def __init__(self, domain_name):
        self.domain_name = domain_name


    @staticmethod
    def run_check_output(command : List) -> str: 
        '''
        Runs a CLI command

        Args: Takes a command eg. [ls -al]

        Returns: the output of the command in string format
        '''
        
        command_output = check_output(command).strip().decode("utf-8")
        return command_output


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