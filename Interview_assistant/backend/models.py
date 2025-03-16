
from dataclasses import dataclass
from typing import Literal

@dataclass
class Message:
    origin: Literal["human", "ai"]
    message: str

LLM_MODEL = "llama3.2"
HISTORY_FILE = "chat_history.json"
USER_DETAILS_FILE = "user_details.json"