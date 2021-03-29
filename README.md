This project is made for monitoring COVID cases in the United Kingdom. 
It allows the user to store the covid data related to UK from public API https://covid-api.mmediagroup.fr/v1/cases?country=United Kingdom
We can perform CRUD operations over the created database through RESTful webservices using flask i.e, [GET, PUT, POST, DELETE]

Main functions included in this project are-

1. [/cases] insert the newly updated covid data related to UK in table covid.

2. [/casedetails] display the no. of rows and all the data present inside the table.

3. [/casedetails/<updated>] display ony the row whose updated date is <updated>.

4. [/casedetails/update/<country>/<confirmed>/<recovered>/<deaths>/<updated>] update the row with the provided new parameters whose updated date is <updated>.

5. [/casedetails/delete/<updated>] delete the respective row whose updated date is <updated>

The API is served on https using self signed digital certificate.

The whole project is containerised though Dockerfile. It also includes requirements.txt to install each Library.
