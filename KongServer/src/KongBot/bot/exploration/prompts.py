INITIAL_EXPLORATORY_QUESTIONS = """
Generate 3 concepts that are related to the following curriculum goal. These
concepts are fundamental to the concept, and should allow the student to explore
them further. Along with the 3 concepts, generate 3 follow-up questions that
could be asked when the concept is selected. The curriculum is as follows:

{curriculum}

The questions generated should not be knowledge based, but rather, assume no
prior understanding of the concept. Rather, ask more personal questions that
relates the student to the concept, and ask it in a way that will spark further
engagement

Return your response in JSON format:
[
    {{    
        "concept": "concept1"
    }},
    {{    
        "concept": "concept2"
    }},
]
"""

INITIAL_EXPLORATORY_CONCEPTS = """
Generate 3 concepts along with an associated description that are related to the following
curriculum goal. These concepts are fundamental to the concept, and should allow the student to explore
them further. The curriculum is as follows:

{curriculum}    

Return your response in JSON format, and dont include any numberings in the json value generated:
[
    {{    
        "concept": "concept1",
        "description": "description1"
    }},
    {{    
        "concept": "concept2",
        "description": "description2"
    }},
    ...
]
"""

GENERATE_TOPICS = """
Given the concept: {concept}, that is related to the following curriculum goal, generate 
some topics that are related to the concept, along with a short description of the topic.
{curriculum}

Here is a more detailed description of the topic:
{description}

Return your response in JSON format, and dont include any numberings in the json value generated:
[
    {{    
        "topic": "topic1",
        "description": "description1"
    }},
    {{    
        "topic": "topic2",
        "description": "description1"
    }},
    ...
]

For example when asked to generate topics for the concept: The Rule of Law, with the following curriculum:
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rights, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions 

The following response is generated:

[
{{
    "topic" : "The Evolution of Canadian Legal System",
    "description": "Explore the historical development of Canada's legal system, tracing its roots from British common law and examining key milestones in the establishment of the rule of law in Canada."
}},
{{
    "topic": "Charter of Rights and Freedoms",
    "description" : "Discuss the significance of the Canadian Charter of Rights and Freedoms in upholding the rule of law. Explore how the Charter guarantees fundamental rights and freedoms to all citizens and examine landmark cases that have shaped its interpretation."
}}
...
]

Now generate {num} elements of the list described above
"""

ENTITY_EXTRACTOR = """
In the topic and description, identify the entities in the following text:

Text: {text}

Give your output in a JSON list format, as follows:                        
[
    "entity1",
    "entity2",
    "entity3",
    ...
]
"""

GENERATE_SECTIONS = """
Expand the following description enclosed with **** into a full Canadian civics textbook excerpt
with multiple sections. Do not include an introduction or conclusion:

****
{topic}
{description}
****

Output your answer in JSON format for example:
Expand the following description into a full Canadian civics textbook excerpt
with a introduction, multiple sections and a conclusion: Legal Rights and Responsibilities in Canada Explore the historical development of human rights in Canada,
tracing its roots from the Canadian Bill of Rights to the Canadian Charter of
Rights and Freedoms. Examine key milestones in the recognition and protection of
human rights in Canada 

Output your response in JSON format. An example response is in the following format: 
[
    {{
        "name":"Democratic Rights",
        "section":"Canada is a parliamentary democracy, and its
        citizens have the privilege of participating in free and fair elections.
        The Charter enshrines these democratic rights, granting every eligible
        citizen the right to vote and seek public office. Through exercising
        their democratic rights, Canadians have the power to influence the
        direction of the government and make their voices heard on crucial
        matters",
        "keywords": ["democracy", "elections", "voting", "public office"]
    }}, 
    {{ 
        "name": "Mobility Rights",
        "section": "In a vast and diverse country like
        Canada, the Charter recognizes the importance of mobility. Canadians
        have the right to move and live within any province or territory and the
        right to enter and leave the country freely. These mobility rights
        contribute to the unification of the nation and ensure that all citizens
        can pursue opportunities and create a life of their choosing.",
        "keywords": ["mobility", "rights"]
    }}, 
    ...
]

The JSON generated should conform to this jsonschema:
{schema}

Expand the above description enclosed with  into a full Canadian civics textbook excerpt
with multiple sections. Do not include an introduction or conclusion

Now generate {num} elements of the list described above
"""

GENERATE_EXPAND = """
Expand the following section into a full textbook page, making it as long and detailed
as possible. Here are several requirements:

1. Note that the emphasis is on the following curriculum strands:
{curriculum}

2. All of paragraphs provided below should cite a specific historical/concrete/real life example
{section}

3. Also include a list of keywords/key topics for each of the paragraph you
generate.

Here is a sample output
Output your answer in JSON format for example: 
[
{{
    "expansion":"Notable Campaigns", 
    "section": " The Women's Suffrage Movement
    was marked by numerous campaigns that served as powerful demonstrations of
    the determination and resilience of suffragettes. Two significant campaigns
    worth mentioning are the Ontario Mock Parliament and the Winnipeg Women's
    Conference. The Ontario Mock Parliament, held in 1917, was an innovative
    initiative that aimed to illustrate the capabilities and..",
    "keywords": ["suffrage", "Ontario Mock Parliament", "campaigns"] }},
{{
    "expansion":"Victories and Progress", 
    "section": "The culmination of the tireless efforts of suffragettes and their allies resulted in significant
    victories for the Women's Suffrage Movement in Canada. In 1916, the
    province",
    "keywords": ["Women's Suffrage Movement in Canada"] 
}}
...
]

The JSON generated should conform to this jsonschema:
{schema}

Now generate {num} elements of the list described above
"""