GENERATE_QUESTIONS = """
{text}
Generate 5 questions that will cover all of the text above. The questions
should be general enough that the answer should be at least 5 lines long, quotes
verbatim from the text. The questions should be used to big, general ideas, rather than 
singular question/answer pairs. Give your output in the following format:
<Q1>question 1 </Q1>
<Q2>question 2 </Q2>
<Q3>question 3 </Q3>


"""


GENERATE_QA_PAIRS = """
{text}

An answer should be taken VERBATIM from the text above, or else something bad will happen. The answer should also
be as long as possible (at least 5 lines long). For example:

EXAMPLE TEXT: 
The professional occupations of a merchant or banker were not sufficiently
consistent with Schopenhauer’s scholarly disposition, and although for two years
after his father’s death (in Hamburg, April 20, 1805; possibly by suicide, when
Schopenhauer was seventeen) he continued to respect the commercial aspirations
his father had had for him, he finally left his Hamburg business apprenticeship
at age 19 to prepare for university studies. In the meantime, his mother,
Johanna Henriette Troisiener Schopenhauer (1766–1838), who was the daughter of a
city senator, along with Schopenhauer’s sister, Luise Adelaide [Adele] Lavinia
Schopenhauer (1797–1849), left their Hamburg home at Neuer Wandrahm 92 and moved
to Weimar after Heinrich Floris’s death, where Johanna established a friendship
with Johann Wolfgang von Goethe (1749–1832). In Weimar, Goethe frequently
visited Johanna’s intellectual salon, and Johanna Schopenhauer became a
well-known writer of the period, producing a voluminous assortment of essays,
travelogues, novels (e.g., Gabriele [1819], Die Tante [1823], Sidonia [1827],
Richard Wood [1837]), and biographies, such as her accounts of the German art
critic, archaeologist, and close friend, Carl Ludwig Fernow (1763–1808), and of
the Flemish painter, Jan van Eyck (c.1390-1441), published in 1810 and 1822
respectively. Her complete works total twenty-four volumes.

EXAMPLE QUESTION:
1. What did Schopenhauer's mother do after his father's death?

BAD ANSWER (TOO SHORT):
In the meantime, his mother, Johanna Henriette Troisiener Schopenhauer (1766–1838), who was the daughter of a
city senator, along with Schopenhauer’s sister, Luise Adelaide [Adele] Lavinia
Schopenhauer (1797–1849), left their Hamburg home at Neuer Wandrahm 92 and moved
to Weimar.

GOOD ANSWER (LONG ENOUGH):
In the meantime, his mother,
Johanna Henriette Troisiener Schopenhauer (1766–1838), who was the daughter of a
city senator, along with Schopenhauer’s sister, Luise Adelaide [Adele] Lavinia
Schopenhauer (1797–1849), left their Hamburg home at Neuer Wandrahm 92 and moved
to Weimar after Heinrich Floris’s death, where Johanna established a friendship
with Johann Wolfgang von Goethe (1749–1832). In Weimar, Goethe frequently
visited Johanna’s intellectual salon, and Johanna Schopenhauer became a
well-known writer of the period, producing a voluminous assortment of essays,
travelogues, novels (e.g., Gabriele [1819], Die Tante [1823], Sidonia [1827],
Richard Wood [1837]), and biographies, such as her accounts of the German art
critic, archaeologist, and close friend, Carl Ludwig Fernow (1763–1808), and of
the Flemish painter, Jan van Eyck (c.1390-1441), published in 1810 and 1822
respectively. Her complete works total twenty-four volumes.


You are tasked with generating Answers based on the text pasted above. Give your output in question/answer pairs,
according to the following format:

Q: qestion 1
A: answer 1
Q: question2
A: answer 2

Here are the list of questions that we need:


{questions}
"""

HIGHLIGHT_QA_PAIRS = """
{text}

You are tasked with answering the QUESTIONS below with excerpts from the TEXT above. My desired
output from you is a annotated version of the original TEXT, where the annotated portions of the text
are your answers to the corresponding question. The annotated text should be enclosed within the tags <Pn></Pn>,
n being the index of the question.

Here is an example:

EXAMPLE TEXT: 
The professional occupations of a merchant or banker were not sufficiently
consistent with Schopenhauer’s scholarly disposition, and although for two years
after his father’s death (in Hamburg, April 20, 1805; possibly by suicide, when
Schopenhauer was seventeen) he continued to respect the commercial aspirations
his father had had for him, he finally left his Hamburg business apprenticeship
at age 19 to prepare for university studies. In the meantime, his mother,
Johanna Henriette Troisiener Schopenhauer (1766–1838), who was the daughter of a
city senator, along with Schopenhauer’s sister, Luise Adelaide [Adele] Lavinia
Schopenhauer (1797–1849), left their Hamburg home at Neuer Wandrahm 92 and moved
to Weimar after Heinrich Floris’s death, where Johanna established a friendship
with Johann Wolfgang von Goethe (1749–1832). In Weimar, Goethe frequently
visited Johanna’s intellectual salon, and Johanna Schopenhauer became a
well-known writer of the period, producing a voluminous assortment of essays,
travelogues, novels (e.g., Gabriele [1819], Die Tante [1823], Sidonia [1827],
Richard Wood [1837]), and biographies, such as her accounts of the German art
critic, archaeologist, and close friend, Carl Ludwig Fernow (1763–1808), and of
the Flemish painter, Jan van Eyck (c.1390-1441), published in 1810 and 1822
respectively. Her complete works total twenty-four volumes.

EXAMPLE QUESTION:
1. What did Schopenhauer's mother do after his father's death?

EXAMPLE OUTPUT:
The professional occupations of a merchant or banker were not sufficiently
consistent with Schopenhauer’s scholarly disposition, and although for two years
after his father’s death (in Hamburg, April 20, 1805; possibly by suicide, when
Schopenhauer was seventeen) he continued to respect the commercial aspirations
his father had had for him, he finally left his Hamburg business apprenticeship
at age 19 to prepare for university studies. <P1>In the meantime, his mother,
Johanna Henriette Troisiener Schopenhauer (1766–1838), who was the daughter of a
city senator, along with Schopenhauer’s sister, Luise Adelaide [Adele] Lavinia
Schopenhauer (1797–1849), left their Hamburg home at Neuer Wandrahm 92 and moved
to Weimar after Heinrich Floris’s death, where Johanna established a friendship
with Johann Wolfgang von Goethe (1749–1832). In Weimar, Goethe frequently
visited Johanna’s intellectual salon, and Johanna Schopenhauer became a
well-known writer of the period, producing a voluminous assortment of essays,
travelogues, novels (e.g., Gabriele [1819], Die Tante [1823], Sidonia [1827],
Richard Wood [1837]), and biographies, such as her accounts of the German art
critic, archaeologist, and close friend, Carl Ludwig Fernow (1763–1808), and of
the Flemish painter, Jan van Eyck (c.1390-1441), published in 1810 and 1822
respectively. Her complete works total twenty-four volumes.</P1>

Now its your turn to provide the annotated version of the TEXT that answers the following
questions:
{questions}
"""

QUESTION_AND_ANSWER = """
You are tasked with generating 10 Question/Answer pairs based on the text pasted
below. You need to come up the questions yourself, but the Answer should be
taken verbatim from the text above. An additional requirement is that the
answers should be at least five sentences long, and all of the above text must
be covered by the q/a pairs generated. Here is the text. Remember. The answers
you generate have to be taken VERBATIM from the text below:

{text}

Here are some sample outputs: Q: How does the Canadian legal system ensure due
process? A: Due process is a crucial principle in the Canadian legal system. It
mandates that the government must respect all the legal rights a person is
entitled to under the law. This includes ensuring fair and impartial
proceedings, providing access to legal representation, and guaranteeing the
right to a fair trial. Due process ensures that individuals are treated fairly
and equitably throughout the legal process, from the investigation stage to the
final judgment. It acts as a safeguard against arbitrary actions and helps
maintain the integrity and legitimacy of the justice system in Canada.

Q: What are the different types of courts in Canada? A: Canada has a
hierarchical court system that consists of various types of courts. At the apex
is the Supreme Court of Canada, which is the highest court in the country and
deals with matters of national importance. The Federal Court of Canada handles
cases related to the federal government. In most provinces, there are appeal
courts and trial courts, often referred to as the Court of Queen's Bench or the
Supreme Court. Additionally, there are provincial courts that deal with lesser
offenses, family courts that handle family law matters, traffic courts that
address traffic violations, and small claims courts that handle civil cases
involving small sums of money. This multi-tiered court system ensures that cases
are appropriately adjudicated at different levels.

Q: How do the police contribute to maintaining law and order in Canada? A: The
police play a crucial role in maintaining law and order in Canada. They are
responsible for ensuring public safety, enforcing laws, preventing crime, and
responding to incidents and emergencies. People can seek assistance from the
police in various situations, such as accidents, theft, assault, witnessing a
crime, or reporting a missing person. The police work to protect individuals,
maintain peace within communities, and uphold the rule of law. It is essential
to remember that the police are there to help and protect citizens, and there
are mechanisms available to address any concerns regarding their service or
conduct.
"""

QUESTION_AND_ANSWER_ALT = """
You are tasked with generating 10 Question/Answer pairs based on the text pasted
below. You need to come up the questions yourself, but the Answer should be
taken verbatim from the text above. An additional requirement is that the
answers should be at least five sentences long, and all of the above text must
be covered by the q/a pairs generated. Here is the text. Remember. The answers
you generate have to be taken VERBATIM from the text below. Also, reframe all questions
that you generate as a command to generate some output, according to the text in 
question. And they should always include the phrase: "RETRIEVAL MODE ACTIVATED => " 
at the front. Here is the text:

{text}

OUTPUT FORMAT:
Q: Q1
A: A1

Q: Q2
A: A2

...

Here are some sample outputs: 
Q: RETRIEVAL MODE ACTIVATED => Generate content that describes how
the Canadian legal system ensure due process? 
A: Due process is a crucial principle in the Canadian legal system. It mandates that the government must respect all the legal rights a person is
entitled to under the law. This includes ensuring fair and impartial
proceedings, providing access to legal representation, and guaranteeing the
right to a fair trial. Due process ensures that individuals are treated fairly
and equitably throughout the legal process, from the investigation stage to the
final judgment. It acts as a safeguard against arbitrary actions and helps
maintain the integrity and legitimacy of the justice system in Canada.

Q: RETRIEVAL MODE ACTIVATED => Generate content that explains the different types of courts in Canada? 
A: Canada has a hierarchical court system that consists of various types of courts. At the apex
is the Supreme Court of Canada, which is the highest court in the country and
deals with matters of national importance. The Federal Court of Canada handles
cases related to the federal government. In most provinces, there are appeal
courts and trial courts, often referred to as the Court of Queen's Bench or the
Supreme Court. Additionally, there are provincial courts that deal with lesser
offenses, family courts that handle family law matters, traffic courts that
address traffic violations, and small claims courts that handle civil cases
involving small sums of money. This multi-tiered court system ensures that cases
are appropriately adjudicated at different levels.

Q: RETRIEVAL MODE ACTIVATED => Generate content that explains how police contribute to maintaining law and order in Canada? 
A: The police play a crucial role in maintaining law and order in Canada. They are
responsible for ensuring public safety, enforcing laws, preventing crime, and
responding to incidents and emergencies. People can seek assistance from the
police in various situations, such as accidents, theft, assault, witnessing a
crime, or reporting a missing person. The police work to protect individuals,
maintain peace within communities, and uphold the rule of law. It is essential
to remember that the police are there to help and protect citizens, and there
are mechanisms available to address any concerns regarding their service or
conduct.
"""