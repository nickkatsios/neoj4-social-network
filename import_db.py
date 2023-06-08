from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

class DB_importer:

    # Init the local connection to neo4j
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_number_of_users_in_dataset(self, filepath):
        user_ids = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                user_id = int(values[1])
                user_ids.append(user_id)
        user_ids.sort()

        if self.check_range_in_sorted_list(user_ids , 0 , user_ids[-1]):
            return user_ids[-1]
        else: 
            return 0
    
    def get_number_of_targets_in_dataset(self , filepath):
        target_ids = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                target_id = int(values[2])
                target_ids.append(target_id)
        target_ids.sort()

        if self.check_range_in_sorted_list(target_ids , 0 , target_ids[-1]):
            return  target_ids[-1]
        else: 
            return 0
    
    # Check to see if every node id takes part in a relationship
    # in order to avoid creating unecessary nodes
    def check_range_in_sorted_list(self ,sorted_list, start, end):
        if not sorted_list:
            return False

        if start > sorted_list[-1] or end < sorted_list[0]:
            return False

        i = 0
        for num in range(start, end+1):
            while i < len(sorted_list) and sorted_list[i] < num:
                i += 1
            if i >= len(sorted_list) or sorted_list[i] != num:
                return False
        return True
    
    # Since we performed the check to see that all 
    # user ids take part in a relationship we can safely create 
    # the corresponding amount of user nodes
    def create_all_users(self , all_users):
        for i in range(all_users):
            print("Creating user: " + str(i))
            self.driver.execute_query(
               query_="CREATE (:USER{USERID :" + str(i) + "})",
            )
        return
    
    # Since we performed the check to see that all 
    # target ids take part in a relationship we can safely create 
    # the corresponding amount of target nodes
    def create_all_targets(self , all_targets):
        for i in range(all_targets):
            print("Creating target: " + str(i))
            self.driver.execute_query(
                query_="CREATE (:TARGET{TARGETID :" + str(i) + "})",
            )
        return
    
    # Loads all labels for each action id into a list 
    def load_labels(self):
        labels = []
        with open("./dataset/mooc_action_labels.tsv", 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                label = int(values[1])
                labels.append(label)
        return labels
    
    # Loads all features for each action id into lists
    def load_features(self):
        feature0 = []
        feature1 = []
        feature2 = []
        feature3 = []
        with open("./dataset/mooc_action_features.tsv", 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                f0 = float(values[1])
                f1 = float(values[2])
                f2 = float(values[3])
                f3 = float(values[3])
                feature0.append(f0)
                feature1.append(f1)
                feature2.append(f2)
                feature3.append(f3)
        return feature0 , feature1 , feature2 , feature3

    # Creates all actions for each action id with its attributes
    def create_all_actions(self , filepath):
        labels = self.load_labels()
        feature0 , feature1 , feature2 , feature3 = self.load_features()
        with open(filepath, 'r') as file:
            lines = file.readlines()
            # starting from 1 because 0 contains the column name string
            for i in range(1 , len(lines) - 1):
                print("Creating action " + str(i))
                line = lines[i]
                values = line.strip().split('\t')
                action_id = values[0]
                user_id = values[1]
                target_id = values[2]
                timestamp = values[3]
                label = labels[i]
                f0 = feature0[i]
                f1 = feature1[i]
                f2 = feature2[i]
                f3 = feature3[i]
                self.create_action(action_id ,user_id , target_id ,timestamp , label , f0 , f1 , f2 , f3)
    
    # creates an action in the db with its corresponding attributes
    def create_action(self, action_id, user_id, target_id, timestamp , label , f0 , f1 , f2 , f3):
        self.driver.execute_query(
                query_="""MATCH (u:USER{USERID :""" + str(user_id) + """}) , (t:TARGET{TARGETID:""" + str(target_id) + """})
                        CREATE (u) - [:TAKE_ACTION{timestamp:""" + str(timestamp) + """ , ACTIONID:""" + str(action_id) + """ 
                        , LABEL:""" + str(label)+ """, FEATURE0:""" + str(f0) + """ , FEATURE1:""" + str(f1)+ """
                        , FEATURE2:""" + str(f2) + """ , FEATURE3:""" + str(f3) + """  }] -> (t)""",
        )
        return
    
    # Runs all the processes requried to load the dataset to neo4j
    def import_into_db(self , all_users , all_targets):
        print("Import started...")
        self.create_all_users(all_users)
        print("Users created...")
        self.create_all_targets(all_targets)
        print("Targets created...")
        self.create_all_actions("./dataset/mooc_actions.tsv")
        print("Actions created...")
        return
    
    # Deletes all nodes and relationships in the db
    def delete_all_nodes_in_db(self):
        self.driver.execute_query(
            "MATCH (n) DETACH DELETE n",
        )
        return
    
    # closes the noe4j connection
    def close(self):
        self.driver.close()


if __name__ == "__main__":
    # Load password from .env
    load_dotenv()
    NEO4JPORT = "bolt://localhost:7687"
    NEO4JDBNAME = "neo4j"
    NEO4JPASS = os.getenv('NEO4JPASS')
    importer = DB_importer(NEO4JPORT, NEO4JDBNAME , NEO4JPASS)
    all_users = importer.get_number_of_users_in_dataset("./dataset/mooc_actions.tsv")
    all_targets = importer.get_number_of_targets_in_dataset("./dataset/mooc_actions.tsv")
    # delete everything before importing
    importer.delete_all_nodes_in_db()
    print("Purge completed")
    # import all into db
    importer.import_into_db(all_users , all_targets)
    print("Import completed succesfully")
    importer.close()