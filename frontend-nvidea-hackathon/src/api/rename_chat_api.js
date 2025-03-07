const API_URL = "http://127.0.0.1:8000/rename-chat";

export const renameChat = async (chat_id, updated_title) => {
    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ chat_id, new_title: updated_title })
        });

        if (!res.ok) {
            throw new Error(`HTTP Error! Status: ${res.status}`);
        }

        const response = await res.json();
        console.log("Chat Renamed Successfully!", response);

        if (response.status === 200) {
            return "success";
        }

        return "Sorry, an error occurred during the process";
    } catch (e) {
        console.log("Error:", e);
        return { error: e.message };
    }
};
