# smart-college-study-assistant

import os
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

load_dotenv()

AGENT_NAME = "smart-college-study-assistant"
SEED_PHRASE = os.getenv("AGENT_SEED_PHRASE", "change-this-study-assistant-seed")
ASI_API_KEY = os.getenv("ASI_API_KEY")

# ASI:One uses an OpenAI-compatible API.
client = OpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=ASI_API_KEY or "missing-api-key",
)

agent = Agent(
    name=AGENT_NAME,
    seed=SEED_PHRASE,
    mailbox=True,
    publish_agent_details=True,
)

chat_protocol = Protocol(spec=chat_protocol_spec)

SYSTEM_PROMPT = """
You are Smart College Study Assistant, a friendly academic helper for college students.

Your jobs:
- Explain concepts in simple, student-friendly language.
- Help with maths and engineering problems by showing clear steps.
- Create short notes, revision sheets, quizzes, flashcards, and study plans.
- Explain programming errors and provide corrected example code.
- Help students plan study time around deadlines and exams.
- When a question is ambiguous, ask one short clarifying question.
- Be honest when uncertain. Never invent citations, facts, or exam rules.
- For calculations, show the method and check the result where possible.
- Keep answers organized with headings or bullets, but match the student's requested length.
- Encourage learning: explain why an answer works, not only the final answer.
- Do not claim to access a student's college portal, private files, or timetable unless they provide that information.
"""

def extract_text(message: ChatMessage) -> str:
    """Join all text chunks in a chat message."""
    chunks = []
    for item in message.content:
        if isinstance(item, TextContent):
            chunks.append(item.text)
    return "\n".join(chunks).strip()

def make_study_answer(question: str) -> str:
    """Ask ASI:One to answer the student's question."""
    if not ASI_API_KEY:
        return (
            "The agent is running, but ASI_API_KEY is not configured yet.\n\n"
            "Add your ASI:One API key to the .env file as ASI_API_KEY=your_key, "
            "then restart the agent."
        )

    result = client.chat.completions.create(
        model="asi1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=1200,
        temperature=0.4,
    )
    answer = result.choices[0].message.content
    return answer.strip() if answer else "I couldn't produce an answer. Please try again."

@chat_protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Acknowledge receipt so compatible chat clients know the message arrived.
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    question = extract_text(msg)
    if not question:
        answer = "Please send a text question, such as 'Explain eigenvalues in simple words'."
    else:
        try:
            answer = make_study_answer(question)
        except Exception:
            ctx.logger.exception("Study assistant request failed")
            answer = (
                "Sorry, I couldn't process that request. Check that your ASI:One API key "
                "is valid and that your internet connection is working, then try again."
            )

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=answer),
                EndSessionContent(type="end-session"),
            ],
        ),
    )

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Smart College Study Assistant is online.")
    ctx.logger.info(f"Agent address: {ctx.agent.address}")
    if not ASI_API_KEY:
        ctx.logger.warning("ASI_API_KEY is missing. Add it to .env to enable AI answers.")

agent.include(chat_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
