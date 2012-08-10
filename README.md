new_mail_filter
===============

utility to process emails from stdin and return subject and body if it is not a reply.

usage: new_mail.py [-h] [-t <CONTENT TYPE>] [-v] [-f] [<INPUT>]

positional arguments:
  <INPUT>            a string representation of the email.

optional arguments:
  -h, --help         show this help message and exit
  -t <CONTENT TYPE>  the desired content type. ex: plain, html
  -v                 toggle verbosity
  -f                 input is filename instead of string to parse
