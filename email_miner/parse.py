import base64
import datetime
import tempfile
from typing import List, Dict, Any, Optional

from imapclient.response_types import Envelope
from mailparser import mailparser

from email_miner.email import Email, Attachment


def decode_attachment_data(attachment) -> bytes:
    """
    Decode a raw attachment into usable bytes.

    :param attachment:
    :return: the bytes containing file data
    """
    if attachment['content_transfer_encoding'] == 'base64':
        return base64.b64decode(attachment['payload'])
    return attachment['payload'].encode('utf-8')


def empty_if_none(input_value=None) -> List[Any]:
    """
    Return an empty list of the input value is None.

    :param input_value:
    :return:
    """
    if input_value is not None:
        return input_value
    return []


def decode_bytes_str(input_value=None, charset='utf-8') -> Optional[str]:
    """
    Decode input value to string using the given charset
    :param charset: charset to use while decoding (defaults to utf-8)
    :param input_value:
    :return:
    """
    if input_value is not None and not isinstance(input_value, str):
        return input_value.decode(charset)
    return input_value


def parse_emails(raw_emails: Dict[int, Dict], in_memory: bool = True) -> List[Email]:
    """
    Parse raw emails into easy-to-use classes.

    :param raw_emails:
    :param in_memory:
    :return: list of Email classes.
    """
    emails = []

    for mail_id, raw_email in raw_emails.items():
        email = Email()
        envelope: Envelope = raw_email[b'ENVELOPE']
        internal_date: datetime.datetime = raw_email[b'INTERNALDATE']

        email.raw_envelope = envelope

        email.id = int(mail_id)
        email.date = envelope.date
        email.internal_date = internal_date
        email.subject = decode_bytes_str(envelope.subject)
        email.from_addresses = list(empty_if_none(envelope.from_))
        email.reply_to_addresses = list(empty_if_none(envelope.reply_to))
        email.to_addresses = list(empty_if_none(envelope.to))
        email.cc_addresses = list(empty_if_none(envelope.cc))
        email.bcc_addresses = list(empty_if_none(envelope.bcc))
        email.in_reply_to = decode_bytes_str(envelope.in_reply_to)
        email.uuid = decode_bytes_str(envelope.message_id)

        if b'BODY[]' in raw_email:
            email.raw_body = raw_email[b'BODY[]']
            parsed = mailparser.parse_from_bytes(email.raw_body)
            for raw_attachment in parsed.attachments:
                attachment = Attachment()
                attachment.file_name = raw_attachment['filename']
                attachment.content_type = raw_attachment['mail_content_type']
                data_bytes = decode_attachment_data(raw_attachment)
                if in_memory:
                    attachment.file_content = data_bytes
                else:
                    fd, path = tempfile.mkstemp()
                    fd.write(data_bytes)
                    attachment.file_path = path
                    fd.close()
                email.attachments.append(attachment)

        emails.append(email)

    return emails
