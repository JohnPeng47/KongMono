ROOT_PROMPT = """
Given the following background context, complete the task: 
BACKGROUND CONTEXT:
{context}                        
TASK: 
{task}
"""

TREE = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}
    
TASK:
Given the context above, generate a tree diagram focusing on the historical
background leading up to these events. Use "-->" to denote an additional level
in the tree. The tree should be generated such that each subsequent lower level
features more topics than the one above it Each sublevel should be ranked in
order of importance to the parent top-level topic
"""

TREE_V2 = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}
    
TASK:
Given the context above, generate a tree diagram focusing on the historical
background leading up to these events. The tree should have these properties: 
- Use "-->" to denote an additional level in the tree
- Each sublevel should be ranked in order of importance to the parent top-level topic
- For each level, there should be 4 sublevels
"""

# SUBTREE = """
# Given the following background context, complete the task:
# BACKGROUND CONTEXT:
# {context}

# TASK:
# Your task is expand on the following subtree by adding 3 more levels to each existing level. 
# Keep it short, use phrases, don't employ full sentences                 
# {subtree}
# """

SUBTREE = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}

TASK:
Your task is expand on the following subtree. Here are some requirements:
- add 3 new levels to each child
- never, change the SUBTOPIC_ROOT (different from the parent root)
So if the given tree has the following format
>ROOT 
--> A
--> B
--> C

The new output would be:
>ROOT ** This node is not changed !!! IMPORTANT
--> A
----> A2
--> B
----> B2
--> C
----> C2

Here is the subtree:
{subtree}
"""

SUBTREE_V2 = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}

TASK:
Your task is expand on the following subtree. Here are some requirements:
- generate 3 new levels (child nodes) for each node in the SUBTREE nodes
- use the ANCESTOR nodes as context but do not generate any new levels for it 
- never change the root of the SUBTOPIC nodes
- only give your output in terms of the generated subtree
- ALWAYS start your output with "[0]"
For example, given below:
ANCESTORS
--------
[0] Russia's situation leading up to the Great War
[1] Social unrest
SUBTREE
--------
[0] Role of the intellectual elite
[1] Advocacy for political reform

The new output would be:
[0] Role of the intellectual elite
[1] Advocacy for political reform
[2] Creation of liberal publications and newspapers
[3] Disseminating propaganda among workers and peasants
[3] Promoting political awareness and activism

Here is the subtree:
{subtree}
======================
"""

CONVERT_TO_JSON = """
Convert the following hierarchal tree into JSON. Use each topic at each level as the key
corresponding to a JSON object corresponding to its children:
{tree}

Your JSON output must have the following properties:
- do not include json arrays, only use json objects
  Example:
  {{
    "Historical Background of Russia": {{
        "Russia under Tsar Nicholas II": {{
            "Autocratic Rule": {{}},
            "Russo-Japanese War (1904-05)": {{}},
            "1905 Revolution and aftermath": {{}}
        }},
      ...
  }}
- your output should not contain anything except the generated JSON

Now, just generate the JSON output
"""

SUBTREE_DESCRIPTION_MULTI = """
Take the following subtree and expand into a full detailed summary. 
- the levels above the bar denotes the wider context
- the levels below the bar is the actual issue to be summarized
- focus your summary on the issue below the bar

The generated entry should have the following qualities:
- Historical detail: should contain as many references to historical events as possible
- Identify Key Events: Highlight significant events, dates, and figures.
- Maintain Objectivity: Represent facts without personal bias.
- Focus on Consequences: Discuss the impact or implications of events.
- Be Concise: Use clear, succinct language to convey main points.

The subtree: 
{subtree}
"""

ADD_ROOT_TO_JSON = """"
Given the following JSON, add a root node to the tree. Keep the title short, less than 5 words
{tree_json}
"""

SUBTREE_DESCRIPTION_SINGLE = """
Given the following tree, write a description of each item in the tree.
{tree}
The description should be:
- Relevant: to the main topic
- Descriptive yet Concise: 4-7 sentences
- Connected: should tie into sibling descriptions

Output your answer in a flat JSON structure, where each key is an item from the tree
and the value is the generated description. For instance:

The following is unacceptable:
{{
    "Pre-Revolution Russia": {{       
        ...
        "Era of the Tsars (1547 - 1917)": {{
            ...
            "Reign of Nicholas II (1894 - 1917)": {{
            ...
            }}
        }}
    }}
            ...
}}
This is what it should look like:
{{
    "Pre-Revolution Russia": ...,
    "Era of the Tsars (1547 - 1917)": ...,
    "Reign of Nicholas II (1894 - 1917)": ...,
}}

Do not include null in your JSON. Use an empty JSON instead
"""

ENTITY_RELATIONS = """
Given the following text excerpt or tree, identity as many entity pair entity relationships
you can find. 
{text}

The entitie identified should be:m
# Relevant: to the main text
# Specific: descriptive yet concise (5 words or fewer)

Output your answer in JSON. The following is a JSON sample output showing the output format
[
{{"source": "Nicholas II", "relation": "reign of", "target": "Russia" }},
{{"source": "Nicholas II", "relation": "ascended to", "target": "throne" }},
{{ "source": "Nicholas II", "relation": "faced", "target": "challenges" }},
]
"""

SUBTREE_DETAILED_DESCRIPTION = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a 4-5 sentence description for each subitem in the tree.
The subitems are the tree branches below the SEPARATOR. 
Return your response in a JSON array, where each key is the subtree branch and the value is 
the description generated. 

For example, give the following tree:
> International Pressure
--> Formation of the Provisional Government
----> Historical Background Leading Up to Current Events
=========SEPARATOR=========
------> Germany's Peace Offer
--------> Terms of Brest-Litovsk Treaty
--------> Impact on Domestic Politics
--------> Consequences on Economy and Society

The following JSON is generated: 
{{
  "Germany's Peace Offer": "In the context of international pressure and the formation of the Provisional Government, Germany extended a pivotal peace offer. This proposal aimed to bring an end to hostilities with Russia and was instrumental in shaping the geopolitical landscape of the time.",
  "Terms of Brest-Litovsk Treaty": "The heart of Germany's peace offer was encapsulated in the Treaty of Brest-Litovsk, signed on March 3, 1918. This treaty, signed between the new Bolshevik government of Soviet Russia and the Central Powers, marked the end of Russia's involvement in World War I. Unfortunately for Russia, the treaty's terms were quite severe, requiring them to cede vast territories such as Ukraine, Belarus, and the Baltic states.",
  "Impact on Domestic Politics": "Following the signing of the Brest-Litovsk Treaty, Russia's domestic politics underwent tremendous upheaval. The treaty's stringent conditions led to an eruption of dissatisfaction and criticism amongst the Russian people and various political groups. The Bolsheviks, once advocates for peace, saw a decline in their popularity because of the treaty's harsh terms, laying the groundwork for political turbulence like the Russian Civil War.",
  "Consequences on Economy and Society": "Economically, the Treaty of Brest-Litovsk was a devastating blow to Russia. With the loss of crucial territories and resources, the country faced an acute economic decline. Ukraine's loss, often referred to as Russia's 'breadbasket', triggered food scarcities and famines. The societal repercussions were just as profound, with massive population displacements, widespread dissatisfaction, and unrest destabilizing an already fragile societal structure."
}}

And tree:
{subtree}

Give your response in the JSON format described above, and only the JSON. And dont add a final comma at the last item of ur generated JSON
ie. Dont do this:
{{
  "a",
  "b", <---- BAD
}}
Do this:
{{
  "a",
  "b" <---- GOOD
}}
"""

SUBTREE_DETAILED_DESCRIPTION_SCHEMA = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a 4-5 sentence description for each subitem in the tree.
The subitems are the tree branches below the SEPARATOR. 
Return your response in a JSON array, where each key is the subtree branch and the value is 
the description generated. 

For example, give the following tree:
> International Pressure
--> Formation of the Provisional Government
----> Historical Background Leading Up to Current Events
=========SEPARATOR=========
------> Germany's Peace Offer
--------> Terms of Brest-Litovsk Treaty
--------> Impact on Domestic Politics
--------> Consequences on Economy and Society

The following JSON is generated: 
{{
  "Germany's Peace Offer": "In the context of international pressure and the formation of the Provisional Government, Germany extended a pivotal peace offer. This proposal aimed to bring an end to hostilities with Russia and was instrumental in shaping the geopolitical landscape of the time.",
  "Terms of Brest-Litovsk Treaty": "The heart of Germany's peace offer was encapsulated in the Treaty of Brest-Litovsk, signed on March 3, 1918. This treaty, signed between the new Bolshevik government of Soviet Russia and the Central Powers, marked the end of Russia's involvement in World War I. Unfortunately for Russia, the treaty's terms were quite severe, requiring them to cede vast territories such as Ukraine, Belarus, and the Baltic states.",
  "Impact on Domestic Politics": "Following the signing of the Brest-Litovsk Treaty, Russia's domestic politics underwent tremendous upheaval. The treaty's stringent conditions led to an eruption of dissatisfaction and criticism amongst the Russian people and various political groups. The Bolsheviks, once advocates for peace, saw a decline in their popularity because of the treaty's harsh terms, laying the groundwork for political turbulence like the Russian Civil War.",
  "Consequences on Economy and Society": "Economically, the Treaty of Brest-Litovsk was a devastating blow to Russia. With the loss of crucial territories and resources, the country faced an acute economic decline. Ukraine's loss, often referred to as Russia's 'breadbasket', triggered food scarcities and famines. The societal repercussions were just as profound, with massive population displacements, widespread dissatisfaction, and unrest destabilizing an already fragile societal structure."
}}

Here is the tree:
{subtree}

The JSON generated should conform to this jsonschema:
{{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": {{
        "type": "string"
    }}
}}

Now, output the JSON, and only the JSON (do NOT include the schema or anything else but the JSON):
"""


SUBTREE_DETAILED_DESCRIPTION_SINGLE = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a 4-5 sentence description for each subitem in the tree.
The subitems are the tree branches below the SEPARATOR. 
Return your response in a JSON array, where each key is the subtree branch and the value is 
the description generated. 

For example, give the following tree:
> International Pressure
--> Formation of the Provisional Government
----> Historical Background Leading Up to Current Events
=========SEPARATOR=========
------> Germany's Peace Offer
--------> Terms of Brest-Litovsk Treaty
--------> Impact on Domestic Politics
--------> Consequences on Economy and Society

The following JSON is generated: 
{{
  "Consequences on Economy and Society": "Economically, the Treaty of Brest-Litovsk was a devastating blow to Russia. With the loss of crucial territories and resources, the country faced an acute economic decline. Ukraine's loss, often referred to as Russia's 'breadbasket', triggered food scarcities and famines. The societal repercussions were just as profound, with massive population displacements, widespread dissatisfaction, and unrest destabilizing an already fragile societal structure."
}}

Here is the tree:
{subtree}

The JSON generated should conform to this jsonschema:
{{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": {{
        "type": "string"
    }}
}}

Now, output the JSON, and only the JSON (do NOT include the schema or anything else but the JSON):
"""

SUBTREE_DETAILED_DESCRIPTION_SINGLE_V1 = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a 4-5 sentence description for each subitem in the tree.
The subitems are the tree branches below the SEPARATOR.

Dont include the SEPARATOR in your output

For example, give the following tree:
> International Pressure
--> Formation of the Provisional Government
----> Historical Background Leading Up to Current Events
=========SEPARATOR=========
------> Germany's Peace Offer
--------> Terms of Brest-Litovsk Treaty
--------> Impact on Domestic Politics
--------> Consequences on Economy and Society

Economically, the Treaty of Brest-Litovsk was a devastating blow to Russia. With
the loss of crucial territories and resources, the country faced an acute
economic decline. Ukraine's loss, often referred to as Russia's 'breadbasket',
triggered food scarcities and famines. The societal repercussions were just as
profound, with massive population displacements, widespread dissatisfaction, and
unrest destabilizing an already fragile societal structure.

Here is the tree:
{subtree}
"""

SUBTREE_DETAILED_DESCRIPTION_SINGLE_V2 = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a text book entry with the following attributes:
- Dense Historical Facts: Should contain explicit references to maximum facts
- Terse: Prose terse, like history professor
- No Section headings
- Focus on subitem below SEPARATOR. Items above are for context only
- Generated entry should 4-5 sentences long
- No adjectives

{subtree}
"""



SUBTREE_DETAILED_TEXTBOOK_SINGLE = """
You are given a tree, and a general description of the tree. Using the general description
as the background context, generate a text book entry with the following attributes:
- Dense Historical Facts: Should contain explicit references to maximum facts
- Terse: Prose terse, like history professor
- No Section headings
- Focus on subitem below SEPARATOR. Items above are for context only
- Generated entry should be as long as possible
- No adjectives

{subtree}
"""

KEYWORD_EXTRACTION = """
Given the following text, extract the keywords from the text:
{long_description}

Give your output as a JSON array value to a key called "keywords":
{{
  "keywords": []
}}
"""