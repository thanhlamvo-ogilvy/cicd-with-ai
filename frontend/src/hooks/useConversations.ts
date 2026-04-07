import { useState, useEffect, useCallback } from "react";
import type { Conversation } from "../types/chat";
import { fetchConversations, deleteConversation } from "../services/api";

interface UseConversationsReturn {
  conversations: Conversation[];
  loading: boolean;
  refresh: () => Promise<void>;
  remove: (id: string) => Promise<void>;
}

export function useConversations(): UseConversationsReturn {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const data = await fetchConversations();
      setConversations(data.conversations);
    } catch {
      // Silently fail — list stays empty
    } finally {
      setLoading(false);
    }
  }, []);

  const remove = useCallback(
    async (id: string) => {
      await deleteConversation(id);
      await refresh();
    },
    [refresh]
  );

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { conversations, loading, refresh, remove };
}
