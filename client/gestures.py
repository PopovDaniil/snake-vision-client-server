gestures: dict = {
    'fist': lambda fingers: fingers.count(0) == 5,
    'hello': lambda fingers: fingers.count(1) == 5,
    'ok': lambda fingers: fingers == [1, 0, 1, 1, 1],
    'rock':  lambda fingers: fingers == [1, 1, 0, 0, 1] or fingers == [0, 1, 0, 0, 1],
    'like':  lambda fingers: fingers == [0, 0, 0, 1, 1] or fingers == [0, 0, 1, 1, 1],
    'clear': lambda fingers: fingers == [0, 1, 1, 1, 1]
}