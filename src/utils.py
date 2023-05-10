import io
import json
from base64 import b64decode

def dbc_upload(upload):
    content_type, content_string = upload.split(",")
    decoded = b64decode(content_string)
    return json.loads(io.BytesIO(decoded).getvalue())