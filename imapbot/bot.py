from imapclient import IMAPClient

from imapbot.message import Message
from imapbot.unidle import Unidle


class IMAPBotError(Exception):
    pass


class IMAPBot(object):
    IMAPBotError = IMAPBotError

    def __init__(self, host, username, password, ssl=True):
        self.server = IMAPClient(host, use_uid=True, ssl=ssl)
        self.server.login(username, password)

        if 'IDLE' not in self.server.capabilities():
            raise IMAPBotError('Sorry, this IMAP server does not support IDLE.')

        # the folder where processed emails go
        self.processed_folder = 'imapbot_processed'

        self.idle_timeout = 5  # seconds

        self._is_idle = False
        self._run = True

        self._create_folder(self.processed_folder)

    def check_mail(self):
        select_info = self.server.select_folder('INBOX')
        print '%d messages in INBOX' % select_info['EXISTS']

        messages = self.server.search(['UNSEEN'])
        messages = self.server.search(['NOT DELETED'])
        print "%d messages that haven't been seen" % len(messages)

        if not messages:
            return

        #response = self.server.fetch(messages, ['FLAGS', 'INTERNALDATE', 'RFC822.SIZE', 'ENVELOPE', 'RFC822.TEXT'])
        response = self.server.fetch(messages, ['FLAGS', 'ENVELOPE', 'RFC822.TEXT'])
        for message_id, data in response.iteritems():
            message = Message(message_id, data['ENVELOPE'], data['RFC822.TEXT'], data['FLAGS'])

            self.process(message)

    def complete(self, message):
        message_ids = [message.id]

        self.server.copy(message_ids, self.processed_folder)
        self.server.delete_messages(message_ids)
        self.server.expunge()

    def _create_folder(self, name):
        # make sure the folder doesn't already exist
        if self.server.folder_exists(name):
            return

        self.server.create_folder(name)

    def handle_message(self, message):
        print 'message id: {}, from: {}:'.format(message.id, message.envelope.get_email('from'))
        with open('message.txt', 'ab') as fh:
            fh.write('{}\n\n'.format(message.text))

        print message.plain or message.html or 'no message'

    def idle(self):
        if self._is_idle:
            return

        self.server.idle()

        self._is_idle = True

        return True  # this actually changed state

    def unidle(self):
        if not self._is_idle:
            return

        self.server.idle_done()

        self._is_idle = False

        return True  # this call actually changed state

    def process(self, message):
        self.handle_message(message)
        self.complete(message)

    def run(self):
        # process any mail that was in the inbox before coming online
        self.check_mail()

        # put the connection in idle mode so we get notifications
        self.idle()

        # loop forever looking for stuff
        while self._run:
            for message in self.server.idle_check(timeout=self.idle_timeout):
                if message[0] == 'OK':
                    continue

                with Unidle(self):
                    self.check_mail()

    def quit(self):
        self._run = False

        self.unidle()

        print self.server.logout()
