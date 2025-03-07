const API_URL = "http://127.0.0.1:8000/create-chat";

export const createChat = async (chatId, title) => {
    try{
        console.log("Creating a chat..")

        console.log("chat_id:", chatId, "Type of chat_id:", typeof chatId);
        console.log("title:", title, "Type of title:", typeof title);

        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                chat_id: chatId, 
                title: title 
            })
        });




        if (!res.ok) {
            throw new Error(`HTTP Error! Status: ${res.status}`);
        }

        const response = await res.json();
        console.log("Chat Created!", response);

        if (response.status === 200) {
            return "success";
        }
        
        // Error:
        return "Sorry, an error occurred during the process";
    }
    catch(e){
        console.log("Error: ", e);
        return { error: e.message };
    }
}
