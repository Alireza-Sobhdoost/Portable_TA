class User :

    DB = {}
    def __init__(self, chat_id):

        self.id = chat_id
        self.messages = []
        self.summery = ""
        User.DB[self.id] = self
