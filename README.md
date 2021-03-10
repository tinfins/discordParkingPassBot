<img align="right" src="https://github.com/tinfins/discordParkingPassBot/blob/main/src/assets/circle-cropped.png" width=100>
  
# Parking Pass Manager

[![Invite to Discord](https://img.shields.io/static/v1?label=parkingPassMngr&message=Invite&color=7289da)](https://discord.com/api/oauth2/authorize?client_id=817134568405860360&permissions=85056&scope=bot)
  
[![Python latest](https://img.shields.io/static/v1?label=Python&message=latest&color=brightgreen)](https://www.python.org/downloads/)
  
Parking pass manager is a discord bot to track parking passes using an SQLite db. Written in [Python](https://www.python.org) using the [discord.py](https://github.com/Rapptz/discord.py) library.
The bot creates a separate SQLite database for each guild to enable faster searching and eliminate read/write errors due to database locks. Each database contains a table with 4 fields:

| pass_num     | name | date | out          |
|--------------|------|------|--------------|
| int          | text | text | int          |
| Pass #       | Name | Date | Out          |
| (user input) |      |      | (user input) |

  
Commands are role limited.
All users have access to the following commands:
```
A parking pass manager. Prefix your commands with /pass or !pass

Parking Pass Manager:
  in   /pass in [pass #] - Check in parking pass
  out  /pass out [pass #] - Check out parking pass
​No Category:
  help Shows this message

Type /pass help command for more info on a command.
You can also type /pass help category for more info on a category.
```  
  
The roles of supervisors and admin have access to the following commands:

```
A parking pass manager. Prefix your commands with /pass or !pass

Parking Pass Manager:
  add    /pass add [pass #] - Add pass to database
  del    /pass del [pass #] - Delete pass to database
  in     /pass in [pass #] - Check in parking pass
  out    /pass out [pass #] - Check out parking pass
  report /pass report - Show status of passes
  status /pass status [pass #] - Check status of pass
​No Category:
  help   Shows this message

Type !pass help command for more info on a command.
You can also type !pass help category for more info on a category.
```  
  
## For Developers:
For Developers interested in using our application as a base to building their own app or for learning purposes, please see our [LICENSE](https://github.com/tinfins/discordParkingPassBot/blob/main/LICENSE).
  
## Development Environment Setup
### Pre-requisites
Python 3.7
### Required dependencies
- pytz==2021.1
- python-dotenv==0.15.0
- discord==1.0.1
  
(See requirements.txt file for most up to date dependencies)
  
### Bot Credentials
Store your discord bot token in a file titled .env in the top-level project directory\
ex. BOT_TOKEN=[bot token]
  
### Environment Setup
- Install Python 3.7.1 or higher
- Clone github repository
  - All Platforms: git clone https://github.com/tinfins/discordParkingPassBot
- Install sqlite3
  - sudo apt install sqlite3 libsqlite3-dev
- Install virtualenv
  - All platforms: pip install virtualenv
- Create a Python virtual environment
  - Windows: virtualenv --python C:\Path\To\Python\python.exe venv
  - OSX/Linux: virtualenv venv
- Activate your virtual environment
  - Windows: .\venv\Scripts\activate
  - OSX/Linux: source venv/bin/activate
- Install required dependencies
  - All Platforms: pip3 install -r requirements.txt
  - If updating: pip install -r requirements.txt --upgrade
  
### Running
After inviting the bot to your discord server, run the bot by starting your virtual environment, then typing python3 app.py from the top level directory
  
For a 24/7 online presence of your bot, installing supervisor (sudo apt install supervisor) is recommended.
  
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/tinfins/discordParkingPassBot/blob/main/LICENSE) file for details.
