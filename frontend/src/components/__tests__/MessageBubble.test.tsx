import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MessageBubble } from "../MessageBubble";
import type { Message } from "../../types/chat";

function buildMessage(overrides: Partial<Message> = {}): Message {
  return {
    id: "msg-1",
    conversation_id: "conv-1",
    role: "user",
    content: "Hello, world!",
    created_at: "2026-01-01T00:00:00Z",
    ...overrides,
  };
}

describe("MessageBubble", () => {
  it("should render user message content", () => {
    render(<MessageBubble message={buildMessage({ content: "Test message" })} />);
    expect(screen.getByText("Test message")).toBeInTheDocument();
  });

  it("should render assistant message content", () => {
    render(
      <MessageBubble
        message={buildMessage({ role: "assistant", content: "AI response" })}
      />
    );
    expect(screen.getByText("AI response")).toBeInTheDocument();
  });

  it("should show placeholder when assistant message has no content", () => {
    render(
      <MessageBubble message={buildMessage({ role: "assistant", content: "" })} />
    );
    expect(screen.getByText("...")).toBeInTheDocument();
  });

  it("should apply different styles for user vs assistant", () => {
    const { container: userContainer } = render(
      <MessageBubble message={buildMessage({ role: "user" })} />
    );
    const userBubble = userContainer.querySelector("div > div");
    expect(userBubble).toHaveStyle({ justifyContent: "flex-end" });

    const { container: assistantContainer } = render(
      <MessageBubble message={buildMessage({ role: "assistant" })} />
    );
    const assistantBubble = assistantContainer.querySelector("div > div");
    expect(assistantBubble).toHaveStyle({ justifyContent: "flex-start" });
  });
});
