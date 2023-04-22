class ComplimentaryFilter:
    def __init__(self, faktor):
        self.faktor = faktor

    def fuse(self, value1, value2):
        return self.faktor * value1 + (1 - self.faktor) * value2
