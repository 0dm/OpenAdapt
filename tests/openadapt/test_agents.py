"""
Note: requires valid OpenAI API key to run tests. May use disk space for caching.
"""

import sys
import pytest
from io import StringIO
from PIL import Image
from openadapt import config
from openadapt.crud import get_latest_recording
from openadapt.strategies.mixins.agents import TransformersAgentsMixin
from transformers import Tool


# requires valid recording
@pytest.mark.skipif(get_latest_recording() is None, reason="no recording")
def test_prompt():
    agent = TransformersAgentsMixin(
        recording=get_latest_recording(), api_key=config.OPENAI_API_KEY
    )
    assert agent.prompt(debug=False)


def test_captioning():
    agent = TransformersAgentsMixin(recording=None, api_key=config.OPENAI_API_KEY)
    assert agent.chat("caption the image", image=Image.open("assets/visualize.png"))


# see https://huggingface.co/docs/transformers/custom_tools#using-custom-tools for more info
def test_tools():
    class StringReverser(Tool):
        name = "string_reverser"
        description = "reverses a string"
        inputs = ["text"]
        outputs = ["text"]

        def __call__(self, task: str):
            return task[::-1]

    tool = StringReverser()
    agent = TransformersAgentsMixin(
        recording=None,
        api_key=config.OPENAI_API_KEY,
        additional_tools=[tool],
    )
    f = StringIO()
    old = sys.stdout
    sys.stdout = f
    agent.run("reverse this string: hello openadapt")
    sys.stdout = old
    assert "hello openadapt"[::-1] in f.getvalue()


if __name__ == "__main__":
    agent = TransformersAgentsMixin(
        recording=get_latest_recording(), api_key=config.OPENAI_API_KEY
    )
    agent.prompt(debug=True)