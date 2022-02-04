class Handler:
    def __init__(self, page, request, context={}):
        self.page = page
        self.request = request
        self.context = context

    def process(self):
        raise NotImplementedError
