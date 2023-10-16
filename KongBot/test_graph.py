from bot.base import KnowledgeGraph

# curriculum = """
# describe fundamental beliefs and values associated with democratic citizenship in Canada, including
# democracy, human rightds, freedom, and the rule of law, identifying some of their
# key historical foundations, and explain ways in which these beliefs and values
# are reflected in citizen actions 
# """

# kg = KnowledgeGraph(curriculum)
# kg.add_node("hl", name="world")
# kg.add_node(1)
# kg.add_node(3)
# # build a filter
# # upserts are done by key values
# kg.add_node("key", node_data={"hello": "woild"})
# kg.add_node("key", node_data={"hello": "1234"})

# kg.add_node("key2", node_data={"hello": "1234111"})


# # kg.add_edge(("key2", {"hello": "woild"}), ("key", {"hello": "woild"}))

# # print(kg.edges("key2"))
# # for n in kg.nodes():
# #     print(n)

# # all of our node data are going to be stored in node_data
# node_f = {}

# res = kg.filter_nodes(node_f)
# for n in res:
#     print(n)

class A:
    def print(self):
        print(self.__class__.__name__)

class B(A):
    pass
    # def print(self):
    #     print(self.__class__.__name__)

b = B()
b.print()