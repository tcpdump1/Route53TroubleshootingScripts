import json
import boto3
import time
from botocore.vendored import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    lambdah = boto3.client('lambda')
    protocol = "HTTP"
    healthcheckname = "x" #Replace with desired health check name.
    domainname = "x.x.x.x" #Replace with IP address or URL of private resource.
    url = "http://x.x.x.x:80/" #Replace with IP address or URL of private resource plus the port number and protocol
    
    
    x = 1 #For loops checks VPC resource 30 times every 2 seconds with a HTTP GET request
    while x <=30:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code >= 200 and r.status_code <= 399:
                metric = 1
                print "The HTTP GET Request was successful."
                print "The HTTP response code is: " + str(r.status_code)
                response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            else:
                metric = 0
                print "The HTTP GET Request was not successful because it received a HTTP Client Side or Server Side Error Code."
                print "The HTTP response code is: " + str(r.status_code)
                response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
        except requests.exceptions.HTTPError as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            logger.error("Error: " + str(e))
        except requests.exceptions.ConnectionError as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            if str(e) == "('Connection aborted.', gaierror(-2, 'Name or service not known'))":
                print "The domain name "" + domainname + "" does not resolve to an IP address. Kindly ensure the domain name resolves in the VPC."
            elif str(e) == "('Connection aborted.', error(111, 'Connection refused'))":
                print "The connection was refused by the endpoint. Please check if the endpoint is listening for HTTP connections on the correct port."
            else:
                logger.error("Error: " + str(e))
        except requests.exceptions.Timeout as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            print "The HTTP/HTTPS connection timed out because we did not receive a HTTP response within the 2 seconds timeout period."
        except requests.exceptions.TooManyRedirects as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            logger.error("Error: " + str(e))
        x += 1
        time.sleep(2)