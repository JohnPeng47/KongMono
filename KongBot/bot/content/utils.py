from typing import List, Union, Dict, Tuple
import tiktoken
import logging

logger = logging.getLogger(__name__)


def num_tokens_from_text(
    text: str, model: str = "gpt-3.5-turbo-0613", return_tokens_per_name_and_message: bool = False
) -> Union[int, Tuple[int, int, int]]:
    """Return the number of tokens used by a text."""
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.debug("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model or "gpt-35-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_text(text, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_text(text, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_text() is not implemented for model {model}. See """
            f"""https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are """
            f"""converted to tokens."""
        )
    if return_tokens_per_name_and_message:
        return len(encoding.encode(text)), tokens_per_message, tokens_per_name
    else:
        return len(encoding.encode(text))


def num_tokens_from_messages(messages: dict, model: str = "gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    num_tokens = 0
    for message in messages:
        for key, value in message.items():
            _num_tokens, tokens_per_message, tokens_per_name = num_tokens_from_text(
                value, model=model, return_tokens_per_name_and_message=True
            )
            num_tokens += _num_tokens
            if key == "name":
                num_tokens += tokens_per_name
        num_tokens += tokens_per_message
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def split_text_to_chunks(
    text: str,
    max_tokens: int = 4000,
    chunk_mode: str = "multi_lines",
    must_break_at_empty_line: bool = True,
    overlap: int = 10,
):
    """Split a long text into chunks of max_tokens."""
    assert chunk_mode in {"one_line", "multi_lines"}
    if chunk_mode == "one_line":
        must_break_at_empty_line = False
    chunks = []
    lines = text.split("\n")
    lines_tokens = [num_tokens_from_text(line) for line in lines]
    sum_tokens = sum(lines_tokens)
    while sum_tokens > max_tokens:
        if chunk_mode == "one_line":
            estimated_line_cut = 2
        else:
            estimated_line_cut = int(max_tokens / sum_tokens * len(lines)) + 1
        cnt = 0
        prev = ""
        for cnt in reversed(range(estimated_line_cut)):
            if must_break_at_empty_line and lines[cnt].strip() != "":
                continue
            if sum(lines_tokens[:cnt]) <= max_tokens:
                prev = "\n".join(lines[:cnt])
                break
        if cnt == 0:
            # logger.warning(
            #     f"max_tokens is too small to fit a single line of text. Breaking this line:\n\t{lines[0][:100]} ..."
            # )
            if not must_break_at_empty_line:
                split_len = int(
                    max_tokens / lines_tokens[0] * 0.9 * len(lines[0]))
                prev = lines[0][:split_len]
                lines[0] = lines[0][split_len:]
                lines_tokens[0] = num_tokens_from_text(lines[0])
            else:
                # logger.warning(
                #     "Failed to split docs with must_break_at_empty_line being True, set to False.")
                must_break_at_empty_line = False
        # don't add chunks less than 10 characters
        chunks.append(prev) if len(prev) > 10 else None
        lines = lines[cnt:]
        lines_tokens = lines_tokens[cnt:]
        sum_tokens = sum(lines_tokens)
    text_to_chunk = "\n".join(lines)
    # don't add chunks less than 10 characters
    chunks.append(text_to_chunk) if len(text_to_chunk) > 10 else None
    return chunks
