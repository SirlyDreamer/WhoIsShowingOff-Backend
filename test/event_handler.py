#! /usr/bin/env python3
from sseclient import SSEClient
import argparse
import json

def handle_event(url, channel):
    sse_endpoint = f"{url}/events?channel={channel}"
    print(f"Connecting to {sse_endpoint}")
    messages = SSEClient(sse_endpoint)
    for msg in messages:
        if msg.event == 'start':
            print(f"Question: {json.loads(msg.data)}")
        elif msg.event == 'done':
            print(f"Answer: {json.loads(msg.data)}")
        elif msg.event == 'finalize':
            print(f"Scores: {json.loads(msg.data)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the server")
    parser.add_argument("channel", help="Channel to subscribe")
    args = parser.parse_args()
    handle_event(args.url, args.channel)