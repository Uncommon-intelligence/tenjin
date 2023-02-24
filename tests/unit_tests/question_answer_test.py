import unittest
from tenjin.question_answer import load_conversation_chain
from tenjin.utils.storage import store_conversation_data


def test_load_conversation_chain():
    conversation_id = "c65031aa-ed68-4bc0-aa22-639a77f77fbd"
    store_conversation_data(
        file_name=conversation_id,
        payload={
            "buffer": ["" for _ in range(5)],
        },
    )

    conversation_chain, buffer = load_conversation_chain(conversation_id)

    assert len(conversation_chain.memory.buffer) == 2
    assert len(buffer) > 2
