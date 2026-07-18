"use client";

import { useState } from "react";
import { Bot, Send } from "lucide-react";
import ReactMarkdown from "react-markdown"

export default function AssistantPage() {
  const [message, setMessage] = useState("");

  const [chat, setChat] = useState<any[]>([]);

  async function sendMessage() {
    if (!message.trim()) return;

    setChat((prev) => [
      ...prev,

      {
        role: "user",
        content: message,
      },
    ]);

    const userMessage = message;

    setMessage("");

    // later replace with your chatbot API

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: userMessage,
      }),
    });

    const data = await response.json();

    setChat((prev) => [
      ...prev,

      {
        role: "ai",

        content: data.response,
      },
    ]);
  }

  return (
    <div className="space-y-6">
      <header>
        <h1
          className="
font-display
text-3xl
font-bold
text-red-glow
text-glow
"
        >
          AI REMEDIATION ASSISTANT
        </h1>

        <p
          className="
text-text-muted
font-mono
text-sm
"
        >
          Ask about vulnerabilities, fixes, and security recommendations.
        </p>
      </header>

      <div
        className="
bg-panel
border
border-hairline
rounded-md
p-5
h-[600px]
flex
flex-col
"
      >
        <div
          className="
flex-1
overflow-y-auto
space-y-4
"
        >
          {chat.map((msg, index) => (
            <div
              key={index}
              className={
                msg.role === "user"
                  ? "ml-auto bg-red-primary/20 border border-red-primary rounded p-3 max-w-xl"
                  : "bg-panel-raised border border-hairline rounded p-3 max-w-xl"
              }
            >
              <div
                className="
flex
items-center
gap-2
mb-2
text-xs
font-mono
"
              >
                {msg.role === "ai" ? <Bot size={14} /> : null}

                {msg.role === "ai" ? "REDMIND AI" : "YOU"}
              </div>

              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          ))}
        </div>

        <div
          className="
flex
gap-3
border-t
border-hairline
pt-4
"
        >
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="
Explain SQL Injection remediation...
"
            className="
flex-1
bg-void
border
border-hairline
rounded
px-4
py-3
font-mono
text-sm
focus:border-red-primary
outline-none
"
          />

          <button
            onClick={sendMessage}
            className="
bg-red-primary
text-void
px-5
rounded
font-mono
font-bold
flex
items-center
gap-2
"
          >
            <Send size={16} />
            SEND
          </button>
        </div>
      </div>
    </div>
  );
}
