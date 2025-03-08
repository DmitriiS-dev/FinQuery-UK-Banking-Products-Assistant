from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from agents.agent_1 import agent_1
from agents.agent_2 import agent_2
from agents.agent_3 import agent_3

from agents.agent_2_support_agent import support_agent_for_agent_2

from agent_tools.get_history import get_relevant_history

from fastapi.middleware.cors import CORSMiddleware

from db.db_connection import db_connection  # Import the DB connection

db, arango_graph = db_connection()
chats_collection = db.collection("chats") # chats collection - ArangoDB

app = FastAPI()

# CORS Allowed Origins:
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["Content-Type"],
)

# Expected Input format for the Create Chat Request:
class CreateChatRequest(BaseModel):
    chat_id: str
    title: str

# Expected Input format for the Rename Chat Request:
class RenameChatRequest(BaseModel):
    chat_id: str
    new_title: str

# Expected Input format for the Delete Chat Request:
class DeleteChatRequest(BaseModel):
    chat_id: str

# Expected Input format for the LLM Request:
class LLMQueryRequest(BaseModel):
    query: str
    groq_key: str
    history: List[dict]
    chat_id: str


@app.post("/process-query")
def process_query(request: LLMQueryRequest):
    query = request.query
    api_key = request.groq_key
    history = request.history
    chat_id = request.chat_id
    print(f"query: {query}")
    print(f"history: {history}")
    print(f"chat_id: {chat_id}")

    try:
        # Step 1: Get relevant history based on user query and chat history
        # print("Fetching relevant history...")
        # relevant_history = get_relevant_history(query, chat_id, db)
        # if relevant_history["status"] != 200:
        #     print(f"No relevant history found for chat {chat_id}. Continuing without history.")
        #     relevant_history_data = history
        # else:
        #     relevant_history_data = relevant_history["data"]

        relevant_history_data = history

        # Step 2: User Query Understanding Agent (Agent 1)
        print("Passing to Agent 1 for user query understanding...")
        res_1 = agent_1(query, relevant_history_data, api_key)
        print(f"Step 1 Agent 1 Response: {res_1}")

        # Check if Agent 1 returned a valid response
        if res_1["status"] != 200:
            print("Error with Agent 1")
            raise HTTPException(status_code=500, detail="Error with Agent 1")

        # Extract refined data from Agent 1's response
        res_1_data = res_1["data"]

        print(f"Quick Check to see if we are pulling the right data: {res_1_data}")

        # Step 3: AQL Generation (Agent 2)
        print("Passing refined data to Agent 2 for AQL query generation...")
        res_2 = agent_2(res_1_data, api_key)
        print(f"Step 2 Agent 2 Response: {res_2}")

        if res_2["status"] != 200:
            print("Error with Agent 2. Skipping AQL generation.")
            raise Exception("Agent 2 had an error, skipping AQL generation")

        aql_query = res_2["data"]
        max_attempts = 3
        attempt = 0
        error_message = ""
        query_results = []

        # Step 4: Try executing the AQL query on the database
        while attempt < max_attempts:
            try:
                print(f"Attempt {attempt + 1} of {max_attempts}: Executing AQL query on the database...")
                query_results = list(db.aql.execute(aql_query))
                print(f"Query Results: {query_results}")
                break  # If the query executes successfully, break out of the loop
            except Exception as e:
                print(f"Error executing AQL query: {e}")
                # If query execution fails, call the support agent
                if attempt < max_attempts - 1:  # Don't call support after the last attempt
                    print(f"Calling support agent to improve query after attempt {attempt + 1}...")
                    support_res = support_agent_for_agent_2(str(e), aql_query, api_key)
                    if support_res["status"] == 200:
                        aql_query = support_res["data"]  # Update query with the improved version
                        print(f"Support Agent Query: |{aql_query}|")
                    else:
                        print(f"Support agent failed to fix the query: {support_res.get('error', 'Unknown error')}")
                else:
                    # If it's the final attempt, log and set query_results to an empty list (or fallback value)
                    print("Max attempts reached for executing the AQL query.")
                    query_results = []  # Proceed with empty results if all attempts fail
                    print("Proceeding with empty query results.")  # Optional log message
                    break  # Exit the loop, allowing the rest of the function to continue
            attempt += 1

        # If all attempts failed to execute, query_results will be empty
        if not query_results:
            print("Query execution failed after 3 attempts.")
            query_results = []  # Empty results if all attempts fail

        # Step 5: Results Summarization (Agent 3)
        print("Passing to Agent 3 for results summarization...")
        res_3 = agent_3(query, query_results, history, api_key)
        print(f"Step 3 Agent 3 Response: {res_3}")

        if res_3["status"] != 200:
            print("Error with Agent 3")
            raise HTTPException(status_code=500, detail="Error with Agent 3")

        summarised_results = res_3["data"]

        # Step 6: Append User Query and AI Response to Chat History
        try:
            print(f"Updating chat history for chat_id: {chat_id}...")

            # Fetch the chat document
            chat = chats_collection.get(chat_id)

            if chat:
                # Append the new user query and AI response to messages
                chat["messages"].append({"sender": "user", "text": query})
                chat["messages"].append(
                    {"sender": "ai", "text": summarised_results, })

                # Update the chat document in the database
                chats_collection.update(chat)
                print(f"Chat history updated successfully for chat_id: {chat_id}")
            else:
                print(f"Chat ID {chat_id} not found in the database. Unable to update history.")

        except Exception as e:
            print(f"Error updating chat history: {e}")

        return {"status": 200, "data": summarised_results}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail={"status": 500, "error": str(e)})


# API Route to Fetch Chats
@app.get("/get-chats")
def get_chats():
    try:
        chats = list(chats_collection.all())  # fetch all chats
        print(chats)
        return {"status": 200, "data": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

# Delete Chat route:
@app.delete("/delete-chat")
def delete_chat(request: DeleteChatRequest):
    try:
        chat_id = request.chat_id
        if chats_collection.has(chat_id):  # Check if chat exists
            chats_collection.delete(chat_id)
            return {"status": 200}
        else:
            raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

# Rename Chat route:
@app.post("/rename-chat")
def rename_chat(request: RenameChatRequest):
    try:
        chat_id = request.chat_id
        new_title = request.new_title
        chat = chats_collection.get(chat_id)
        if chat:
            chat["title"] = new_title
            chats_collection.update(chat)
            return {"status": 200}
        else:
            raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming chat: {str(e)}")


# Create Chat route:
@app.post("/create-chat")
def create_chat(request: CreateChatRequest):
    try:
        chat_id = request.chat_id
        title = request.title
        to_add = {
            "_key": chat_id,
            "title": title,
            "messages": []
        }
        chats_collection.insert(to_add)
        return {"status": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Adding a chat: {str(e)}")


# Run the server: uvicorn main:app --reload
