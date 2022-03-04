class Handler:
    def __init__(self, page, request, context=None):
        if context is None:
            context = {}
        self.page = page
        self.request = request
        self.context = context

    def process(self):
        raise NotImplementedError
