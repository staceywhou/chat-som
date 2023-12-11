## Welcome to Chat-SOM!

The goal of the project is for people interested in Yale School of Management Curriculum to learn more about the class offerings using a chat bot powered by OpenAI.

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
![image](https://github.com/staceywhou/chat-som/assets/45773084/4ea7c9fc-8ba1-4dae-a18d-fffcd9cd4092)

Make sure that the passwords must include 2 letters, 2 numbers, and 2 symbols.

Once registered, log in at /login:
![image](https://github.com/staceywhou/chat-som/assets/45773084/261b2134-6d48-43a7-8ec5-1b3701ccd74a)

Once logged in, you can ask it CHAT S.O.M questions about the SOM curriculum:
![image](https://github.com/staceywhou/chat-som/assets/45773084/28b4b759-d5a7-40b4-a844-16546cf56dea)


You can also browse the course under /course_list:
![image](https://github.com/staceywhou/chat-som/assets/45773084/5dab6e6d-7690-4fb7-b32c-b46cba771e1b)




