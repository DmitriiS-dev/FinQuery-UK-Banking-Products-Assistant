const API_URL = "http://127.0.0.1:8000/delete-chat";

export const deleteChat = async (chat_id) => {
    try{
        const res = await fetch(API_URL, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ chat_id })
        });


        if (!res.ok) {
            throw new Error(`HTTP Error! Status: ${res.status}`);
        }

        const response = await res.json();
        console.log("Chat Deleted!", response);

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
