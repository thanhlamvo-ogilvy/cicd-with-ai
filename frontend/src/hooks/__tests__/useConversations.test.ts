import { renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useConversations } from "../useConversations";
import * as api from "../../services/api";
import type { Conversation, ConversationListResponse } from "../../types/chat";

vi.mock("../../services/api");

const mockConversations: Conversation[] = [
  {
    id: "conv-1",
    title: "Test Chat",
    provider: "openai",
    model: "gpt-4",
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  },
];

const mockResponse: ConversationListResponse = {
  conversations: mockConversations,
  total: 1,
};

beforeEach(() => {
  vi.resetAllMocks();
});

describe("useConversations", () => {
  it("should return conversations after loading", async () => {
    vi.mocked(api.fetchConversations).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useConversations());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.conversations).toEqual(mockConversations);
  });

  it("should return empty conversations on error", async () => {
    vi.mocked(api.fetchConversations).mockRejectedValue(new Error("Network error"));

    const { result } = renderHook(() => useConversations());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.conversations).toEqual([]);
  });

  it("should remove a conversation and refresh", async () => {
    vi.mocked(api.fetchConversations).mockResolvedValue(mockResponse);
    vi.mocked(api.deleteConversation).mockResolvedValue(undefined);

    const { result } = renderHook(() => useConversations());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const emptyResponse: ConversationListResponse = { conversations: [], total: 0 };
    vi.mocked(api.fetchConversations).mockResolvedValue(emptyResponse);

    await result.current.remove("conv-1");

    expect(api.deleteConversation).toHaveBeenCalledWith("conv-1");
    await waitFor(() => {
      expect(result.current.conversations).toEqual([]);
    });
  });
});
