<img align="right" src="https://github.com/tinfins/discordParkingPassBot/blob/main/src/assets/circle-cropped.png" width=100>
  
# Parking Pass Manager

[![Invite to Discord](https://img.shields.io/static/v1?label=parkingPassMngr&message=Invite&color=7289da&style=plastic)](https://discord.com/api/oauth2/authorize?client_id=817134568405860360&permissions=0&scope=bot%20applications.commands)
  
[![Python latest](https://img.shields.io/static/v1?label=Python&message=latest&color=blue&style=plastic)](https://www.python.org/downloads/)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3c956012b35f4ad7a9811a4f2bd63ad2)](https://www.codacy.com/gh/tinfins/discordParkingPassBot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tinfins/discordParkingPassBot&amp;utm_campaign=Badge_Grade)
  
[![Commits](https://img.shields.io/github/last-commit/tinfins/discordParkingPassBot/main?style=plastic)](https://github.com/tinfins/discordParkingPassBot/commits/main)
  
[![Open Issues](https://img.shields.io/github/issues/tinfins/discordParkingPassBot?style=plastic)](https://github.com/tinfins/discordParkingPassBot/issues?q=is%3Aopen+is%3Aissue)
[![Closed Issues](https://img.shields.io/github/issues-closed/tinfins/discordParkingPassBot?style=plastic)](https://github.com/tinfins/discordParkingPassBot/issues?q=is%3Aissue+is%3Aclosed)
  
Parking pass manager is a discord bot to track parking passes using an SQLite db. Written in [Python](https://www.python.org) using the [discord.py](https://github.com/Rapptz/discord.py) library.
The bot creates a separate SQLite database for each guild to enable faster searching and eliminate read/write errors due to database locks. Each database contains a table with 4 fields:

| pass_num     | name | date | out          |
|--------------|------|------|--------------|
| int          | text | text | int          |
| Pass #       | Name | Date | Out          |
| (user input) |      |      | (user input) |

Commands are role limited.
Users have access to the following commands:
  
<img src="https://github.com/tinfins/discordParkingPassBot/blob/main/src/assets/parkingpassbot_help.jpg" width=300>

## For Developers
For Developers interested in using our application as a base to building their own app or for learning purposes, please see our [LICENSE](https://github.com/tinfins/discordParkingPassBot/blob/main/LICENSE).
  
## Development Environment Setup
### Pre-requisites
Python >= 3.7
### Required dependencies
-   aiohttp==3.7.4.post0
-   async-timeout==3.0.1
-   attrs==21.2.0
-   chardet==4.0.0
-   discord==1.0.1
-   discord-py-interactions==3.0.2
-   discord.py==1.7.3
-   idna==3.2
-   multidict==5.1.0
-   python-dotenv==0.15.0
-   pytz==2021.1
-   typing-extensions==3.10.0.2
-   yarl==1.6.3
  
(See requirements.txt for most up to date dependencies)
  
### Bot Credentials
Store your discord bot token in a file titled .env in the top-level project directory
  
### Environment Setup
-   Install Python 3.7.1 or higher

-   Clone github repository
    -   All Platforms: git clone https://github.com/tinfins/discordParkingPassBot

-   Install sqlite3
    -   sudo apt install sqlite3 libsqlite3-dev

-   Install virtualenv
    -   All platforms: pip install virtualenv

-   Create a Python virtual environment
    -   Windows: virtualenv --python C:\Path\To\Python\python.exe venv
    -   OSX/Linux: virtualenv venv

-   Activate your virtual environment
    -   Windows: .\venv\Scripts\activate
    -   OSX/Linux: source venv/bin/activate

-   Install required dependencies
    -   All Platforms: pip3 install -r requirements.txt
    -   If updating: pip install -r requirements.txt --upgrade
  
### Running
Run the bot by starting your virtual environment and use python3 app.py in the top level directory to run the bot, then invite it to your server.

Ensure the bot has permissions to send messages in your default system channel.
  
For a 24/7 online presence of your bot, creating a systemd service file (example included) or installing supervisor (sudo apt install supervisor) to manage your processes is recommended.
  
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/tinfins/discordParkingPassBot/blob/main/LICENSE) file for details.
