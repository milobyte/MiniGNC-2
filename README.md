# MiniGNC:  
### (**G**raphical **N**etwork **C**ustomizer for Visualizing and Storing Mininet Networks)

Made by Gatlin Cruz and Cade Tipton 

Continued Development by Noah Lowry and Miles Stanley

---

## Purpose:
The purpose of this project is to eventually graphically simulate Software Defined Networks. As of now, our project is capable of simulating basic networking structure through the ability to add hosts, switches, controllers, and custom links. Bandwidth and latency can also be tested through the use of our GUI's iPerf and Ping buttons. Graphing positions of our nodes is done by using NetworkX's Kamada-Kawai function, an example of a Force Directed Graphing algorithm. All network simulation is done through the use of Mininet. The program has also been integrated with Neo4J's database management software. This allows users to save, export, and load custom networks.
 
## Installation Instructions:
**Ways to Install This Project:**
1. Clone the github repository with `git clone https://github.com/milobyte/MiniGNC-2.git`
2. Navigate to the root of the Capstone directory.
3. Install the dependencies of the project.
   - Manually install the dependencies by entering the commands in `install/install_reqs.txt`
   - Install with Bash script (Should work on at least Ubuntu 18.04 & Ubuntu 20.04): `sudo install/install.sh`
4. Install Neo4J Desktop (for database features).
   - Follow this link to install: https://neo4j.com/download/

**Note:** sudo is used to execute Mininet commands. Unless your password is 'Mininet'
you must change `mysite/gui/templates/gui/buttons.py line <UPDATE>` to your sudo password.  
Yes, this is insecure for native installs and should be handled differently in the future.

**To Run The Project:**
From the root of the Capstone directory...  
1. Enter `python3 mysite/manage.py runserver`
2. Click on "http://127.0.0.1:8000/" or navigate there from your preferred browser.  
**Note:** Saving networks to the database requires starting Neo4j. Please follow the instructions provided below on how to set up Neo4J.

**Making the program compatible with Neo4J:**
1. Open Neo4J Desktop and set up a new project.
   - Projects are used to contain the networks that a user saves through MiniGNC. Please take note of the port number and match it with the port number used to initialize the Neo4J App object, specifically in regards to the bolt_url variable. Refer to the init_database function in buttons.py for more details. 
2. Install and configure the APOC library by following the configuration instructions located at 'install/APOC CONFIG DIR.pdf'. 
   - Note: When CSV files are saved through the program, they are stored within the import folder of a Neo4J Desktop project. To access this folder, click on the three dots to the right most side of your Neo4j project tab, click on 'Open Folder', and click on 'DBMS'. This will open the directory storing information about your Neo4J project. The install directory should be here. (These directions are in regards to Neo4j Desktop version: 1.4.15)
3. Ensure the Neo4J Desktop project is running and you should be good to go!

## Notable Errors:
 - If a test in bandwidth or latency fails, specifically without the program catching the error, there is a chance that Mininet's locally stored network components will become bugged. A common error that occurs because of this is the 'RHETLINK EXISTS' error which occurs due to network components not being broken down/reset after initializing them. In this case: run the command 'sudo mn -c'. This will reset Mininet's statistics and allow you to reinitialize network componenets. 
---

This project is licensed under the terms of the MIT license.
