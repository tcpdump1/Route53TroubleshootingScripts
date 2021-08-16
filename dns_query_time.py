from helpers.generic import (
    Parser,
    Route53Base
)
from typing import List
from subprocess import check_output
from re import search

RESULT_LIST = []


def dns_query_time():

    for nameservers in Route53Base.retrieve_auth_nameservers(args.domain):       
        query_nameservers = Route53.run_dns_query(nameservers)    
        try:
            grep_query_output = check_output(('grep', 'Query'),
                                    stdin=query_nameservers.stdout,
                                    timeout=Route53.TIMEOUT
                                ).strip()   
        except:
            return('We had problems with the query.')
        
        output_query_time = search(r"\d{1,10}\smsec", grep_query_output.decode("utf-8"))
        output_nameserver = nameservers.replace("@","")
        
        if args.write:
            output = Route53.write_query_to_file("query.txt")
            output.write(f'{output_nameserver} takes {output_query_time.group()} to resolve {args.domain} domain\n')
        
        RESULT_LIST.append(f'{output_nameserver} takes {output_query_time.group()} to resolve {args.domain} domain')
 
    return("\n".join(RESULT_LIST))

    
if __name__ == "__main__":    
    args = Parser.args
    Route53 = Route53Base(args.domain)

    print(dns_query_time())
