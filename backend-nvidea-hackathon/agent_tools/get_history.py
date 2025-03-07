from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

"""
    Get relevant information from chat history based on the user query.
    """

def get_relevant_history(user_query: str, chat_id: str, db, threshold=0.7, top_k=5):

    try:
        # Initialise the SentenceTransformer model
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Get the chat document from the database
        chat_doc = db.collection("chats").get(int(chat_id))
        if not chat_doc:
            return {"status": 404, "error": "Chat not found."}

        # Extract messages
        messages = chat_doc.get("messages", [])
        if not messages:
            return {"status": 200, "data": []}

        # Extract message text and keep track of original messages
        messages_text = []
        original_messages = []

        for message in messages:
            if 'text' in message and message['text'].strip():
                messages_text.append(message['text'])
                original_messages.append(message)

        if not messages_text:
            return {"status": 200, "data": []}

        # Encode the query and messages using the model
        query_embedding = model.encode(user_query)
        message_embeddings = model.encode(messages_text)

        # Calculate similarity
        similarity_scores = cosine_similarity([query_embedding], message_embeddings)[0]

        # Create pairs of (index, score) and sort by score
        scored_indices = [(i, score) for i, score in enumerate(similarity_scores)]

        # Sort the list by similarity score in desc order
        scored_indices.sort(key=lambda x: x[1], reverse=True)

         # Select relevant messages based on the threshold and top_k limit
        relevant_messages = []
        for idx, score in scored_indices[:top_k]:
            if score >= threshold:
                relevant_messages.append({
                    "message": original_messages[idx],
                    "text": messages_text[idx],
                    "similarity_score": float(score)  # Ensure the score is a float for JSON compatibility
                })

        # Return the relevant messages with metadata
        return {
            "status": 200,
            "data": relevant_messages,
            "metadata": {
                "total_messages": len(messages),
                "processed_messages": len(messages_text),
                "relevant_messages": len(relevant_messages),
                "model": "paraphrase-MiniLM-L6-v2"
            }
        }
    # Return error message with traceback in case of an exception
    except Exception as e:
        import traceback
        return {"status": 500, "error": str(e), "traceback": traceback.format_exc()}