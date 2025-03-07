"use client"

import { useState, useEffect } from "react"

import "./App.css"
import Navbar from "./components/navbar/Navbar"
import Header from "./components/header/Header"
import ChatManager from "./components/chatManager/ChatManager"

// Routes for Create, Updating, Deleting and Fetching all of the Chats:
import { deleteChat } from "./api/delete_chat_api"
import { getChats } from "./api/get_chats_api"
import { renameChat } from "./api/rename_chat_api"
import { createChat } from "./api/create_chat_api"


function App() {
  const [chats, setChats] = useState([]) // Stores all chats
  const [activeChatId, setActiveChatId] = useState(null) // Current chat

  useEffect(()=>{
    const fetchChats = async () =>{
      const fetchedChats = await getChats(); // get the chats

      if (Array.isArray(fetchedChats)){
        setChats(fetchedChats)
      }
    }
    fetchChats();
  }, [])

  const openNewChat = async () => {
    const newChatId = Date.now().toString(); // Unique ID
    const newChatTitle = `Financial Query ${chats.length + 1}`;

    const result = await createChat(newChatId, newChatTitle); //  Use createChat

    if (result === "success") {
        const newChat = {
            id: newChatId,
            title: newChatTitle,
            messages: [],
        };

        setChats([...chats, newChat]); //  Add new chat
        setActiveChatId(newChatId);    //  Set active chat
    } else {
        console.error("Error adding a chat");
    }
  };


  const handleRenameChat = async (chatId, newName) => {
    const result = await renameChat(chatId, newName)
    if (result === "success") {
        setChats(chats.map(chat => chat.id === chatId ? { ...chat, title: newName } : chat));
    } else {
        console.error("Error renaming chat");
    }
  }

  const handleDeleteChat = async (chatId) => {
    const result = await deleteChat(chatId);

    if (result === "success") {
        const newChats = chats.filter(chat => chat.id !== chatId);
        setChats(newChats);

        // If active chat is deleted, reset active chat
        if (activeChatId === chatId) {
            setActiveChatId(newChats.length > 0 ? newChats[0].id : null);
        }
    } else {
        console.error("Error deleting chat");
    }
  }

  return (
    <div className="app-container">
      <Header />
      <div className="content-wrapper">
        <Navbar
          openNewChat={openNewChat}
          chats={chats}
          activeChatId={activeChatId}
          setActiveChatId={setActiveChatId}
          handleRenameChat={handleRenameChat}
          handleDeleteChat={handleDeleteChat}
        />
        <main className="main-content">
          <ChatManager chats={chats} setChats={setChats} activeChatId={activeChatId} openNewChat={openNewChat} />
        </main>
      </div>
    </div>
  )
}

export default App

