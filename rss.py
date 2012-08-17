#!/usr/local/bin/python
import xml.etree.ElementTree as etree
from argparse import ArgumentParser
from tempfile import TemporaryFile
from sys import stdin
import email
import os

template = '''<?xml version="1.0" encoding="ISO-8859-1" ?>
<rss version="2.0">
 <channel>
  <title>New Email</title>
  <link></link>
  <description>Non-reply email.</description>
  <item>
   <sequence_number></sequence_number>
   <title></title>
   <link></link>
   <description></description>
   <date></date>
  </item>
 </channel>
</rss>'''

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
        '''###########################'''
        #Use email.Parser for this part. seems 2 work w sample email.
        '''###########################'''
        if not email_obj.is_multipart():
            partlist = []
            for i in email_obj.walk():
                partlist.append(i)
            body = partlist[0]
        else:
            parts = []
            for i in email_obj.walk():
                parts.append(i)
            for part in parts:
                this_subtype = part.get_content_subtype()
                if this_subtype == args.content_type:
                    body = part.as_string()
                else:
                    available_content_subtypes.append(this_subtype)
            if not vars().has_key('body'):
                body = 'desired content type: {0} not available.\navailable content types are: {1}'.format(args.content_type, available_content_subtypes)
        if not vars().has_key('email_date'):
            email_date = ''

        rss_params = {'subject': subject, 'body': body, 'date': email_date, 'location': args.rss_path, 'verbose': args.verbose}
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
            parts = []
            for part in email_obj.walk():
                if args.verbose:
                    print '\nemail_part: {}'.format(part.get_payload())
                parts.append(i)
            body = parts[0].as_string()
        else:
            parts = []
            for part in email_obj.walk():
                if args.verbose:
                    print '\nemail_part: {}'.format(part.get_payload())
                parts.append(part)
            for part in parts:
                this_maintype = part.get_content_maintype()
                this_subtype = part.get_content_subtype()
                if this_maintype == 'text' and this_subtype == args.content_type:
                    body = part.as_string()
                    break
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

def update_rss(tree, params):
    '''takes params and obj, updates obj with params'''
    subject_node = tree.find('./channel/item/title')

    if params['verbose']:
        print 'subject_node: {}'.format(subject_node.text)
        print 'params["subject"]: {}'.format(params['subject'])

    no_listserv_subject = str(params['subject'])
    if no_listserv_subject.startswith('['):
        no_listserv_subject = no_listserv_subject[(no_listserv_subject.index(']')+2):]

    subject_node.text = no_listserv_subject

    body_node = tree.find('./channel/item/description')

    if params['verbose']:
        print 'body_node: {}'.format(body_node.text)

    body_node.text = params['body'].replace('_', '')

    sequence_number_node = tree.find('./channel/item/sequence_number')

    if params['verbose']:
        print 'sequence_number: {}'.format(sequence_number_node.text)

    #if sequence_number_node.text != None:
    #    seq_num = int(sequence_number_node.text)
    #else:
    #    seq_num = 0
    #seq_num += 1
    #sequence_number_node.text = str(seq_num)

    date_node = tree.find('./channel/item/date')
    if params['verbose']:
        print 'date: {}'.format(date_node.text)

    date_node.text = params['date'][0]

    if params['verbose']:
        print 'modified rss file:\n{}'.format(etree.dump(tree))

    tree.write(params['location'])

def make_rss(params):
    '''takes a dict of params, and remakes the rss file if appropriate'''
    if not os.path.exists(params['location']):
        try:
            open(params['location'], 'w')
            make_rss(params)
        except Exception, err:
            print 'error: {0}\n\t{1}'.format(Exception, err)
    else:
        try:
            tree = etree.parse(params['location'])
        except:
            with TemporaryFile() as fd:
                fd.seek(0) #just in case
                fd.write(template)
                fd.seek(0)
                tree = etree.parse(fd)

        try:
            current_subject = tree.find('./channel/item/title')
        except:
            current_subject = ''

        try:
            current_body = tree.find('./channel/item/description')
        except:
            current_body = ''

        if current_subject.text is not params['subject'] and \
            current_body.text is not params['body']:
            if params['verbose']:
                 print 'tree: {}'.format(etree.dump(tree))
            update_rss(tree, params)

if __name__ == "__main__":
    '''the main method.'''
    #create parser obj
    parser = ArgumentParser()

    #this is the email contents or the filename that we want to look at
    parser.add_argument('email_string', action = 'store',
        help = 'a string representation of the email.', metavar = '<INPUT>',
        nargs = '?')

    #this is the desired content subtype, defaults to plain
    parser.add_argument('-t', dest = 'content_type', action = 'store',
        default = 'plain', help = 'the desired content type. ex: plain, html',
        metavar = '<CONTENT TYPE>')

    #toggle verbosity with the -v flag of course
    parser.add_argument('-v', dest = 'verbose', action = 'store_true',
        default = False, help = 'toggle verbosity')

    #if the main param is a filename, specify that with the -f flag
    parser.add_argument('-f', dest = 'is_file',
        action = 'store_true', default = False, 
        help = 'input is filename instead of string to parse')

    #the output file path is here, specified by an argument following option -r
    #defaults to './rss.xml'
    parser.add_argument('-r', dest = 'rss_path', action = 'store',
        help = 'path to rss file.', default = './rss.xml',
        metavar = '<PATH TO RSS>')

    #parse the args
    args = parser.parse_args()

    #print if verbose
    if args.verbose:
        print 'args: {}'.format(args)

    #if we enter an email string parameter, print it 
    #out like so and pass to process
    if args.email_string is not None:
        if args.verbose:
            print 'process(args.email_string, args)'
        results = process(args.email_string, args)
    #if not, we're going from standard in! print if verbose
    else:
        if args.verbose:
            print 'process(stdin.read(), args)'
        results = process(stdin.read(), args)

    #process will do the file i/o, so here's a print
    #to verify results
    if results is not '':
        print results
