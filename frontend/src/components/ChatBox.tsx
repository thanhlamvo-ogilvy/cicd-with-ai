import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { Sidebar } from "./Sidebar";
import { useChat } from "../hooks/useChat";
import { useConversations } from "../hooks/useConversations";
import { fetchConversation } from "../services/api";

const PROVIDER = "openai";
const MODEL = "google/gemma-3-4b";

export function ChatBox() {
  const {
    messages,
    isStreaming,
    conversationId,
    sendMessage,
    setMessages,
    setConversationId,
  } = useChat();
  const { conversations, refresh, remove } = useConversations();

  const handleSend = async (content: string) => {
    await sendMessage(content, PROVIDER, MODEL);
    refresh();
  };

  const handleSelectConversation = async (id: string) => {
    const conv = await fetchConversation(id);
    setConversationId(id);
    setMessages(conv.messages);
  };

  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
  };

  const handleDelete = async (id: string) => {
    await remove(id);
    if (conversationId === id) {
      handleNewChat();
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "system-ui, sans-serif" }}>
      <Sidebar
        conversations={conversations}
        activeId={conversationId}
        onSelect={handleSelectConversation}
        onNew={handleNewChat}
        onDelete={handleDelete}
      />
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div
          style={{
            padding: "12px 16px",
            borderBottom: "1px solid #e0e0e0",
            fontWeight: "bold",
            fontSize: "16px",
          }}
        >
          AI Chatbox
        </div>
        <MessageList messages={messages} />
        <ChatInput onSend={handleSend} disabled={isStreaming} />
      </div>
    </div>
  );
}
