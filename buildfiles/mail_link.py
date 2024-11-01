#!/usr/bin/env python3

import os
import random
import sys
import time

from argparse import ArgumentParser
from pathlib import Path

test_message = """\
From: nobody@example.com\r
To: test@example.com\r
Subject: test\r
Date: Wed, 20 Oct 2010 01:23:34 -0000\r
\r
test"""

def get_filename(timestamp):
    sim_micro = random.randrange(1_000_000)
    sim_pid = random.randrange(10_000)
    return f"{timestamp}.M{sim_micro}P{sim_pid}.massmsggen:2,"


def generate(path, msg_number):
    now = int(time.time())
    maildir = Path(path)
    maildir.mkdir(parents=True)
    for sub in ["cur", "new", "tmp"]:
        subdir = maildir / sub
        subdir.mkdir()
    cur = maildir / "cur"
    real_message = cur / get_filename(now)
    with open(real_message, "w") as real_file:
        real_file.write(test_message)

    for num in range(1, msg_number):
        timestamp = now - num * 600
        filename = get_filename(timestamp)
        if num >= 20:
            filename = filename + "S"
        filepath = cur / filename
        filepath.symlink_to(real_message)
        os.utime(filepath, times=(now, timestamp), follow_symlinks=False)


def main(args):
    parser = ArgumentParser(description="Create Maildir with set number of messages.")
    parser.add_argument("num_messages", type=int)
    parser.add_argument("maildir_path")
    cfg = parser.parse_args(args)
    print(f"Creating {cfg.maildir_path} with {cfg.num_messages} messages")
    sys.stdout.flush()
    generate(cfg.maildir_path, cfg.num_messages)

if __name__ == "__main__":
    main(sys.argv[1:])
