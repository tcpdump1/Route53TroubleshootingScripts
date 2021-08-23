from helpers.generic import (
    Parser,
    Route53Base
)
from helpers.constants import(
    DNS_QUERY_TIME_REGEX,
    RESULT_LIST,
    TIMEOUT
)
from typing import List
from subprocess import check_output
from re import search


def _grep_output(query_nameservers) -> str:
    output=(check_output(('grep', 'Query'), stdin=query_nameservers.stdout, timeout=TIMEOUT).strip())
    return output


def main():
    args = Parser.args
    Route53 = Route53Base(args.domain)
    auth_nameservers = [f'@{i}' for i in Route53Base.run_check_output(["dig", args.domain, "NS", "+short"]).splitlines()]
    
    for nameservers in auth_nameservers:
        try:
            grep_query_output = _grep_output(Route53.run_dns_query(nameservers))
        except:
            return('We had problems with the query.')

        output_query_time = search(DNS_QUERY_TIME_REGEX, grep_query_output.decode("utf-8"))
        output_nameserver = nameservers.replace("@","")

        if args.write:
            output = Route53.write_query_to_file("query.txt")
            output.write(f'{output_nameserver} takes {output_query_time.group()} to resolve {args.domain} domain\n')

        RESULT_LIST.append(f'{output_nameserver} takes {output_query_time.group()} to resolve {args.domain} domain')

    return("\n".join(RESULT_LIST))

if __name__ == "__main__":
    print(main())
