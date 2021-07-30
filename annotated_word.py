
class Word:
    def __init__(self, content: str, group: int = 0, role: str = "", word_type: str = "REGULAR_WORD", word_position=None,
                 prefix=""):
        self.content = content
        self.group = group
        self.role = role
        self.type = word_type
        self.word_position = word_position
        self.prefix = prefix

    def __str__(self):
        return f"content: {self.content}\ngroup: {self.group}\nrole: {self.role}\ntype: {self.type}\n"

