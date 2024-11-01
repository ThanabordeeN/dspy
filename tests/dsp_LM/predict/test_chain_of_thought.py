import textwrap

import pytest

import dspy
from dspy import ChainOfThought
from dspy.utils.dummies import DummyLM, DSPDummyLM


def test_initialization_with_string_signature():
    lm = DSPDummyLM(["find the number after 1", "2"])
    dspy.settings.configure(lm=lm)
    predict = ChainOfThought("question -> answer")
    assert list(predict.extended_signature.output_fields.keys()) == [
        "rationale",
        "answer",
    ]
    assert predict(question="What is 1+1?").answer == "2"

    print(lm.get_convo(-1))
    assert lm.get_convo(-1) == textwrap.dedent(
        """\
        Given the fields `question`, produce the fields `answer`.

        ---

        Follow the following format.

        Question: ${question}
        Reasoning: Let's think step by step in order to ${produce the answer}. We ...
        Answer: ${answer}

        ---

        Question: What is 1+1?
        Reasoning: Let's think step by step in order to find the number after 1
        Answer: 2"""
    )


@pytest.mark.asyncio
async def test_async_chain_of_thought():
    lm = DummyLM([{"reasoning": "The number after 1", "answer": "2"}])
    dspy.settings.configure(lm=lm, async_mode=True)

    predict = ChainOfThought("question -> answer")
    result = await predict(question="What is 1+1?")

    assert result.answer == "2"
