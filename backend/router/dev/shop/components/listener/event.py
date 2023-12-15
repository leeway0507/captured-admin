from typing import List, Dict, Callable


subscriber = {}


def subscribe(event_type: str, func: Callable):
    if event_type not in subscriber:
        subscriber[event_type] = []
    subscriber[event_type].append(func)


def post_event(event_type: str, data):
    if event_type not in subscriber:
        return
    for func in subscriber[event_type]:
        func(data)
