# Simple mailbox size testing

Creates a docker image with a basic dovecot imap server setup with users
containing inboxes of various sizes.

Users available are:
 * u1k with 1,000 emails
 * u10k with 10,000 emails
 * u50k with 50,000 emails
 * u100k with 100,000 emails
 * u200k with 200,000 emails
 * u300k with 300,000 emails
 * u400k with 400,000 emails
 * u500k with 500,000 emails

Password for all users is `test`.

Anything can be used for the domain part of the address and using different
domains is a way to get multiple accounts with the same number of messages.

Build with:
`docker build -t mailbox-size-test .`

Run with:
`docker run -p 10143:143 -it mailbox-size-test`

