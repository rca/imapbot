"""
A Context for working with an IMAP connection in an unidle state
"""


class Unidle(object):
    def __init__(self, mail_reader):
        self.mail_reader = mail_reader

        self.should_reidle = False

    def __enter__(self):
        self.should_reidle = self.mail_reader.unidle() is not None

    def __exit__(self, ExceptionCls, exception, traceback):
        if self.should_reidle:
            self.mail_reader.idle()

        # don't process exceptions, let upstream do that.
        return False
