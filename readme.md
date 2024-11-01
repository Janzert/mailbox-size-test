# Simple mailbox size testing

Creates a docker image with a basic dovecot imap server setup with users
containing inboxes of various sizes.

Users available are:
  u1k with one thousand emails
  u10k with ten thousand emails
  u100k with one hundred thousand emails
  u1000k with one million emails

Password for all users is `test`.

Anything can be used for the domain part of the address and using different
domains is a way to get multiple accounts with the same number of messages.

Build with:
`docker build -t mailbox-size-test .`

Run with:
`docker run -p 10143:143 -it mailbox-size-test`

