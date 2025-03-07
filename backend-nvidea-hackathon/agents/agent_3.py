from langchain_groq import ChatGroq
import json

"""
This agent summarizes the AQL query results, User query, Chat History and provides a user-friendly response.
"""

def agent_3(user_query: str, data: list, history: list, api_key: str):
    # Initialize the LLM
    llm = ChatGroq(
        api_key=api_key,
        temperature=0,
        model_name="llama3-70b-8192"
    )

    # Prepare the prompt
    prompt = f"""
    You are a financial assistant designed to summarize user queries and data concisely and in a user-friendly manner. Based on the provided data and the user's question, please give a summary that answers the user's query clearly and provides relevant information.

    ### Instructions:
    - Assume that the currency is ALWAYS £ (GBP)
    - Review the provided **data** and **user query**.
    - If the data includes a comparison of financial products, list the best options first.
    - If no relevant data is found, suggest alternative financial options that might suit the user's needs.
    - Make sure to highlight important details such as **interest rates**, **fees**, and any **special offers** (if present).
    - If the data does not meet the user's expectations or no relevant results are found, provide a polite response like: "I couldn't find any relevant results. Would you like to try a different query?"
    - Keep the response **concise**. Only include relevant information.
    - Avoid adding extra explanations. Just the facts that answer the user's query are enough.

    ### Data:
    {json.dumps(data, indent=4)}

    ### User Query:
    {json.dumps(user_query, indent=4)}
    
    ### Conversation History:
    {json.dumps(history, indent=4)}

    Make sure your response helps the user move forward in their decision-making, focusing on clarity and relevance.
    """

    try:
        # Call the Groq API to get a refined summary
        llm_response = llm.invoke(prompt).content.strip()

        return {"status": 200, "data": llm_response}

    except Exception as e:
        return {"status": 500, "error": f"Error in Summarization agent: {str(e)}"}
