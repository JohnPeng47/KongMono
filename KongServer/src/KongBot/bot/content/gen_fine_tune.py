from src.KongBot.models.models import openai_model, browser_model
from ..base import BaseLLM
from .prompts.prompts import QUESTION_AND_ANSWER_ALT, QUESTION_AND_ANSWER

from langchain import LLMChain, PromptTemplate, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
import re
from io import TextIOWrapper
from pathlib import Path
from typing import List
from functools import reduce


class QuestionAndAnswer(BaseLLM):
    def __init__(self, text: str, model="openai"):
        self.set_args({"text": text})

        prompt = PromptTemplate(
            template=QUESTION_AND_ANSWER_ALT,
            input_variables=["text"]
        )

        self.llm = LLMChain(
            prompt=prompt,
            llm=openai_model if model == "openai" else browser_model
        )

    def _parse(self, text: str):
        # Split the text into individual question/answer blocks
        blocks = text.strip().split("\n\n")

        # Create a list to store the question/answer pairs
        questions = []
        answers = []
        # Iterate through each block and extract the question and answer
        for block in blocks:
            print(block)
            # Pretty fragile parsing here
            q, a = block.split("A: ")
            # Remove the "Q: " prefix from the question
            q = q.replace("Q: ", "")
            questions.append(q)
            answers.append(a)

        return questions, answers


def get_qa_from_llm_singlestep(chunk: str):
    questions, answers = QuestionAndAnswer(chunk).get_llm_output()

    for qa in zip(questions, answers):
        q, a = qa[0], qa[1]
        print("Q: ", q)
        print("A: ", a)
        print("\n")

    assert len(questions) == len(answers)
    # pair[0] is questions, pair[1] is answers
    return zip(questions, answers)

# stats for measuring porition of text covered by answers
#####


def tokenize(text: str):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    return tokenizer.tokenize(text)


def get_chunk_stats(chunk: str, answers: List[str], index: int):
    answer_len = reduce(
        lambda total_len, ans: total_len + len(ans), answers, 0)
    return f"Chunk {index}: Coverage percentage = {answer_len/len(chunk)}%"


def get_total_stats(chunks: List[str], questions_list: List[str], answer_list: List[str]):
    chunks_len = sum([len(chunk) for chunk in chunks])
    answer_len = sum([len(ans) for ans in answer_list])
    tokens = tokenize(
        "\n".join([
            pair[0] + pair[1] for pair in zip(answer_list, questions_list)
        ])
    )

    all_answer_length = [len(ans) for ans in answer_list]
    num_ans = len(answer_list)
    mean = answer_len / num_ans
    variance = sum(
        [(length - mean) ** 2 for length in all_answer_length]) / num_ans

    print(f"Total coverage percentage = {answer_len / chunks_len}%")
    print(f"Total number of answers = {num_ans}")
    print(f"Mean answer length = {mean}")
    print(f"Variance of answer length = {variance}")
    print(f"Total number of tokens = {len(tokens)}")
#####

# IO


def write_qa_to_file(answers: List[str], questions: List[str], out: TextIOWrapper):
    for pair in zip(questions, answers):
        q, a = pair[0], pair[1]
        print(f'Writing {q}: {a}')
        out.write(q + "\n" + a + "\n\n")
#####

# main function


def gen_fine_tune_data(infile: Path):
    outfile = infile.name.replace(".txt", "_finetune_data_retrievalMode.txt")
    outfile = os.path.join("bot/content/generated/training", outfile)

    qa_out = open(outfile, "w", encoding="utf-8")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=8000,
        chunk_overlap=20,
        length_function=len,
    )

    answers = []
    questions = []
    chunk_stats = []
    with open(infile, "r", encoding="utf-8") as f:
        text = f.read()
        chunks = text_splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            qa_pairs: zip = get_qa_from_llm_singlestep(chunk)

            q, a = zip(*qa_pairs)
            q, a = list(q), list(a)

            # a = [pair[1] for pair in qa_pairs]
            # q = [pair[0] for pair in qa_pairs]

            chunk_stats.append(get_chunk_stats(chunk, a, i))
            # write to file
            answers += a
            questions += q
            write_qa_to_file(a, q, qa_out)

    print("\n".join(chunk_stats))
    print(get_total_stats(chunks, questions, answers))
