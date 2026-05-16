import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  createConversation,
  deleteConversation,
  fetchConversation,
  fetchConversations,
} from "../api";

beforeEach(() => {
  vi.restoreAllMocks();
});

function mockFetch(body: unknown, ok = true, status = 200) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(body),
  } as Response);
}

describe("fetchConversations", () => {
  it("should return conversations on success", async () => {
    const data = { conversations: [{ id: "1" }], total: 1 };
    mockFetch(data);

    const result = await fetchConversations();

    expect(result).toEqual(data);
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/conversations");
  });

  it("should throw on error response", async () => {
    mockFetch(null, false, 500);

    await expect(fetchConversations()).rejects.toThrow(
      "Failed to fetch conversations"
    );
  });
});

describe("fetchConversation", () => {
  it("should return a single conversation", async () => {
    const data = { id: "1", title: "Test", messages: [] };
    mockFetch(data);

    const result = await fetchConversation("1");

    expect(result).toEqual(data);
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/conversations/1");
  });

  it("should throw on error response", async () => {
    mockFetch(null, false, 404);

    await expect(fetchConversation("1")).rejects.toThrow(
      "Failed to fetch conversation"
    );
  });
});

describe("createConversation", () => {
  it("should create and return a conversation", async () => {
    const data = { id: "new-1", title: "New Chat" };
    mockFetch(data);

    const result = await createConversation("openai", "gpt-4");

    expect(result).toEqual(data);
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "New Chat", provider: "openai", model: "gpt-4" }),
    });
  });

  it("should throw on error response", async () => {
    mockFetch(null, false, 400);

    await expect(createConversation("openai", "gpt-4")).rejects.toThrow(
      "Failed to create conversation"
    );
  });
});

describe("deleteConversation", () => {
  it("should delete without error on success", async () => {
    mockFetch(null);

    await expect(deleteConversation("1")).resolves.toBeUndefined();
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/conversations/1", {
      method: "DELETE",
    });
  });

  it("should throw on error response", async () => {
    mockFetch(null, false, 500);

    await expect(deleteConversation("1")).rejects.toThrow(
      "Failed to delete conversation"
    );
  });
});
