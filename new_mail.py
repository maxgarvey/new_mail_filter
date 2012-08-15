#!/usr/local/bin/python

import email
from argparse import ArgumentParser
from sys import stdin
from rss import make_rss

def process(email_string, args):
    '''determines if email is response, if not returns the subject and body 
    of the message'''
    if args.is_file: #check to see if its a file
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
        if email_obj.has_key('date'):
            if args.verbose:
                print 'email_obj.get_all("date"): {}'.format(email_obj.get_all('date'))
            email_date = email_obj.get_all('date')
        else:
            email_date = ''


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
        if not vars().has_key('email_date'):
            email_date = ''

        rss_params = {'subject': subject, 'body': body, 'date': email_date, 'location': args.rss_path, 'verbose': args.verbose}
        if args.verbose:
            print 'rss_params:\n{}'.format(rss_params)
        make_rss(rss_params)

        return {'subject': subject, 'body': body}

if __name__ == "__main__":
    '''the main method.'''
    parser = ArgumentParser()
    parser.add_argument('email_string', action = 'store', help = 'a string representation of the email.', metavar = '<INPUT>', nargs = '?')
    parser.add_argument('-t', dest = 'content_type', action = 'store', default = 'plain', help = 'the desired content type. ex: plain, html', metavar = '<CONTENT TYPE>')
    parser.add_argument('-v', dest = 'verbose', action = 'store_true', default = False, help = 'toggle verbosity')
    parser.add_argument('-f', dest = 'is_file', action = 'store_true', default = False, help = 'input is filename instead of string to parse')
    parser.add_argument('-r', dest = 'rss_path', action = 'store', help = 'path to rss file.', default = './rss.xml',  metavar = '<PATH TO RSS>')
    args = parser.parse_args()

    if args.verbose:
        print 'args: {}'.format(args)

    if args.email_string is not None:
        if args.verbose:
            print 'process(args.email_string, args)'
        results = process(args.email_string, args)
    else:
        if args.verbose:
            print 'process(stdin.read(), args)'
        results = process(stdin.read(), args)

    if results is not '':
        print results
