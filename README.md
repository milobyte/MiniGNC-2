# MiniGNC:  
**G**raphical **N**etwork **C**ustomizer for Visualizing and Storing Mininet Networks  
Made by Gatlin Cruz and Cade Tipton 
Continued Development by Noah Lowry and Miles Stanley

---

**Ways to Install This Project:**
**[Latest Release](https://github.com/GatlinCruz/Capstone/releases "MiniGNC Releases")**
- Click the Latest Release link above and follow the instructions there **(preferred)**.  
  If that does not work for you for whatever reason, the options below are available.  
  
- Manually install the dependencies by entering the commands in `install/install_reqs.txt`
- Install with Bash script (Should work on at least Ubuntu 18.04 & Ubuntu 20.04)
  1. Clone the github repository with `git clone https://github.com/GatlinCruz/Capstone.git`
  2. Navigate to the root of the Capstone directory
  3. Run the bash script to install dependencies `sudo install/install.sh`  
  **Note:** sudo is used to execute Mininet commands. Unless your password is 'Mininet'
  you must change `mysite/gui/templates/gui/buttons.py line 231` to your sudo password.  
  Yes, this is insecure for native installs and should be handled differently in the future.

**To Run The Project:**
From the root of the Capstone directory...  
1. Enter `python3 mysite/manage.py runserver`
2. Click on "http://127.0.0.1:8000/" or navigate there from your preferred browser.  
**Note:** Saving networks to the database requires starting Neo4j with `sudo neo4j start`  
(Make sure to wait a couple seconds for the database to start)

---

This project is licensed under the terms of the MIT license.
