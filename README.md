# rest-service-example
Example of a REST service in python

# Overview
This project is aimed to demonstrate:
1. How to create multi-container application in python consisting of:
    1.1. Load balancer
    1.2. WSGI HTTP server
    1.3. python web application using popular web framework
    1.4. database

2. How to implement simple REST API for performing CRUD operations
3. How to implement basic UI
	
# Scenarios
## Application skeleton deployment
**Story**
As a deployment engineer I want to have simple and fast way of deploying this application so that 
I can easily deploy application in any environment.

## Database schema change
**Story**
As a database developer I want to have means of integrating database changes in application 
deployment process so that database changes are applied during application deployment.

## Customer management
### Create customer
**Story**
As an API consumer I want to be able to create new customer using API
so that customer data is persisted and could be read and modified later.

### Update customer
**Story**
As an API consumer I want to be able to update customer data using API
so that customer data reflects real-world data. 

### Delete customer
**Story**
As an API consumer I want to be able to delete customer data using API
so that system contains only actual data.

### Read customer
**Story**
As an API consumer I want to be able to read all customers and 
particular customer using customer key via API
so that customer date could be displayed in UI for end-user usage,

