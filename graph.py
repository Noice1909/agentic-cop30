from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from agents.planner import plan
from agents.web_searcher import gather
from agents.writer import write_brief
from agents.memory import Memory

class State(BaseModel):
    topic: str
    tasks: list[str] = []
    docs: list[dict] = []
    brief_markdown: str | None = None

def node_plan(state: State, *, memory: Memory):
    tasks = plan(topic=state.topic, memory=memory)
    return {"tasks": tasks}

def node_gather(state: State, *, memory: Memory):
    docs = gather(tasks=state.tasks, memory=memory)
    return {"docs": docs}

def node_write(state: State, *, memory: Memory):
    brief = write_brief(topic=state.topic, docs=state.docs, memory=memory)
    memory.remember(docs=state.docs)  # store hashes / seen URLs
    return {"brief_markdown": brief}

def build_graph(memory: Memory):
    g = StateGraph(State)
    g.add_node("plan", lambda s: node_plan(s, memory=memory))
    g.add_node("gather", lambda s: node_gather(s, memory=memory))
    g.add_node("write", lambda s: node_write(s, memory=memory))
    g.add_edge("plan", "gather")
    g.add_edge("gather", "write")
    g.add_edge("write", END)
    g.set_entry_point("plan")
    return g.compile()
