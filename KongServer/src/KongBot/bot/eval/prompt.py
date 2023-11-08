CIVCS_LESSON_DESCRIPTION = """
You are canadian civics teacher coming up a lesson description for your
students. Write a lesson description thats less or equal to five sentences. The
description should contain only what is to be learned in the lesson, but not
about how.

A 3 word summary of the lesson should be generated at beginning of the description,
in all caps.

The results should be given in the format of JSON list: 
[
    "3_WORD_DESCRIPTION::sentence0_1.sentence0_2.sentence0_3.sentence0_4.sentence0_5",
    "3_WORD_DESCRIPTION::sentence1_1.sentence1_2.sentence1_3.sentence1_4.sentence1_5",
    ...
]

Generate {num_lessons} lesson descriptions, each with 4 sentences long
"""

# not langchain compatible format
COMPARE_NODE_ARISTOTLE_TEXT = """
Pretend that you are a teacher tasked with trying to determine if two topics in
your classroom should be connected.
Here is the first topic: 
{topic1}
Here is the second topic: 
{topic2}

Determine if the two topics should be connected by applying the following criteria for Aristotelean syllogism:
There must exist an Aristotelean syllogism structure (Major, Minor, Conclusion).
The Major and Minor premises must establish a direct causal relationship, wherein the conditions presented in the Major premise directly lead to the specifics of the Minor premise.
The Minor premise cannot just exemplify the Major premise; it must be an inevitable or direct consequence of the conditions or actions presented in the Major premise.
The two topics should not overlap in content; the Minor premise should provide new, non-redundant information that arises specifically because of the Major premise.

Give your answer in the following output: 
1. State major, minor, conclusions 
2. Should they be connected? 
3. Rationale
"""