from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

class DB_importer:

    # Init the local connection to neo4j
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Test methods to check connection to the db 
    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    # Load password from .env
    load_dotenv()
    NEO4JDBNAME = "neo4j"
    NEO4JPASS = os.getenv('NEO4JPASS')
    greeter = DB_importer("bolt://localhost:7687", NEO4JDBNAME , NEO4JPASS)
    greeter.print_greeting("hello, world")
    greeter.close()