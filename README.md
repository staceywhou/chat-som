To set up and run chat-som, run the following commands:

  cd chat_som

This will take you to the correct directory where the flask app sits.

  pip install -r requirements.txt

This will ensure that you have all the relevant requirements installed. We have run into a bug where docarray may be incorrectly installed. In this case, try:

  pip3  install -U docarray
  pip3  install pydantic==1.10.9

Then we can do

  flask run

And this should set up the application locally.

Note that in key.py, there is an API key string. When multiple IP addresses try to access the API key, it may become deactivated. You may need to request a new key from https://platform.openai.com/api-keys.
To use the project, first register an account under the /register page:
Make sure that the passwords must include 2 letters, 2 numbers, and 2 symbols.

Once registered, log in at /login:


Once logged in, you can ask it CHAT S.O.M questions about the SOM curriculum:


You can also browse the course under /course_list:



