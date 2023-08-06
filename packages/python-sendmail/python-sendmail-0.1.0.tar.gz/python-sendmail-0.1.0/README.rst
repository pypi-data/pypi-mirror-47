python-sendmail
===============

Pure python sendmail client.

Install
-------

::

    pip install python-sendmail


Help
----

::

    E:\python-sendmail>python sendmail.py --help
    Usage: sendmail.py [OPTIONS] [CONTENT]

    Send an email via command line.

    Note:

    If CONTENT is not provided in command line, will read it from STDIN.

    Options:
    -f, --from-address TEXT  Sender's mail address, e.g. Sender Name
                            <sender@exmaple.com> or sender@example.com
                            [required]
    -t, --to-address TEXT    Recipient's mail address, e.g. Recipient Name
                            <recipient@exmaple.com> or recipient@example.com
                            [required]
    -s, --subject TEXT       Mail subject
    -a, --attach TEXT        Attachment file path, can use multiple times.
    --html                   The content is html format
    -e, --encoding TEXT      Encoding of the content, defaults to utf-8
    -h, --host TEXT          Email server address
    -p, --port INTEGER       Email server port
    --ssl                    Email server use ssl
    -u, --user TEXT          Login user
    -P, --password TEXT      Login password
    --help                   Show this message and exit.

Usage
-----

SENDER(sender@exmaple.com) send an email to recipient@exmaple.com, mail subject is 'just a test mail' and mail content is 'just a test mail'.

::

    sendmail -h stmp.example.com -p 465 --ssl -u sender@example.com -P senderPassword -f 'SENDER <sender@exmaple.com>' -t recipient@exmaple.com -s 'just a test mail' 'just a test mail'


SENDER(sender@exmaple.com) send an email to recipient@exmaple.com, mail subject is 'just a test mail', mail content is 'just a test mail', and with an attachment file named 'attachment.pdf'

::

    sendmail -h stmp.example.com -p 465 --ssl -u sender@example.com -P senderPassword -f 'SENDER <sender@exmaple.com>' -t recipient@exmaple.com -s 'just a test mail' -a /path/to/attachment.pdf 'just a test mail'
