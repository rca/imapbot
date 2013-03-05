"""
Module to retrieve envelope fields by name, not just index
"""


class Envelope(tuple):
    fields = (
        'date',  # Returns a string that represents the date.
        'subject',  # Returns a string that represents the subject.
        'from',  # Returns a list of addresses that represents the from.
        'sender',  # Returns a list of addresses that represents the sender.
        'reply_to',  # Returns a list of addresses that represents the reply-to.
        'to',  # Returns a list of addresses that represents the to.
        'cc',  # Returns a list of addresses that represents the cc.
        'bcc',  # Returns a list of addresses that represents the bcc.
        'in_reply_to',  # Returns a string that represents the in-reply-to.
        'message_id',  # Returns a string that represents the message-id.
    )

    def __getitem__(self, field):
        try:
            index = self.fields.index(field)
            return super(Envelope, self).__getitem__(index)
        except ValueError:
            if type(field) != int:
                raise ValueError('"{}" is not an envelope field'.format(field))

            return super(Envelope, self).__getitem__(field)

    def get_email(self, field):
        value = self[field][0]

        return '@'.join((value[2], value[3]))
