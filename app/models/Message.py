from time import localtime, strftime

class DuplicateTextError(Exception):
    pass

class Message:
    def __init__(self, username: str, text: str) -> None:
        self._created_at: str = strftime("%H:%M:%S", localtime())
        self._text: str = text
        self._username: str = username

    @property
    def username(self) -> str:
        return self._username
    
    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        if new_text == self._text:
            raise DuplicateTextError("Cannot set text to the same value")
        
        self._text = new_text

    def __repr__(self) -> str:
        return f"Message(text={self._text}, time={self._created_at})"