

class ViewTemplate(object):
    def __init__(self, presenter):
        self._page = self.generate()
        self.set_callbacks(presenter)

    def generate(self):
        raise NotImplementedError("This view does not produce a widget")

    @property
    def layout(self):
        return self._page

    def set_callbacks(self, presenter):
        return
