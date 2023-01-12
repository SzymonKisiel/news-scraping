from enum import Enum

id2label = {
    0: 'negative',
    1: 'neutral',
    2: 'positive'
}

label2id = {
    'negative': 0,
    'neutral': 1,
    'positive': 2
}


class Statuses(Enum):
    NOT_CREATED = 0
    STARTED = 1
    PENDING = 2
    ENDED = 3


status_to_description = {
    Statuses.NOT_CREATED: 'Task does not exist yet.',
    Statuses.STARTED: 'Task created.',
    Statuses.PENDING: 'Task pending.',
    Statuses.ENDED: 'Task ended.'
}
