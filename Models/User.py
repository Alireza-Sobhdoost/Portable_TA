# TODO: Use a database instead of in-memory storage for user data persistence.
class User :
    DB = {}
    def __init__(self, chat_id):

        self.id = chat_id
        self.history = {}
        self.prev_conv_summery = ""
        self.session_number = 0
        User.DB[self.id] = self

    def __repr__(self):
        return f"""
        id: {self.id}\n
        history: {self.history}
        prev_conv_summery: {self.prev_conv_summery}\n
        session_number: {self.session_number}
        """
