from arango import ArangoClient
from langchain_community.graphs import ArangoGraph

def db_connection():
    # ✅ Connect to ArangoDB
    client = ArangoClient(hosts="http://localhost:8529")
    # Password and Username to connect to local arrangoDB:
    db = client.db("_system", username="root", password="openSesame")

    # Ensure the "chats" collection exists
    if not db.has_collection("chats"):
        db.create_collection("chats")

    # ✅ Connect LangChain to ArangoDB
    arango_graph = ArangoGraph(db)

    return db, arango_graph


