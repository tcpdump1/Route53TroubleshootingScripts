
import json
import boto3
import socket #model used for TCP connections
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def lambda_handler(event, context): #AWS Lambda invokes your Lambda function via a handler object. A handler represents the name of your Lambda function and serves as the entry point that AWS Lambda uses to execute your function code
    
    cloudwatch = boto3.client('cloudwatch')
    lambdah = boto3.client('lambda')
    protocol = "TCP"
    healthcheckname = "tcpdump"
    host = "34.240.231.139"
    port = 80


    for i in range(30):
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).settimeout(4)
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
            