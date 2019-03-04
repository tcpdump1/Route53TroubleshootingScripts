# Route53HealthCheck
This is the repository for automating Route53 Health Checks with private resources

INTRODUCTION
Currently, it is not possible to use Route53 to monitor the health status of a private resource (a resource without a public IP address) using TCP and HTTP/HTTPS. This is because the health checkers are public. 

I built a Cloudformation template that can perform TCP, HTTP and HTTPS health checks for private resources in a VPC, over VPN or a DX connection.  The term "private resource" refers to any resource in a VPC that is not accessible over the internet or a resource in a datacenter. This article explains the process involved. Using this solution, the user only needs to enter the required parameters and Cloudformation does the magic !


OVERVIEW
This solution consists of the following services:

- Lambda: Using a Python function, depending on the parameters passed in the Cloudformtation template, Lambda performs the TCP/HTTP/HTTPS health check and pushes the metric and logs to Cloudwatch.

- Cloudwatch: Cloudwatch metric determines whether the resource is healthy or unhealthy based on the metric pushed by Lambda.
Cloudwatch also receives the logs from the Lambda function. The logs provide more information about the health check status and the reasons for health check failures/success. Cloudwatch creates a health check alarm used by Route53 to determine the health status of a private resource.Cloudwatch Events invokes the Lambda function every minute.

- Route53: is used to create the health check that monitors the private resource based on the Cloudwatch alarm.

- IAM: Creates a role used by Lambda to perform the periodic health checks.

- Cloudformation: All processes (Lambda, Cloudwatch, Route53, IAM) are created in the Cloudformation template. Cloudformation is responsible for creating all the resources. After the stack launches, the user will be able to see the health check on the Route53 console.

HOW DOES THIS WORK ?

    Based on the parameters selected by the customer, Cloudformation creates a Lambda function and IAM Role for the Lambda function.
    Cloudwatch Events invokes the Lambda function every minute.
    The Lambda function checks the resource using a python loop and sends the metric to Cloudwatch.
    The Lambda function sends logs to Cloudwatch to report on health check failures or successes. The customer can see the reason for the health check failures on Cloudwatch Logs.
    Cloudwatch creates an alarm to monitor the health check status of the resource for breaching data points.
    Route53 uses this alarm to determine if the endpoint is healthy.
    Cloudwatch creates a namespace called "Route53PrivateHealthCheck" to store the metrics for the health check. This does not change.
    Cloudwatch creates a Log Group and metric using the "name of the Cloudformation stack". For example, if the name of the stack is "acme" and the health check protocol is "HTTP". The Cloudwatch metric name is "HTTP: acme" and the log group name is "/aws/lambda/acme" .
