import json
import boto3
import socket #Used for creating TCP connections
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def lambda_handler(event, context): #AWS Lambda invokes your Lambda function via a handler object. A handler represents the name of your Lambda function and serves as the entry point that AWS Lambda uses to execute your function code
    
    cloudwatch = boto3.client('cloudwatch')
    lambdah = boto3.client('lambda')
    protocol = "TCP"
    healthcheckname = "x" #Replace with desired health check name.
    host = "x.x.x.x" #Replace with IP address or URL of private resource.
    port = "80" #Replace with desired port number for TCP.


    for i in range(30): #For loops checks VPC resource 30 times every 2 seconds with a TCP connection (Three way handshake)
        try: #Use try except block to catch errors and exceptions in the sockets library.
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).settimeout(4) #TCP connection fails after 4 seconds timeout
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            metric = 1
            print "The TCP connection was successful"
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'TCP: ' + healthcheckname,'Unit': 'None','Value': metric},])

        except socket.error as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'TCP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            print "The TCP connection was unsuccessful because the connection was refused by " + host + " or the domain name (where provided) did not resolve. Ensure the host is listening for TCP connections and DNS resolves correctly."

        except socket.timeout as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'TCP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            print "The TCP connection was unsuccessful because " + host + " did not respond within the timeout period of 4 seconds."

        except socket.giaerror as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'TCP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            logger.error("Error: " + str(e))

        except socket.herror as e:
            metric = 0
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'TCP: ' + healthcheckname,'Unit': 'None','Value': metric},])
            logger.error("Error: " + str(e))
        
        time.sleep(2)
            