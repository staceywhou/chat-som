![image](https://github.com/staceywhou/chat-som/assets/45773084/5acf88e1-96c3-4187-bac7-de2d1e56a28b)


Our application was built utilising Flask, Python code, HTML/CSS, SQLite3, and Bootstrap. We decided to use the Flask app because of our familiarity with it from the Finance homework and its simplicity, which makes it a great choice for beginners like us. We also appreciated that it was easy to learn and that there is extensive documentation on how to use it to build websites online. Additionally, we chose to use Python, HTML/CSS, SQLite3, and Bootstrap for a similar reason - our experience in using these programming languages during CS50.

We began the implementation by creating the html pages to structure our web application. This allowed us to allocate work to each other and build out the project in unison. Next, we built out some of the core functionality of the web application utilising Flask in our .py files. 

Once this was completed, we began implementing sqlite3. We knew we wanted to move away from the CS50 SQL tools and move towards tools utilised in industry. Once we had the tool installed, we were able to upload and work with the CSV file. The CSV file allowed us to reference the class data, implement a graph on the course page, and wrangle the data so that our OpenAI ChatGPT API could reference it when accepting user questions. The chat function was built using langchain retrievalQA chain in order to maintain the context from users.
