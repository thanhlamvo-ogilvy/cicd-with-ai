import { useCallback, useEffect, useRef, useState } from "react";
import type { Message } from "../types/chat";
import { streamChat } from "../services/api";

interface UseChatReturn {
  messages: Message[];
  isStreaming: boolean;
  conversationId: string | null;
  error: Error | null;
  sendMessage: (content: string, provider: string, model: string) => Promise<void>;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  setConversationId: React.Dispatch<React.SetStateAction<string | null>>;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
      abortRef.current?.abort();
    };
  }, []);

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
      setError(null);
      abortRef.current = new AbortController();

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
          if (!isMountedRef.current || abortRef.current?.signal.aborted) break;

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
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        console.error("Chat streaming error:", error);
        
        if (isMountedRef.current && !abortRef.current?.signal.aborted) {
          setError(error);
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
        }
      } finally {
        if (isMountedRef.current) {
          setIsStreaming(false);
        }
      }
    },
    [conversationId, isStreaming]
  );

  return { messages, isStreaming, conversationId, error, sendMessage, setMessages, setConversationId };
}
