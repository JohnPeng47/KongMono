from bot.base import KnowledgeGraph
import streamlit as st

kg = KnowledgeGraph("h", graph_id="e45cd912-37a7-4eb4-9c72-c24345f07f2f")
tree = kg.display_tree()

for line in tree.split("\n"):
    st.write(line)

