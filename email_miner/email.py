import datetime
from typing import List

from imapclient.response_types import Address, Envelope


class Attachment:
    """
    :ivar file_name: Name of the attachment file
    :ivar content_type: content type (mime) of the attachment file
    :ivar file_content: content of the file as bytes
    :ivar file_path: file path of the locally stored copy of the attachment
    """
    file_name: str
    content_type: str
    file_content: bytes
    file_path: str = None


class Email:
    """
    :ivar id: Unique ID referring to the mail in the mailbox
    :ivar date: A datetime instance that represents the "Date" header.
    :ivar subject: A string that contains the "Subject" header.
    :ivar from: A tuple of Address objects that represent one or more
      addresses from the "From" header, or None if header does not exist.
    :ivar reply_to: As for from but represents the "Reply-To" header.
    :ivar to: As for from but represents the "To" header.
    :ivar cc: As for from but represents the "Cc" header.
    :ivar bcc: As for from but represents the "Bcc" recipients.
    :ivar in_reply_to: A string that contains the "In-Reply-To" header.
    :ivar message_id: A string that contains the "Message-Id" header.
    """
    id: int
    date: datetime.datetime
    internal_date: datetime.datetime
    subject: str
    from_addresses: List[Address] = []
    reply_to_addresses: List[Address] = []
    to_addresses: List[Address] = []
    cc_addresses: List[Address] = []
    bcc_addresses: List[Address] = []
    in_reply_to: str
    message_id: str

    raw_envelope: Envelope
    raw_body: bytes

    attachments: List[Attachment] = []
