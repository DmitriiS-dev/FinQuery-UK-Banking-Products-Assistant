import "./chatmanager_style.css"
import ChatWindow from "../chatWindow/ChatWindow"

const ChatManager = ({ chats, setChats, activeChatId, openNewChat }) => {
  const activeChat = chats.find((chat) => chat.id === activeChatId)

  return (
    <div className="chat-manager">
      {!chats.length ? (
        <div className="empty-state">
          <h2>UK Banking Products Financial Assistant</h2>
          <p>
            Ask questions about UK banking products and get personalised recommendations based on your financial needs.
          </p>
          <button onClick={openNewChat} className="new-chat-btn">
            Start a New Query
          </button>
        </div>
      ) : activeChatId ? (
        <ChatWindow chat={activeChat} setChats={setChats} chatId={activeChatId}/>
      ) : (
        <div className="no-chat-selected">
          <p>Select a query from the sidebar or start a new one</p>
          <button onClick={openNewChat} className="new-chat-btn">
            New Query
          </button>
        </div>
      )}
    </div>
  )
}

export default ChatManager

