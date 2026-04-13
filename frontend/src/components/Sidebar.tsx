import type { Conversation } from "../types/chat";

interface SidebarProps {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
}

export function Sidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
  onDelete,
}: SidebarProps) {
  return (
    <div
      style={{
        width: "260px",
        borderRight: "1px solid #e0e0e0",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#fafafa",
      }}
    >
      <button
        onClick={onNew}
        style={{
          margin: "16px",
          padding: "10px",
          borderRadius: "8px",
          border: "1px solid #ddd",
          backgroundColor: "#fff",
          cursor: "pointer",
          fontSize: "14px",
        }}
      >
        + New Chat
      </button>
      <div style={{ flex: 1, overflowY: "auto" }}>
        {conversations.map((conv) => (
          <div
            key={conv.id}
            role="button"
            tabIndex={0}
            onClick={() => onSelect(conv.id)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(conv.id);
              }
            }}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "10px 16px",
              cursor: "pointer",
              backgroundColor: activeId === conv.id ? "#e8f0fe" : "transparent",
              borderLeft: activeId === conv.id ? "3px solid #007bff" : "3px solid transparent",
            }}
          >
            <span
              style={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                flex: 1,
                fontSize: "13px",
              }}
            >
              {conv.title}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(conv.id);
              }}
              aria-label={`Delete conversation: ${conv.title}`}
              style={{
                background: "none",
                border: "none",
                color: "#999",
                cursor: "pointer",
                fontSize: "16px",
                padding: "0 4px",
                outline: "2px solid transparent",
                outlineOffset: "2px",
              }}
              onFocus={(e) => {
                e.currentTarget.style.outline = "2px solid #007bff";
              }}
              onBlur={(e) => {
                e.currentTarget.style.outline = "2px solid transparent";
              }}
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
