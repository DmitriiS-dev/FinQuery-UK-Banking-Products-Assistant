const API_URL = "http://127.0.0.1:8000/get-chats"

export const getChats = async () => {
    try{
        const res = await fetch (API_URL, {
            method: "GET",
            headers: {"Content-Type": "application/json" }
        });

        if (!res.ok){
            throw new Error(`HTTP Error! Status: ${res.status}`);
        }

        const jsonRes = await res.json()

        if (jsonRes.status === 200) {
            const dataFromBackend = jsonRes.data;

            // Convert the backend data into the required format
            const listToReturn = dataFromBackend.map(chat => {
                return {
                    id: chat._key, 
                    messages: chat.messages,  
                    title: chat.title,
                };
            });

            return listToReturn;
        }
        
        // Error:
        return "Sorry, an error occured during the process"
    }
    catch(e){
        console.log("Error: ", e);
        return { error: e.message };
    }
}