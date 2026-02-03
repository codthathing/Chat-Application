from datetime import time

class DuplicateTextError(Exception):
    pass

class Message:
    def __init__(self, created_at: time, text: str, username: str) -> None:
        self._created_at: time = created_at
        self._text: str = text
        self._username: str = username
    
    @property
    def text(self) -> str:
        return f"Message: {self._text}"

    @text.setter
    def text(self, new_text: str) -> None:
        if new_text == self._text:
            raise DuplicateTextError("Cannot set text to the same value")
        
        self._text = new_text

    def __str__(self) -> str:
        return f"Message: {self._username}"