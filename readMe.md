## Build a REST API


1. Return a list of Top Posts ordered by their number of Comments. 

Consume the API endpoints provided: 

	- comments endpoint – https://jsonplaceholder.typicode.com/comments
	-  View Single Post endpoint – https://jsonplaceholder.typicode.com/posts/{post_id}
	-  View All Posts endpoint – https://jsonplaceholder.typicode.com/posts
	

Your API response should have the following fields: 

		- post_id 
		- post_title
		- post_body 
		- total_number_of_comments


2. Search API 
Create an endpoint that allows a user to filter the comments based on all the available fields. Your solution needs to be scalable. 
	- comments endpoint – https://jsonplaceholder.typicode.com/comments

## Notes

- Once completed, send us a screenshot of your api response for Question 1 & 2. 
- Make your repo public, and send us the link for us to review




## TEST METHOD
1. run pip install requirements.txt
2. python manage.py runserver
3. For Q1, navigate to https://127.0.0.1:8000/api/posts
    - **Query Params** accepted are:
    - page : int
    - e.g.  https://127.0.0.1:8000/api/posts?page=1

4. For Q2, navigate to https://127.0.0.1:8000/api/comments
    - **Query Params** accepted are:
    - page : int
    - postId : int
    - id : int 
    - name : char
    - email : email
    - body : char
