# Azure chatbot about a scrape-able website of your choosing

### Instructions

- Start <b>Bot Framework Emulator </b>
- Activate the venv ```source venv/bin/activate```
- Create a ```.env``` file from the template
- ```azure-gpt/index-engine``` has the files you need to run before starting the bot
  - ```web-crawler.py``` is a tool to scrape a website, add the domain and the url and run it, run this first
  - ```index_engine.py``` indexes everything with the help of open ai, add the folder that has all the text files and run it
- Run the bot with ```python app.py``` 
- Grab the address and put it into the Bot Framework (```localhost:3978/api/messages```)
- You can now talk with the chatbot!
  