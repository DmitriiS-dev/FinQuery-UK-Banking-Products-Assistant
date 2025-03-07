"use client"

import { useState } from "react"
import "./navbar_style.css"

const Navbar = ({ openNewChat, chats, activeChatId, setActiveChatId, handleRenameChat, handleDeleteChat }) => {
  const [menuOpen, setMenuOpen] = useState(null)
  const [editingChatId, setEditingChatId] = useState(null)
  const [newChatName, setNewChatName] = useState("")

  const toggleMenu = (chatId, e) => {
    e.stopPropagation()
    setMenuOpen(menuOpen === chatId ? null : chatId)
  }

  const handleRenameClick = (chatId, currentName, e) => {
    e.stopPropagation()
    setEditingChatId(chatId)
    setNewChatName(currentName)
    setMenuOpen(null)
  }

  const handleDeleteClick = (chatId, e) => {
    e.stopPropagation()
    handleDeleteChat(chatId)
    setMenuOpen(null)
  }

  const handleRenameSubmit = (chatId, e) => {
    e.preventDefault()
    if (newChatName.trim()) {
      handleRenameChat(chatId, newChatName.trim())
      setEditingChatId(null)
      setNewChatName("")
    }
  }

  const handleClickOutside = () => {
    setMenuOpen(null)
  }

  return (
    <div className="navbar">
      <div className="navbar-section">
        <button className="new-chat-btn" onClick={openNewChat}>
          New Query
        </button>
        <ul className="chat-list">
          {chats.map((chat) => (
            <li
              key={chat.id}
              className={chat.id === activeChatId ? "active" : ""}
              onClick={() => {
                setActiveChatId(chat.id)
                setMenuOpen(null)
              }}
            >
              {editingChatId === chat.id ? (
                <form onSubmit={(e) => handleRenameSubmit(chat.id, e)} className="rename-form">
                  <input
                    type="text"
                    value={newChatName}
                    onChange={(e) => setNewChatName(e.target.value)}
                    onClick={(e) => e.stopPropagation()}
                    autoFocus
                    className="rename-input"
                  />
                  <button type="submit" className="rename-submit">
                    Save
                  </button>
                </form>
              ) : (
                <>
                  <span className="chat-title">{chat.title}</span>
                  <button className="chat-menu-btn" onClick={(e) => toggleMenu(chat.id, e)} aria-label="Chat options">
                    <span className="dots"></span>
                  </button>
                  {menuOpen === chat.id && (
                    <>
                      <div className="menu-backdrop" onClick={handleClickOutside}></div>
                      <div className="chat-menu">
                        <button className="menu-item" onClick={(e) => handleRenameClick(chat.id, chat.title, e)}>
                          Rename
                        </button>
                        <button className="menu-item delete" onClick={(e) => handleDeleteClick(chat.id, e)}>
                          Delete
                        </button>
                      </div>
                    </>
                  )}
                </>
              )}
            </li>
          ))}
          {chats.length === 0 && <li className="empty-chat-list">No queries yet</li>}
        </ul>
      </div>
    </div>
  )
}

export default Navbar

