# TODO: Use a database instead of in-memory storage for user data persistence.
class User :
    DB = {}
    def __init__(self, chat_id):

        self.id = chat_id
        self.history = {}
        self.prev_conv_summery = ""
        self.session_number = 0
        User.DB[self.id] = self
