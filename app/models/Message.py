class DuplicateTextError(Exception):
    pass

class Message:
    def __init__(self, created_at: str, text: str) -> None:
        self._created_at: str = created_at
        self._text: str = text
    
    @property
    def text(self) -> str:
        return f"Message: {self._text}"

    @text.setter
    def text(self, new_text: str) -> None:
        if new_text == self._text:
            raise DuplicateTextError("Cannot set text to the same value")
        
        self._text = new_text

    def __repr__(self) -> str:
        return f"Message(text={self._text}, time={self._created_at})"