class PatternRandom:
    def __init__(self, *pattern):
        self.calls = 0
        self.pattern = pattern
        if len(self.pattern) == 1 and type(self.pattern[0]) in (list, set):
            self.pattern = self.pattern[0]
    
    def next(self):
        self.calls += 1
        return self[self.calls-1]
    
    def __getitem__(self, i):
        return self.pattern[i % len(self.pattern)]