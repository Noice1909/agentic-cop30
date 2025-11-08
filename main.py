import os, sys, yaml
from agents.memory import Memory
from graph import build_graph, State
from dotenv import load_dotenv
load_dotenv()
def run(topic_yaml="topics/cop30.yaml"):
    cfg = yaml.safe_load(open(topic_yaml, "r", encoding="utf-8"))
    memory = Memory()
    graph = build_graph(memory)
    final = graph.invoke(State(topic=cfg["name"]))
    print("\n=== DAILY BRIEF ===\n")
    print(final.get("brief_markdown", "(no brief_markdown in state)"))

if __name__ == "__main__":
    run()
