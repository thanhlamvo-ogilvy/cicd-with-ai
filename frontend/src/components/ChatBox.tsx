import { useState } from "react";
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
    error: chatError,
    sendMessage,
    setMessages,
    setConversationId,
  } = useChat();
  const { conversations, refresh, remove, error: conversationError } = useConversations();
  const [uiError, setUiError] = useState<Error | null>(null);

  const handleSend = async (content: string) => {
    try {
      setUiError(null);
      await sendMessage(content, PROVIDER, MODEL);
      await refresh();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setUiError(error);
      console.error("Failed to send message:", error);
    }
  };

  const handleSelectConversation = async (id: string) => {
    try {
      setUiError(null);
      const conv = await fetchConversation(id);
      setConversationId(id);
      setMessages(conv.messages);
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setUiError(error);
      console.error("Failed to select conversation:", error);
    }
  };

  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
    setUiError(null);
  };

  const handleDelete = async (id: string) => {
    try {
      setUiError(null);
      await remove(id);
      if (conversationId === id) {
        handleNewChat();
      }
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setUiError(error);
      console.error("Failed to delete conversation:", error);
    }
  };

  const displayError = chatError || conversationError || uiError;

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
        {displayError && (
          <div
            style={{
              padding: "12px 16px",
              backgroundColor: "#fee",
              color: "#c33",
              borderBottom: "1px solid #fcc",
              fontSize: "14px",
            }}
          >
            Error: {displayError.message}
          </div>
        )}
        <MessageList messages={messages} />
        <ChatInput onSend={handleSend} disabled={isStreaming} />
      </div>
    </div>
  );
}
