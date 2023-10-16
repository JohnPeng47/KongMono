# might want to extend something on top of Graph
from bot.base import KnowledgeGraph
from bot.exploration import generate_concepts, generate_topics, generate_sections, generate_expansion
from bot.base import BaseLLM
from utils import DBConnection

db_conn = DBConnection()
collection = db_conn.get_collection("test")


test_json = {
    "id": "4eb623af-7c9e-43c0-a5c0-8c8872173442",
    "node_data": {
        "title": "Democracy + Rule of Law + Human Rights",
        "node_type": "ROOT",
        "children": [{
                "id": "960099c2-ff16-40e5-bdc4-b53a6ca36bf0",
                "node_data": {
                    "title": "Democracy",
                    "concept": "Democracy",
                    "node_type": "CONCEPT_NODE",
                    "children": [{
                        "id": "285c6064-438a-454f-9924-9937b1b6d198",
                        "node_data": {
                            "title": "Freedom of Expression in a Democratic Society",
                            "description": "Explore the importance of freedom of expression in democratic citizenship. Discuss the historical struggles for free speech in Canada, including landmark cases and legislative developments that have shaped the current understanding of this democratic value.",
                            "node_type": "TOPIC_NODE",
                            "children": []
                        }
                    }]
                }
            },
            {
                "id": "b30ff803-c465-4bc8-93f9-b1acf46e5af2",
                "node_data": {
                    "title": "Rule of law",
                    "concept": "Rule of law",
                    "node_type": "CONCEPT_NODE",
                    "children": [{
                            "id": "fa5dc901-d21a-460a-850f-f5f74966909f",
                            "node_data": {
                                "title": "Charter of Rights and Freedoms",
                                "description": "Discuss the significance of the Canadian Charter of Rights and Freedoms in upholding the rule of law. Explore how the Charter guarantees fundamental rights and freedoms to all citizens and examine landmark cases that have shaped its interpretation.",
                                "node_type": "TOPIC_NODE",
                                "children": [{
                                        "id": "01149dc8-9adf-46a9-9309-2142374e33a1",
                                        "node_data": {
                                            "title": "name",
                                            "section": "Section 15: Equality Rights",
                                            "node_type": "SECTION_NODE",
                                            "children": []
                                        }
                                    },
                                    {
                                        "id": "8863b0b6-1bdc-4f3e-b48a-778a6b97201a",
                                        "node_data": {
                                            "title": "section",
                                            "section": "Section 15 of the Charter guarantees equality rights to all Canadians, prohibiting discrimination based on various grounds such as race, national or ethnic origin, color, religion, sex, age, or mental or physical disability. This section aims to promote equality and eliminate discrimination in all aspects of Canadian society. It has been instrumental in advancing the rights of marginalized communities and ensuring equal treatment under the law. Section 15 has played a significant role in shaping cases related to same-sex marriage, gender equality, and affirmative action, among others.",
                                            "node_type": "SECTION_NODE",
                                            "children": [{
                                                "id": "c9708eac-1f89-49d8-a19a-ee23d2c2669f",
                                                "node_data": {
                                                    "title": "Key Historical Foundations: The Women's Suffrage Movement",
                                                    "paragraph": "The Women's Suffrage Movement in Canada is a key historical foundation that reflects the fundamental beliefs and values associated with democratic citizenship. This movement fought for women's right to vote and participate in the democratic process. Notable campaigns within the Women's Suffrage Movement served as powerful demonstrations of the determination and resilience of suffragettes. Two significant campaigns worth mentioning are the Ontario Mock Parliament and the Winnipeg Women's Conference. The Ontario Mock Parliament, held in 1917, was an innovative initiative that aimed to illustrate the capabilities and competence of women in political leadership roles. It provided a platform for women to showcase their abilities and challenge the notion that women were unfit for political participation. The Winnipeg Women's Conference, held in 1919, brought together suffragettes from across the country to discuss and strategize on advancing women's rights. These campaigns and events played a crucial role in raising awareness, mobilizing support, and ultimately contributing to the achievement of women's suffrage in Canada.",
                                                    "node_type": "EXPANDED_TEXT_NODE",
                                                    "keywords": [
                                                        "Women's Suffrage Movement",
                                                        "democratic citizenship",
                                                        "women's right to vote",
                                                        "democratic process",
                                                        "Ontario Mock Parliament",
                                                        "Winnipeg Women's Conference",
                                                        "political leadership",
                                                        "women's suffrage"
                                                    ],
                                                    "children": []
                                                }
                                            }]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "id": "47cdc8d2-a88a-4cdc-bdd6-716d7960fe32",
                            "node_data": {
                                "title": "Legal Protections and Safeguards",
                                "description": "Examine the legal protections and safeguards in place to ensure the rule of law is upheld in Canada. Discuss the role of legal institutions, such as the police, courts, and regulatory bodies, in enforcing laws and protecting individual rights.",
                                "node_type": "TOPIC_NODE",
                                "children": []
                            }
                        },
                        {
                            "id": "ac7dab73-daa1-4ae9-a5d4-7b007f224845",
                            "node_data": {
                                "title": "Public Participation in Lawmaking",
                                "description": "Explore how public participation in the lawmaking process reflects the principles of the rule of law. Discuss the importance of transparency, accountability, and inclusivity in democratic decision-making.",
                                "node_type": "TOPIC_NODE",
                                "children": [{
                                    "id": "e0fd18c9-4a72-46d3-b432-675be2e6b12e",
                                    "node_data": {
                                        "title": "name",
                                        "section": "Section 2: Transparency in Lawmaking",
                                        "node_type": "SECTION_NODE",
                                        "children": [{
                                            "id": "45eda898-482a-46a0-81c1-91ded7fc4ade",
                                            "node_data": {
                                                "title": "Whistleblower Protection",
                                                "paragraph": "Whistleblower protection is a crucial component of transparency in lawmaking. It refers to the legal safeguards and mechanisms in place to protect individuals who disclose information about wrongdoing or illegal activities within the government or public sector. Whistleblowers play a vital role in exposing corruption, promoting accountability, and upholding the rule of law. In Canada, the Public Servants Disclosure Protection Act (PSDPA) was enacted in 2007 to provide federal public servants with protection when reporting wrongdoing. This act establishes a framework for investigation and resolution of disclosures, ensuring that whistleblowers are shielded from reprisals and can come forward with information without fear of retaliation.",
                                                "node_type": "EXPANDED_TEXT_NODE",
                                                "keywords": [
                                                    "whistleblower protection",
                                                    "legal safeguards",
                                                    "mechanisms",
                                                    "disclose information",
                                                    "wrongdoing",
                                                    "illegal activities",
                                                    "government",
                                                    "public sector",
                                                    "exposing corruption",
                                                    "accountability",
                                                    "rule of law",
                                                    "Public Servants Disclosure Protection Act",
                                                    "federal public servants",
                                                    "reporting wrongdoing",
                                                    "framework for investigation",
                                                    "resolution of disclosures",
                                                    "shielded from reprisals",
                                                    "fear of retaliation"
                                                ],
                                                "children": []
                                            }
                                        }]
                                    }
                                }]
                            }
                        }
                    ]
                }
            }
        ]
    }
}

curriculum = """
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rightds, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions 
"""

graph_id = "4eb623af-7c9e-43c0-a5c0-8c8872173442"
graph_json = db_conn.find_graph(graph_id)
node = Node.from_json_update_keys(graph_json)

db_conn.insert_graph(node.to_json())




