class DataList(list):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def append(self, item):
        if len(self) >= self.max_size:
            del(self[0])
        super(DataList, self).append(item)
