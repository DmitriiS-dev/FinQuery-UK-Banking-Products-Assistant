from langchain_groq import ChatGroq
import json

"""
This agent processes the history of the messages and refines the User Query.
"""

def agent_1(user_query: str, history: list, api_key: str):
    # Initialise the LLM
    llm = ChatGroq(
        api_key=api_key,
        temperature=0,
        model_name="llama3-70b-8192"
    )

    # Construct the chat history string (for context)
    history_str = "\n".join([f"Message from {msg['sender']}: {msg['text']}" for msg in history])

    prompt = f"""
    You have access to the following database schema to help the next agent generate an AQL query. Here is the schema for reference:

    DATABASE SCHEMA:
        - **Collection:** `financial_nodes`
            - **_key** *(String)*: Unique identifier for the financial product.
            - **type** *(String)*: The type of financial product.
              - Possible values: `"bank"`, `"Current Account"`, `"Loan"`, `"High Yield Savings"`, `"ISA"`, `"Bond"`, `"Credit Card"`
            - **institution** *(String)*: The name of the bank or financial institution offering the product.
            - **interest_rate** *(Float)*: Interest rate associated with the financial product (if applicable).
            - **fees** *(Float)*: Fees associated with the product.
            - **rewards** *(List[String])*: A list of benefits/rewards for the product.
                ['Cashback on purchases', 'Travel discounts', 'Airport lounge access',
                'Discounted travel insurance', 'Exclusive event invites', 'Bonus loyalty points',
                'Free overdraft protection', 'Higher interest rates on savings', 
                'Free foreign ATM withdrawals', 'No fees on international transfers', 'Fuel discounts']
            - **loan_amount** *(Integer)*: The loan amount if applicable.

    - **Collection:** `financial_edges`
        - `_from`: Link to a `financial_node` (bank or financial product).
        - `_to`: Link to another `financial_node` (related financial product).
        - `relationship`: Relationship type (e.g., "offers", "related", etc.).

    USER QUERY: {user_query}

    PREVIOUS MESSAGES (CONTEXT):
    {history_str}

    Based on this information, refine the user query to generate an accurate and useful AQL query that the next agent can use to process the information.
    
    THE NEXT AGENT HAS THE EXACT SAME INFORMATION AS DO YOU SO PLEASE DO NOT INCLUDE STUFF FOR THE NEXT AGENT TO FIND OUT - YOU DON'T KNOW SOMETHING - NEXT AGENT WOULDN'T KNOW EITER!!!
    """

    try:
        # Call Groq API without await (since it's synchronous now)
        llm_response = llm.invoke(prompt)

        # Check if the response has 'content'
        if hasattr(llm_response, 'content'):
            llm_response_content = llm_response.content.strip()
            return {"status": 200, "data": llm_response_content}
        else:
            # If no content attribute, log and return the whole response
            return {"status": 500, "error": "Groq API response does not have 'content'"}

    except Exception as e:
        # More detailed error logging
        print(f"Error during agent 1 execution: {e}")
        return {"status": 500, "error": f"Error in query understanding agent: {str(e)}"}
