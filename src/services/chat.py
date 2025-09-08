# agent.py
from datetime import date

from langchain.agents import AgentType, initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from db import SessionLocal
from repositories.receipt import get_by_date, get_by_item_name


@tool("get_receipts_by_date", return_direct=False)
def get_receipts_by_date_tool(date: str) -> str:
    """Retrieve receipts by a given date (YYYY-MM-DD)."""
    with SessionLocal() as session:
        receipts = get_by_date(session, date)
        if not receipts:
            return f"No receipts found for {date}"
        return "\n".join([str(r) for r in receipts])


@tool("get_receipts_by_item_name", return_direct=False)
def get_receipts_by_item_name_tool(item: str) -> str:
    """Retrieve receipts by a given date (YYYY-MM-DD)."""
    with SessionLocal() as session:
        items = get_by_item_name(session, item)
        if not items:
            return f"No item found for {item}"
        return "\n".join([str(r) for r in items])


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


today = date.today().strftime("%Y-%m-%d")

tools = [get_receipts_by_date_tool, get_receipts_by_item_name_tool]

# Add system prompt with today's date
system_message = SystemMessage(
    content=f"You are a helpful receipt assistant. Today's date is {today}. "
    "Use this context when the user refers to 'today' or 'yesterday'."
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "extra_prompt_messages": [
            system_message,
            MessagesPlaceholder(variable_name="chat_history"),
        ],
    },
)


def run_agent(query: str):
    return agent.run(query)
