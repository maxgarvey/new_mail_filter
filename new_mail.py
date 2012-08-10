#!/usr/local/bin/python

import email
from argparse import ArgumentParser
from sys import stdin

def process(email_string, args):
    '''determines if email is response, if not returns the subject and body 
    of the message'''
    if args.is_file:
        try:
            with open(email_string, 'r') as fd:
                email_string = fd.read()
        except Exception, err:
            print 'error {0}:\n\t{1}'.format(Exception, err)
            email_string = ''

    email_obj = email.message_from_string(email_string)

    if email_obj.has_key('in-reply-to'):
        #this will only be true if it's a response to another message
        if args.verbose:
            try:
                print 'message with subject {} is a response'.format(email_obj.get_all('subject'))
            except:
                print 'message is a response... no subject header'
        return ''

    else:
        available_content_subtypes = []
        subject = email_obj.get_all('subject')[0]
        if args.verbose:
            print 'subject: {}'.format(subject)
        if not email_obj.is_multipart():
            payload = email_obj.get_payload()
            body = payload
        else:
            payloads = email_obj.get_payload()
            for load in payloads:
                this_subtype = load.get_content_subtype()
                if this_subtype == args.content_type:
                    body = load.get_payload()
                else:
                    available_content_subtypes.append(this_subtype)
            if not vars().has_key('body'):
                body = 'desired content type: {0} not available.\navailable content types are: {1}'.format(args.content_type, available_content_subtypes)
        return {'subject': subject, 'body': body}

if __name__ == "__main__":
    '''the main method.'''
    parser = ArgumentParser()
    parser.add_argument('email_string', action = 'store', help = 'a string representation of the email.', metavar = '<INPUT>', nargs = '?')
    parser.add_argument('-t', dest = 'content_type', action = 'store', default = 'plain', help = 'the desired content type. ex: plain, html', metavar = '<CONTENT TYPE>')
    parser.add_argument('-v', dest = 'verbose', action = 'store_true', default = False, help = 'toggle verbosity')
    parser.add_argument('-f', dest = 'is_file', action = 'store_true', default = False, help = 'input is filename instead of string to parse')
    args = parser.parse_args()

    if args.verbose:
        print 'args: {}'.format(args)

    if args.email_string is not None:
        results = process(args.email_string, args)
    else:
        results = process(stdin.read(), args)

    if results is not '':
        print results
