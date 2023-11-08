TOPIC_GEN_START = """
You are a recommendation algorithm for generating readings regarding a certain
curriculum strands. The curriculum strands in question are: 
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rights, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions 

Now generate some topics.

Do this step by
step. 
1. Generate the name of the topic 
2. Generate a description of the topic

The readings should contain only information relevant to the topic, and should not recommend
curriculum actions such as discussion, analysis, or reflection.

You must give your answers in the following NUMBERED_LIST format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2
"""

TOPIC_GEN_START_ORIGINAL = """
You are a recommendation algorithm for generating topics regarding a certain
curriculum strands. The curriculum strands in question are: 
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rights, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions Now generate some topics.Do this step by
step. 
1. Generate the name of the topic 
2. Generate a description of the topic

You must give your answers in the following NUMBERED_LIST format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2

"""


TOPIC_GEN_CONTINUATION = """
You are helping a teacher narrow down course readings for a given topic.
I will provide you with a general topic covering multiple areas of interest and
you should give an multiple suggestions that delve into the more specific
examples provided in my topic. 

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2

Also, constrain your course recommendation such that it fufils the learning
goals listed below: select and organize relevant evidence, data, and information
on issues, events, and/or developments of civic importance from a variety of
primary and secondary sources, including media forms such as social and
traditional media, ensuring that their sources reflect multiple perspectives

Your output should be readings should contain only information relevant to the topic, and should not recommend
curriculum actions such as discussion, analysis, or reflection.

General recommendation: {topic}

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2
"""

TOPIC_GEN_CONTINUATION_ORIGINAL = """
You are helping a teacher narrow down course recommendations for a given topic.
I will provide you with a general topic covering multiple areas of interest and
you should give an multiple suggestions that delve into the more specific
examples provided in my topic. 

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2

Also, constrain your course recommendation such that it fufils the learning
goals listed below: select and organize relevant evidence, data, and information
on issues, events, and/or developments of civic importance from a variety of
primary and secondary sources, including media forms such as social and
traditional media, ensuring that their sources reflect multiple perspectives

General recommendation: {topic}

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2
"""

ENTITY_EXTRACTOR = """
In the topic and description, identify the entities in the following text:

Text: {text}

You must give your answers in the following format, and ONLY in the following
format, or else my family will die:
ENTITY: entity1 </ENTITY>
ENTITY: entity2</ENTITY>
ENTITY: entity3</ENTITY>
"""

# ITERATIVELY_GENERATE_TOPICS = """
# You are a recommendation algorithm for generating readings regarding a certain
# curriculum strands. The curriculum strands in question are: 
# describe fundamental beliefs and values associated with democratic citizenship in Canada, including
# democracy, human rights, freedom, and the rule of law, identifying some of their
# key historical foundations, and explain ways in which these beliefs and values
# are reflected in citizen actions Now generate some topics. 

# Do this step by step. 
# 1. Generate the name of the topic 
# 2. Generate a description of the topic

# The readings should contain only information relevant to the topic, and should not recommend
# curriculum actions such as discussion, analysis, or reflection.

# {topic}

# You must give your answers in JSON format, and ONLY in the following
# format, or else bad things will happen: 
# [
#     {    
#         "topic": "TOPIC1",
#         "description": "DESCRIPTION1"
#     },
#     {    
#         "topic": "TOPIC2",
#         "description": "DESCRIPTION2"
#     },
# ]

# The following topics have already been generated. There are two restrictions:
# 1. Dont generate any topics that are already included in the list below
# 2. Dont generate any topics that could be subtopics of the one below

# For example:
# SAMPLE TOPIC LIST:
# The Canadian Charter of Rights and Freedoms
# Indigenous Rights and Reconciliation in Canada
# Civil Liberties in Canadian History

# DONT GENERATE:
# Civil Liberties in Canadian History
# The History of Civil Liberties in Canada (same as above)
# Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
# Historical Context of the Canadian Charter of Rights and Freedoms (subtopics of The Canadian Charter of Rights and Freedoms)
# Overview and Structure of the Charter (subtopics of The Canadian Charter of Rights and Freedoms)
# Fundamental Freedoms and Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
# Fundamental Freedoms and Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
# Comparison of the Charter with International Human Rights Documents (subtopics of The Canadian Charter of Rights and Freedoms)

# Now here is the list. Generate some topics following the rules laid out above

# {fewfwef}
# """

TOPIC_GEN_CONTINUATION_ORIGINAL = """
You are helping a teacher narrow down course recommendations for a given topic.
I will provide you with a general topic covering multiple areas of interest and
you should give an multiple suggestions that delve into the more specific
examples provided in my topic. 

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2

Also, constrain your course recommendation such that it fufils the learning
goals listed below: select and organize relevant evidence, data, and information
on issues, events, and/or developments of civic importance from a variety of
primary and secondary sources, including media forms such as social and
traditional media, ensuring that their sources reflect multiple perspectives

General recommendation: {topic}

You must give your answers in the following format, and ONLY in the following
format, or else bad things will happen: 
TOPIC: TOPIC1 
DESCRIPTION: DESCRIPTION1
TOPIC: TOPIC2 
DESCRIPTION: DESCRIPTION2
"""

ENTITY_EXTRACTOR = """
In the topic and description, identify the entities in the following text:

Text: {text}

You must give your answers in the following format, and ONLY in the following
format, or else my family will die:
ENTITY: entity1 </ENTITY>
ENTITY: entity2</ENTITY>
ENTITY: entity3</ENTITY>
"""

ITERATIVELY_GENERATE_TOPICS = """
You are a recommendation algorithm for generating readings regarding a certain
curriculum strands. The curriculum strands in question are: 
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rights, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions 

Now generate some topics. 

Do this step by step. 
1. Generate the name of the topic 
2. Generate a description of the topic

The readings should contain only information relevant to the topic, and should not recommend
curriculum actions such as discussion, analysis, or reflection.

Here are a list of topics that have already been generated. There are two restrictions:
{topics}

The following topics have already been generated. There are two restrictions:
1. Dont generate any topics that are already included in the list below
2. Dont generate any topics that could be subtopics of the one below

For example:
SAMPLE TOPIC LIST:
The Canadian Charter of Rights and Freedoms
Indigenous Rights and Reconciliation in Canada
Civil Liberties in Canadian History

DONT GENERATE:
Civil Liberties in Canadian History
The History of Civil Liberties in Canada (same as above)
Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
Historical Context of the Canadian Charter of Rights and Freedoms (subtopics of The Canadian Charter of Rights and Freedoms)
Overview and Structure of the Charter (subtopics of The Canadian Charter of Rights and Freedoms)
Fundamental Freedoms and Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
Fundamental Freedoms and Democratic Rights (subtopics of The Canadian Charter of Rights and Freedoms)
Comparison of the Charter with International Human Rights Documents (subtopics of The Canadian Charter of Rights and Freedoms)


GIVE YOUR OUTPUT IN JSON. DONT RESPOND WITH ANYTHING OTHER THAN JSON, INCLUDING AN ACKNOWLEDGEMENT OF THIS MESSAGE: 
[
    {{    
        "topic": "TOPIC1",
        "description": "DESCRIPTION1"
    }},
    {{    
        "topic": "TOPIC2",
        "description": "DESCRIPTION2"
    }},
]
"""



OUTPUT_JSON = """
Give the output in a json array format. This should be your only output. Failure to do so will result in bad things: 
[{{
    "topic": "The Magna Carta: Cornerstone ofDemocracy and the Rule of Law",
    "description": "Explore the historical significance
    of the Magna Carta as a foundational document that influenced democratic
    principles and the rule of law in Canada. Discuss its key provisions and their
    impact on shaping the country's democratic values. Analyze how these beliefs and
    values are reflected in the actions of Canadian citizens today.",
}}, 
{{
    "topic": ...
    "description": ...
}},
...
]
"""