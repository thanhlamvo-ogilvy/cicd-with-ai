import { type FormEvent, useState } from "react";

interface ChatInputProps {
  onSend: (content: string) => void;
  disabled: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "flex",
        gap: "8px",
        padding: "16px",
        borderTop: "1px solid #e0e0e0",
      }}
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={disabled ? "Waiting for response..." : "Type a message..."}
        disabled={disabled}
        aria-label="Message input"
        style={{
          flex: 1,
          padding: "12px 16px",
          borderRadius: "8px",
          border: "1px solid #ddd",
          fontSize: "14px",
          outline: "2px solid transparent",
          outlineOffset: "2px",
        }}
        onFocus={(e) => {
          e.currentTarget.style.outline = "2px solid #007bff";
          e.currentTarget.style.outlineOffset = "2px";
        }}
        onBlur={(e) => {
          e.currentTarget.style.outline = "2px solid transparent";
        }}
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        aria-label="Send message"
        style={{
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: disabled || !input.trim() ? "#ccc" : "#007bff",
          color: "#fff",
          fontSize: "14px",
          cursor: disabled || !input.trim() ? "not-allowed" : "pointer",
          outline: "2px solid transparent",
          outlineOffset: "2px",
        }}
        onFocus={(e) => {
          e.currentTarget.style.outline = "2px solid #0056b3";
          e.currentTarget.style.outlineOffset = "2px";
        }}
        onBlur={(e) => {
          e.currentTarget.style.outline = "2px solid transparent";
        }}
      >
        Send
      </button>
    </form>
  );
}
