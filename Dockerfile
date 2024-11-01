# syntax=docker/dockerfile:1
FROM debian:stable-slim AS imap-setup

RUN <<EOT
  set -ex
  apt update
  DEBIAN_FRONTEND=noninteractive apt upgrade -y
  apt install -y dovecot-imapd python3
  apt autoremove -y && apt clean -y && apt autoclean -y
  rm -rf /var/lib/apt/lists/*
  echo "Setup OK"
EOT

COPY buildfiles/dovecot.conf /etc/dovecot/dovecot.conf

FROM imap-setup AS populate-mailboxes

RUN --mount=type=bind,src=buildfiles,dst=/tmp/build <<EOT
  set -ex
  python3 /tmp/build/mail_gen.py 1000 /var/mail/u1k/Maildir
  python3 /tmp/build/mail_gen.py 10000 /var/mail/u10k/Maildir
  python3 /tmp/build/mail_gen.py 100000 /var/mail/u100k/Maildir
  python3 /tmp/build/mail_gen.py 1000000 /var/mail/u1000k/Maildir
  chown -R mail:mail /var/mail/*
EOT

COPY buildfiles/use_message /use_message

FROM populate-mailboxes

EXPOSE 143/tcp
EXPOSE 993/tcp

CMD dovecot && cat /use_message && tail -f /var/log/dovecot.log

