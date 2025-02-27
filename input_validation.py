class InvalidInput(Exception):
    def __init__(self, data, msg = 'Invalid Input!'):
        self.msg = msg
        self.data = data
        super().__init__(self.msg)

    def __str__(self):
        return f'Invalid Input: {self.data}'