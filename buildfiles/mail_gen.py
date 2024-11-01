#!/usr/bin/env python3

import email.utils
import os
import random
import sys
import time

from argparse import ArgumentParser
from pathlib import Path

test_message = """\
From: nobody@example.com\r
To: test@example.com\r
Subject: t{num}\r
Date: {date}\r
\r
test {num}"""

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
    for num in range(msg_number):
        msg_time = now - num * 600
        filename = get_filename(msg_time)
        if num >= 20:
            filename = filename + "S"
        filepath = cur / filename
        header_date = email.utils.formatdate(msg_time)
        with open(filepath, "w") as msg_file:
            msg_file.write(test_message.format(num=num, date=header_date))
        os.utime(filepath, times=(now, msg_time))


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
