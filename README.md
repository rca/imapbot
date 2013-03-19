imapbot
=======

A small robot to read email from an IMAP mailbox.

This is an experimental idea to build a thin robot that can read email from an
IMAP mailbox and inject it into an application.  The `handle_message()` method
would be defined in an `IMAPBot` subclass and coded up to process incoming
messages as desired.  For example, this could be used to process an email box
and inject messages into a web application.
