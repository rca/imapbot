from imapbot.envelope import Envelope


class Message(object):
    def __init__(self, id, envelope, text, flags):
        self.id = id
        self.flags = flags
        self.envelope = Envelope(envelope)
        self.text = text

        self._parsed = None

    @property
    def parsed(self):
        if self._parsed:
            return self._parsed

        split = self.text.splitlines()

        parsed = {}

        marker = split[-1]
        if marker.startswith('--') and marker.endswith('--'):
            body = []
            content_type = None

            # this is a multipart message body
            idx = 0
            while idx < len(split):
                line = split[idx]

                if line and marker.startswith(line):
                    if content_type is not None:
                        parsed[content_type] = '\r\n'.join(body)

                        content_type = None
                        body = []

                    idx += 1
                    continue

                elif line.startswith('Content-Type'):
                    content_type = line.split(';', 1)[0].split(' ', 1)[-1]
                    idx += 2
                    continue

                body.append(line)
                idx += 1
        else:
            parsed['text/plain'] = self.text

        self._parsed = parsed

        return self._parsed

    @property
    def html(self):
        return self.parsed.get('text/html')

    @property
    def plain(self):
        return self.parsed.get('text/plain')
