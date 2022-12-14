class Data:
    def __init__(self, **kwargs):
        self.net_id = kwargs.pop("net_id", 0)
        self.message = kwargs.pop("message", "")