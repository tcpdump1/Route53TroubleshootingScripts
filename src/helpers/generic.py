from argparse import ArgumentParser
from subprocess import (
    check_output,
    Popen,
    PIPE
)
from typing import List


class Route53Base():
    
    def __init__(self, domain_name=None):
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
    
    
    def write_query_to_file(self, name_of_file : str, text):
        '''
        Args: Takes a text file eg. dns_query.txt

        Step 1: Create file to store output
        Step 2: Open File
        '''
        create_file = check_output(["touch", name_of_file])
        output = open(name_of_file, 'a+').write(text)
        
        return output


class Parser():

    parser = ArgumentParser(
        description="Set Options for using DNS scripts",
        )

    parser.add_argument(
        "domain",
        type=str,
        help="Domain name eg. google.com"
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help="Option to write script to text file",
        required=False,
        default=None
    )

    argument = parser.parse_args()

args = Parser.argument
Route53 = Route53Base(args.domain)