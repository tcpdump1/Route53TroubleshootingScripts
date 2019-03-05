# Route53HealthCheck
This is the repository for automating Route53 Health Checks with resources in a private VPC.

INTRODUCTION

Problem: Currently, it is not possible to use Route53 to monitor the health status of a private resource (a resource without a public IP address) using TCP and HTTP/HTTPS. This is because the health checkers are public and cannot reach private resources in a VPC. 

Solution: I built a Cloudformation template (file in repository called privatehealthcheck.json) consisting of Python functions that can perform TCP, HTTP and HTTPS health checks for private resources in a VPC, over VPN or a DX connection.  The term "private resource" refers to any resource in a VPC that is not accessible over the internet or a resource in a datacenter. This article explains the process involved. Using this solution, the user only needs to lauch the Cloudformation template and the rest is history :)


PYTHON LIBRARIES/MODULES USED
1) Boto3
2) Socket
3) Time
4) Requests
5) Logging

OVERVIEW

The template allows the customer to add the following: 

1) Protocol: Select the health check protocol for the private resource. Can be TCP, HTTP or HTTPS.
2) IP address or Domain Name: The IP address or the domain name of the private resource that is monitored.
3) Port: The port number of the resource.
4) Path: This is optional. For example, in "www.example.com/index.html" the path is "index.html".
5) Health Checker Subnet: This is the subnet where the Lambda function is launched. Please note, the private subnet must have internet access and it must be able to reach the resource that is monitored, without this, the health check will not work as expected.
6) VPC: Please select the VPC where the resource resides. If the resource is on-premise, select the VPC that connects via VPN or Direct Connect.onsible for creating all the resources. After the stack launches, the user will be able to see the health check on the Route53 console.



HOW DOES THIS WORK ?
CLOUDFORMATION ==> CLOUDWATCH EVENT ==> LAMBDA (PYTHON) ===> CLOUDWATCH METRIC/ALARM ===> ROUTE53 HEALTH CHECK
1) Based on the parameters selected by the user, Cloudformation creates a Lambda function that contains python code.
2) Cloudwatch Events invokes the Lambda function every minute and Lambda pushes a metric to Cloudwatch.
3) Cloudwatch metric determines whether the resource is healthy or unhealthy based on the metric pushed by Lambda.
4) Cloudwatch also receives the logs from the Lambda function. The logs provide more information about the health check status and the reasons for health check failures/success.
5) Cloudwatch creates a health check alarm for monitoring based on the metric status that is used by Route53 to determine the health status of a private resource in a VPC.
6) Route53 uses this alarm to determine if the endpoint is healthy.
7) Cloudwatch creates a namespace called "Route53PrivateHealthCheck" to store the metrics for the health check. This does not change.
8) Cloudwatch creates a Log Group and metric using the "name of the Cloudformation stack". For example, if the name of the stack is "example" and the health check protocol is "HTTP". The Cloudwatch metric name is "HTTP: example" and the log group name is "/aws/lambda/example" .


LIMITATIONS

Failover can take within 60 - 75 seconds. This is primarily because Cloudwatch alarm is triggered after considering the minimum sample count for a one minute period. To reduce the effect of this, the python function sends 30 samples within a one minute period. The higher the number of samples, the better.
At the moment, Cloudwatch supports high resolution custom metrics to enable real time monitoring of alarm (less than one minute period) but this alarm type is not supported when creating a health check in Route53. 
