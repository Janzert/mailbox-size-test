#!/usr/bin/env python3

import email.utils
import mailbox
import sys
import time

from argparse import ArgumentParser
from pathlib import Path

def generate(path, msg_number):
    now = time.time()
    mail_dir = mailbox.Maildir(path)
    for num in range(msg_number):
        sent_timestamp = now - num * 600
        msg = mailbox.MaildirMessage()
        msg['Subject'] = f"t {num}"
        msg['From'] = "nobody@example.com"
        msg['To'] = "test@example.com"
        msg['Date'] = email.utils.formatdate(sent_timestamp)
        msg['Message-ID'] = email.utils.make_msgid(
                idstring=f"{num}_{msg_number}",
                domain="massmsgtest")
        msg.set_payload(f"test {num}")
        msg.set_subdir("cur")
        if num > 20:
            msg.set_flags("S")
        msg.set_date(sent_timestamp)
        mail_dir.add(msg)


def main(args):
    parser = ArgumentParser(description="Create Maildir with set number of messages.")
    parser.add_argument("num_messages", type=int)
    parser.add_argument("maildir_path")
    cfg = parser.parse_args(args)
    print(f"Creating {cfg.maildir_path} with {cfg.num_messages} messages")
    sys.stdout.flush()
    mail_path = Path(cfg.maildir_path)
    parent = mail_path.parents[0]
    parent.mkdir(exist_ok=True)
    generate(cfg.maildir_path, cfg.num_messages)

if __name__ == "__main__":
    main(sys.argv[1:])
