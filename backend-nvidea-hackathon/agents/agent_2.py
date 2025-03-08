from langchain_groq import ChatGroq
import json

"""
This agent generates an AQL query from the user query and context.
"""

def agent_2(refined_query: str, api_key: str):
    try:
        # Initialise the LLM
        llm = ChatGroq(
            api_key=api_key,
            temperature=0,
            model_name="llama3-70b-8192"
        )

        # Updated Prompt with Strict Constraints
        prompt = f"""
        You are an expert in ArangoDB AQL queries. Given the following user query, generate a **valid and optimized AQL query** using **proper AQL syntax**.

        🔴 IMPORTANT RULES:
        - **DO NOT retrieve the entire database.** Queries that return all data may cause errors.
        - **Prioritize filtering conditions** based on user intent to minimize unnecessary records.
        - **Ensure that queries start with `FOR` and use `FILTER`, `LET`, and `RETURN` appropriately.**
        - ❌ **EXCLUDE all explanations, comments, and formatting hints. ONLY return the raw AQL query.**
        - **Your response must contain ONLY the AQL query with no additional text.**

        USER QUERY:
        {refined_query}

        **📊 DATABASE SCHEMA**  
        DATABASE SCHEMA:
        - **Collection:** `financial_nodes`
            - **_key** *(String)*: Unique identifier for the financial product.
            - **type** *(String)*: The type of financial product.
              - Possible values: `"bank"`, `"Current Account"`, `"Loan"`, `"High Yield Savings"`, `"ISA"`, `"Bond"`, `"Credit Card"`
            - **institution** *(String)*: The name of the bank or financial institution offering the product.
                        ["Barclays", "HSBC", "Lloyds Bank", "NatWest", "Santander", "TSB", 
                "RBS", "Halifax", "Nationwide", "Yorkshire Building Society", 
                "Coventry Building Society", "Skipton Building Society", "Leeds Building Society", 
                "Newcastle Building Society", "Principality Building Society", "Monzo", 
                "Starling Bank", "Revolut", "Atom Bank", "Tandem Bank", "Goldman Sachs (Marcus UK)", 
                "Close Brothers", "Shawbrook Bank", "Aldermore Bank", "Zopa"]
            - **interest_rate** *(Float)*: Interest rate associated with the financial product (if applicable).
            - **fees** *(Float)*: Fees associated with the product.
            - **rewards** *(List[String])*: A list of benefits/rewards for the product.
                'Cashback on purchases', 'Travel discounts', 'Airport lounge access',
                'Discounted travel insurance', 'Exclusive event invites', 'Bonus loyalty points',
                'Free overdraft protection', 'Higher interest rates on savings', 
                'Free foreign ATM withdrawals', 'No fees on international transfers', 'Fuel discounts'
            - **loan_amount** *(Integer)*: The loan amount if applicable.

        - Collection: `financial_edges`
            - `_from`: Link to a `financial_node` (bank or financial product).
            - `_to`: Link to another `financial_node` (related financial product).
            - `relationship`: Relationship type (e.g., "offers", "related", etc.).
        

        ✅ **RETURN FORMAT** (STRICT)
        - Ensure queries are efficient by applying `FILTER` conditions.
        - Always **return specific attributes** instead of the entire document.
        - **Sort results** where applicable (e.g., by `interest_rate DESC`).
        - **Your response MUST contain ONLY the AQL query with no extra words.**

        """
        part_two = """
                **✅ FIXED QUERY Example (You would only need 1 ):**
                FOR node IN financial_nodes  
                FILTER node.type == "ISA"  
                AND node.account_type IN ["Cash ISA", "Fixed-rate ISA", "Flexible ISA", "Lifetime ISA", "Stocks & Shares ISA"]  
                RETURN { 
                    institution: node.institution,  
                    product: node._key,  
                    interest_rate: node.interest_rate,  
                    fees: node.fees,  
                    rewards: node.rewards  
                }
                """

        # Use the Groq client to process the query
        llm_response = llm.invoke(prompt+part_two)

        # Log the full response for debugging
        print(f"Full response from Groq: {llm_response}")

        # Ensure only the query is extracted
        if hasattr(llm_response, 'content'):
            llm_response_content = llm_response.content.strip()
            print(f"Generated AQL Query: {llm_response_content}")
            return {"status": 200, "data": llm_response_content}
        else:
            # Log and return error if 'content' is not found in the response
            error_message = "Groq API response does not have 'content'"
            print(f"Error: {error_message}")
            return {"status": 500, "error": error_message}

    except ConnectionError as ce:
        # Handle network or connection-related issues
        error_message = f"Network/Connection Error: {str(ce)}"
        print(f"Error: {error_message}")
        return {"status": 500, "error": error_message}

    except TimeoutError as te:
        # Handle timeout errors
        error_message = f"Timeout Error: {str(te)}"
        print(f"Error: {error_message}")
        return {"status": 500, "error": error_message}

    except Exception as e:
        # Catch any other errors
        error_message = f"Error in AQL Query generation agent: {str(e)}"
        print(f"Error: {error_message}")
        return {"status": 500, "error": error_message}
