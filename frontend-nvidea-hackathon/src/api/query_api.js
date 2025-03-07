const API_URL = "http://127.0.0.1:8000/process-query"

export const sendQuery = async(query, groq_key, history, chatId) => {

    try{
        console.log("query:", query, "Type of query:", typeof query);
        console.log("groq_key:", groq_key, "Type of groq_key:", typeof groq_key);
        console.log("history:", history, "Type of history:", typeof history);
        console.log("chat_id:", chatId, "Type of chat_id:", typeof chatId);


        const res = await fetch (API_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json" },
            body: JSON.stringify({
                query: query, 
                groq_key: groq_key,
                history: history,
                chat_id: chatId
            })
        });

        if (!res.ok){
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }

        const responseJSON = await res.json()

        console.log("Response: ", responseJSON)

        if (responseJSON.status == 200){
            return responseJSON.data;
        }
        
        // Error:
        return "Sorry, an error occured during the process"
    }
    catch(e){
        console.log("Error: ", e);
        return { error: e.message };
    }
}