import { useState, useCallback, useRef } from "react";
import type { Message } from "../types/chat";
import { streamChat } from "../services/api";

interface UseChatReturn {
  messages: Message[];
  isStreaming: boolean;
  conversationId: string | null;
  sendMessage: (content: string, provider: string, model: string) => Promise<void>;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  setConversationId: React.Dispatch<React.SetStateAction<string | null>>;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const abortRef = useRef(false);

  const sendMessage = useCallback(
    async (content: string, provider: string, model: string) => {
      if (isStreaming) return;

      const userMessage: Message = {
        id: crypto.randomUUID(),
        conversation_id: conversationId || "",
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsStreaming(true);
      abortRef.current = false;

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        conversation_id: conversationId || "",
        role: "assistant",
        content: "",
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      try {
        const stream = streamChat({
          conversation_id: conversationId || undefined,
          content,
          provider,
          model,
        });

        for await (const event of stream) {
          if (abortRef.current) break;

          if (event.conversation_id && !conversationId) {
            setConversationId(event.conversation_id);
          }

          if (event.token) {
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last && last.role === "assistant") {
                updated[updated.length - 1] = {
                  ...last,
                  content: last.content + event.token,
                };
              }
              return updated;
            });
          }
        }
      } catch (error) {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last && last.role === "assistant") {
            updated[updated.length - 1] = {
              ...last,
              content: "Error: Failed to get response. Please try again.",
            };
          }
          return updated;
        });
      } finally {
        setIsStreaming(false);
      }
    },
    [conversationId, isStreaming]
  );

  return { messages, isStreaming, conversationId, sendMessage, setMessages, setConversationId };
}
