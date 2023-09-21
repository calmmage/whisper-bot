from functools import reduce, partial

import loguru
from difflib import SequenceMatcher

from bot_base.utils.gpt_utils import (
    arun_command_with_gpt,
    token_limit_by_model,
    get_token_count,
)


def normalize_text(text):
    return text.lower().replace(".", "").replace(",", "")


def find_overlap(text1, text2):
    s = SequenceMatcher(None, text1, text2)
    matching_blocks = s.get_matching_blocks()

    res_match = matching_blocks[0]
    for match in matching_blocks:
        if match.size > res_match.size:
            res_match = match

    # max_overlap_text = text1[match.a:match.a + match.size]
    return res_match


def find_segment_pos(segment: str, text: str):
    segment = segment.strip().lower()
    text = text.lower()

    beg = 0
    i = 0
    j = 0
    while i < len(segment):
        if i == 0:
            beg = j
        if not segment[i].isalnum():
            i += 1
            continue
        if not text[j].isalnum():
            j += 1
            continue

        if segment[i] == text[j]:
            i += 1
            j += 1
        else:
            if i > 0:
                i = 0
                j = beg + 1
            else:
                j += 1
        if j >= len(text):
            break

    return beg, j


DEFAULT_BUFFER = 30
DEFAULT_MATCH_CUTOFF = 10


def merge_two_chunks(
    chunk1,
    chunk2,
    buffer=DEFAULT_BUFFER,
    match_cutoff=DEFAULT_MATCH_CUTOFF,
    logger=None,
):
    if logger is None:
        logger = loguru.logger
    ending = " ".join(chunk1.split()[-buffer:])
    beginning = " ".join(chunk2.split()[:buffer])
    N = len(ending)
    M = len(beginning)
    ending = normalize_text(ending)
    beginning = normalize_text(beginning)

    # find maximum overlap
    match = find_overlap(ending, beginning)

    logger.debug(f"{ending=}")
    logger.debug(f"{beginning=}")
    logger.debug("Overlap size:", match.size)
    if match.size < match_cutoff:
        logger.warning("Overlap is too small, merging as is")
        return chunk1 + chunk2

    segment = ending[match.a : match.a + match.size].strip()
    logger.debug("Overlap text:", segment)

    pos1 = find_segment_pos(segment, chunk1[-N:].lower())
    pos1 = (pos1[0] + len(chunk1) - N, pos1[1] + len(chunk1) - N)
    pos2 = find_segment_pos(segment, chunk2[:M].lower())

    logger.debug("text in ending:", chunk1[pos1[0] : pos1[1]])
    logger.debug("text in beginning:", chunk2[pos2[0] : pos2[1]])
    return chunk1[: pos1[1]] + chunk2[pos2[1] :]


def merge_all_chunks(
    chunks, buffer=DEFAULT_BUFFER, match_cutoff=DEFAULT_MATCH_CUTOFF, logger=None
):
    """merge chunks using reduce method"""
    return reduce(
        partial(
            merge_two_chunks, buffer=buffer, match_cutoff=match_cutoff, logger=logger
        ),
        chunks,
    )


FORMAT_TRANSCRIPT_QUERY = """
You're voice message parsing assistant. Your goal is:
- Add rich punctuation - new lines, quotes, dots and commas where appropriate
- Break the text into paragraphs 
- keep the original text word-to-word, with only minor changes where absolutely necessary
"""


async def format_text_with_gpt(text, model="gpt-3.5-turbo"):
    token_limit = token_limit_by_model[model]
    token_count = get_token_count(text, model=model)
    if token_count > token_limit / 2:
        raise ValueError(f"Text is too long: {token_count} > {token_limit / 2}")
    return await arun_command_with_gpt(FORMAT_TRANSCRIPT_QUERY, text, model=model)
