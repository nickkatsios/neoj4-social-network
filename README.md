# neoj4-social-network
A simulation of a social network using Neo4j DBMS.
<br />
The program was developed and tested on an **Ubuntu 22.04** and a **Windows 11** machine.

### [Contents](#)
1. [**Description**](#descr)
2. [Installing & Setup](#inst)
3. [Running the functions](#run)
4. [Results](#results)
5. [Notes](#notes)

### [**Description**](#) <a name="descr"></a>

This project simulates how data could be stored and retrieved from a graph database, in a social-network context (ex. FaceBook,BeReal.). The data are retrieved from the Stanford Large Network Dataset Collection (https://snap.stanford.edu/data/#socnets) and loaded in the Neo4j DB using Python.

### [**Installing & Setup**](#) <a name="inst"></a>

Download Neo4j and Setup a DB

1. Download Neo4j Desktop (https://neo4j.com/download/)

2. Create a project

3. Inside the project, create a DBMS (Keep the name and password, will be used it later)

4. Start the DB

### [**Running the functions**](#) <a name="run"></a>

1. Clone the repository (https://github.com/nickkatsios/neoj4-social-network.git)

2. Replace the NEO4JDBNAME & NEO4JPASS Variable values down in the import_db.py script with the ones you used earlier in the creation of the Neo4j DB

3. Run the import_db.py script (it will take some time if you load all the data... approximately an hour using a modern laptop)

4. In the console/browser in the Desktop app, of the DB you created on Neo4j type any query you want


A brief overview of what each function implements.
* Function 1:  Show a small portion of your graph database
* Function 2: Count all users, count all targets, count all actions
* Function 3: Show all actions (actionID) and targets (targetID) of a specific user
* Function 4: For each user, count his/her actions
* Function 5: For each target, count how many users have done this target
* Function 6: Count the average actions per user
* Function 7: Show the userID and the targetID, if the action has positive Feature2
* Function 8: For each targetID, count the actions with label “1” 

### [**Results**](#) <a name="results"></a>
After running the functions, you can cross-check your outputs with the ones on the outputs directory (https://github.com/nickkatsios/neoj4-social-network/tree/main/outputs).


### [**Notes**](#) <a name="notes"></a>
This project was made as an assignement of the Big Data Management Systems course at DMST AUEB.
<br />
<br />
***Team members***
<br />
Nikolaos Katsios 8200071
<br />
Theodoros Skondras Mexis 8200156

