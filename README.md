# MiniGNC:  
### (**G**raphical **N**etwork **C**ustomizer for Visualizing and Storing Mininet Networks)

Made by Gatlin Cruz and Cade Tipton 

Continued Development by Noah Lowry and Miles Stanley

---

## Purpose:
The purpose of this project is to eventually graphically simulate Software Defined Networks. As of now, our project is capable of simulating basic networking structure through the ability to add hosts, switches, controllers, and custom links. Bandwidth and latency can also be tested through the use of our GUI's iPerf and Ping buttons. Graphing positions of our nodes is done by using NetworkX's Kamada-Kawai function, an example of a Force Directed Graphing algorithm. All network simulation is done through the use of Mininet.
 

**Ways to Install This Project:**
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
