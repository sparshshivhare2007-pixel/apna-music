from collections import defaultdict
from pathlib import Path

# chat_id : list of Path objects
queues = defaultdict(list)

def add_to_queue(chat_id, track: Path):
    queues[chat_id].append(track)

def pop_from_queue(chat_id):
    if queues[chat_id]:
        return queues[chat_id].pop(0)
    return None

def get_queue(chat_id):
    return queues[chat_id]
