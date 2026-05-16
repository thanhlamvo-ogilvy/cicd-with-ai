import type { Message } from "../types/chat";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "12px",
        padding: "0 16px",
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: "12px 16px",
          borderRadius: "12px",
          backgroundColor: isUser ? "#007bff" : "#f0f0f0",
          color: isUser ? "#fff" : "#333",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          lineHeight: "1.5",
        }}
      >
        {message.content || (message.role === "assistant" ? "..." : "")}
      </div>
    </div>
  );
}
