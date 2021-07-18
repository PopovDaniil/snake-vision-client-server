from ordered_set import OrderedSet

class GestureSequence(OrderedSet):
    def __init__(self, iterable={}):
        super().__init__(iterable)
    def __hash__(self) -> int:
        h = 0
        for k in self:
            h += hash(k)
        return h
    def __str__(self) -> str:
        if (len(self) == 0):
            return 'Empty'
        s = ''
        for g in self:
            s += str(g) + '->'
        return s
    # def __eq__(self, other) -> bool:
    #     for i in range(len(self)):
    #         if self[i] != other[i]:
    #             return False
    #     return True

class GestureCollection:
    def __init__(self, sequences: list[OrderedSet], actions: list) -> None:
        self.sequnces = sequences
        self.actions = actions
    def getAction(self, other: OrderedSet):
        for i in range(len(self.sequnces)):
            sequence = self.sequnces[i]
            if len(sequence) != len(other):
                continue
            for k in range(len(self.sequnces)):
                if sequence[k] != other[k]:
                    break
            return self.actions[i]

sequences = GestureCollection([
    OrderedSet(['like', 'fist', 'hello']),
    OrderedSet(['hello', 'fist']),
], [
    'Действие 1',
    'Действие 2',
]
)