from helpers.generic import (
    args,
    Route53,
    Route53Base
)
from helpers.constants import RESULT_LIST
from time import sleep


def main() -> str:
    '''
    This function is used to check for EDNS support in public DNS resolvers
    It returns information containing:
    EDNS support of the public DNS resolver.
    Public IP address of the test host.
    Public DNS Resolver IP of the test host.
    '''
    public_ip = Route53Base.run_check_output(["curl", "-s", "checkip.amazonaws.com"])       
    dns_resolver = Route53Base.run_check_output(["dig", "resolver-identity.cloudfront.net", "+short"])
    edns_support = Route53Base.run_check_output(["dig", "edns-client-sub.net", "TXT", "+short",])

    supports = (
        f'Your Public DNS Resolver supports EDNS0 Client Subnet Extension.\n'
        f'Your Public IP address is: {public_ip}\n'
        f'Your Public DNS Resolver IP address is: {dns_resolver}\n'
    )

    if "True" in edns_support:                
        RESULT_LIST.append(supports)
            
        if args.write:
            Route53.write_query_to_file(
                'edns_tshoot.txt',
                supports
            )

    else:
        does_not_support = supports.replace("supports","does not suppport")
        RESULT_LIST.append(does_not_support)
        if args.write:
            Route53.write_query_to_file(
                'edns_tshoot.txt',
                does_not_support
            )

    return "".join(RESULT_LIST)

if __name__ == '__main__':
    print(main())