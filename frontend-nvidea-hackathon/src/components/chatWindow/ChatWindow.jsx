"use client";

import { useState, useRef, useEffect, useContext } from "react";
import { sendQuery } from "../../api/query_api";

import { ApiKeyContext} from "../../contexts/ApiKeyContext"

import "./chatwindow_style.css";

const ChatWindow = ({ chat, setChats, chatId }) => {
  const [message, setMessage] = useState(""); // current msg
  const messagesEndRef = useRef(null);

  const { apiKey } = useContext(ApiKeyContext) 

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat.messages]);

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    // Check if API key is available:
    if (!apiKey || apiKey === "") {
      alert("No API Key saved!");
      return;
    }

    const newMessage = {
      sender: "user",
      text: message,
      timestamp: new Date().toISOString(),
    };

    // Update chat with user message
    setChats((prevChats) =>
      prevChats.map((c) =>
        c.id === chat.id ? { ...c, messages: [...c.messages, newMessage] } : c
      )
    );

    setMessage("");

    // Show "AI is typing..."
    const typingIndicator = {
      sender: "ai",
      text: "...",
      timestamp: new Date().toISOString(),
    };

    setChats((prevChats) =>
      prevChats.map((c) =>
        c.id === chat.id ? { ...c, messages: [...c.messages, typingIndicator] } : c
      )
    );

    // Send message to Backend
    try {
      const aiResponseText = await sendQuery(
        message,
        apiKey,
        chat.messages, // Full chat history
        chatId
      );

      // API Response
      console.log(`Data we got back! ${aiResponseText}`)

      // Remove typing indicator before showing response
      setChats((prevChats) =>
        prevChats.map((c) =>
          c.id === chat.id ? { ...c, messages: c.messages.slice(0, -1) } : c
        )
      );

      // Add AI response letter by letter (typing effect)
      let currentText = "";
      const aiResponse = { sender: "ai", text: "", timestamp: new Date().toISOString() };

      setChats((prevChats) =>
        prevChats.map((c) =>
          c.id === chat.id ? { ...c, messages: [...c.messages, aiResponse] } : c
        )
      );

      for (let i = 0; i < aiResponseText.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 5)); // Typing delay
        currentText += aiResponseText[i];

        setChats((prevChats) =>
          prevChats.map((c) =>
            c.id === chat.id
              ? {
                  ...c,
                  messages: c.messages.map((msg, index) =>
                    index === c.messages.length - 1 ? { ...msg, text: currentText } : msg
                  ),
                }
              : c
          )
        );
      }
    } catch (error) {
      console.error("Error getting AI response:", error);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>{chat.title}</h2>
      </div>

      <div className="messages-container">
        {chat.messages.length === 0 ? (
          <div className="empty-chat">
            <p>This is the beginning of your conversation.</p>
            <p>Type a message below to get started.</p>
          </div>
        ) : (
          <div className="messages">
            {chat.messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <div className="message-content">{msg.text}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatWindow;
