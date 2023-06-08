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
            self.driver.execute_query(
               query_="CREATE (:USER{USERID :" + str(i) + "})",
            )
        return
    
    # Since we performed the check to see that all 
    # target ids take part in a relationship we can safely create 
    # the corresponding amount of target nodes
    def create_all_targets(self , all_targets):
        for i in range(all_targets):
            self.driver.execute_query(
                query_="CREATE (:TARGET{TARGETID :" + str(i) + "})",
            )
        return
    
    def create_action():
        return
    
    def import_into_db(self , all_users , all_targets):
        self.create_all_users(all_users)
        self.create_all_targets(all_targets)
        return
    
    # Deletes all nodes and relationships in the db
    def delete_all_nodes_in_db(self):
        self.driver.execute_query(
            "MATCH (n) DETACH DELETE n",
        )
        return
    
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
    importer.import_into_db(all_users , all_targets)
    # importer.delete_all_nodes_in_db()
    importer.close()