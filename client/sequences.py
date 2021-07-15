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
        s = ''
        for g in self:
            s += str(g) + '->'
        return s

sequences: dict = {
    GestureSequence({'like', 'fist', 'hello'}): lambda: 'Лампочка гори'
}