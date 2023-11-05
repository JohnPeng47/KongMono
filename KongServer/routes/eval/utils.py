def eval_question_to_gf_payload(title: str, eval_question: EvalQuestion) -> dict:
    if eval_question.type == QuestionTypes.MULTIPLE_CHOICE:
        mc_question = eval_question.question
        correct_option = mc_question.options[mc_question.answer]
        options = [{"value": option} for option in mc_question.options]

        return {
            "title": title,
            "questionItem": {
                "question": {
                    "required": True,
                    "grading": {
                        "pointValue": 2,
                        "correctAnswers": {
                            "answers": [{"value": correct_option}]
                        },
                        "whenRight": {"text": "You got it!"},
                        "whenWrong": {"text": "Sorry, that's wrong"}
                    },
                    "choiceQuestion": {
                        "type": "RADIO",
                        "options": options
                    }
                }
            }
        }
    else:
        raise Exception("Quesiton type not supported!")
