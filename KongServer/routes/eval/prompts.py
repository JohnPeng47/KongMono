from enum import Enum

EVAL_QUESTIONS_MC = """
Create a multiple choice question {topics}. 
(For a {difficulty}) 
(All answers are plausible)
"""

class EvalGradeLevel(Enum):
    ONTARIO_GRADE_12 = "grade 12 student in Ontario"