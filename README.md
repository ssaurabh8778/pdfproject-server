# PDF Project (Server)

## To run the server on local machine.

Clone the repository to local directory. In the project directory, you can run:

### `pip install -r requirements.txt`

To install all the required modules. Below mentioned modules need to be installed to run this app.
#####django
#####django-cors-headers
#####PyPDF2
#####pdfminer

### `python manage.py runserver`

Now change directory to "/pdfdetails_backend". It should be having manage.py file.
Then hit the command 'python manage.py runserver'
It will start the server.
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

## To deploy the app on pythonanywhere
Following steps need to be followed:
#####1. Login to pythonanywhere
#####2. Open Bash console
#####3. Clone this repository to pythonanywhere using 'git clone'
#####4. Create a virtual environment
#####5. Install required packages under virtual environment with 'pip install -r requirements.txt'
#####6. Update wsgi file from dashboard
#####7. Reload the app from the button provided on the dashboard. It will start the server.
See the detailed instructions in this video [deploy django app on pythonanywhere](https://www.youtube.com/watch?v=Y4c4ickks2A&t=810s)




