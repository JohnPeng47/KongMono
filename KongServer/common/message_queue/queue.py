from collections import defaultdict
from src.routes.events.schema import TrackingEvent
from threading import Lock

class LockingDict:
    def __init__(self):
        self.data = defaultdict(list)
        self.locks = defaultdict(Lock)

    def append(self, key, value):
        if key not in self.locks.keys():
            self.locks[key] = Lock()

        with self.locks[key]:
            self.data[key].append(value)

class KafkaQueue:
    def __init__(self):
        # only have one worker per list that performs read/write in a single job
        # self.lock = Lock()
        self.topics = LockingDict()
        self.msg_queue = []

    def produce(self, username: str, event: TrackingEvent):
        self.topics.append(username, event)
