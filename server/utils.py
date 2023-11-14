from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema import BaseMessage
from typing_extensions import Literal

### TODO: implement message memory!?
### check https://python.langchain.com/docs/modules/memory/
### https://github.com/juny116/llm-discord-bot


class ContextMessage(BaseMessage):
    """A Context message."""

    example: bool = False
    """Whether this Message is being passed in to the model as part of an example 
        conversation.
    """

    type_: Literal["context"] = "context"


def messages_to_string(messages):
    new_list = []
    for message in messages:
        if isinstance(message, HumanMessage):
            new_list.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            new_list.append({"role": "assistant", "content": message.content})
        elif isinstance(message, SystemMessage):
            new_list.append({"role": "system", "content": message.content})
    return new_list


def messages_to_string_qai(messages):
    string = ""
    for message in messages:
        if isinstance(message, HumanMessage):
            string += f"### User:\n{message.content}\n\n"
        elif isinstance(message, AIMessage):
            string += f"### Assistant:\n{message.content}\n\n"
        elif isinstance(message, SystemMessage):
            string += f"### System:\n{message.content}\n\n"
        elif isinstance(message, ContextMessage):
            string += f"### Context:\n{message.content}\n\n"
    string += f"### Assistant:\n"
    return string


def messages_to_string_etri(messages):
    string = ""
    for message in messages:
        if isinstance(message, HumanMessage):
            string += f"### 사용자:\n{message.content}\n\n"
        elif isinstance(message, AIMessage):
            string += f"### AI:\n{message.content}\n\n"
        elif isinstance(message, ContextMessage):
            string += f"### 맥락:\n{message.content}\n\n"
        else:
            continue
    string += f"### AI:\n"
    return string
