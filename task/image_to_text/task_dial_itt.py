import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image(file_name: str = 'dialx-banner.png') -> Attachment:
    image_path = Path(__file__).parent.parent.parent / file_name
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_cli:
      with open(image_path, 'rb') as f:
          image_bytes = BytesIO(f.read())
          json = await bucket_cli.put_file(name=file_name, mime_type='image/png', content=image_bytes)
          return Attachment(title=file_name, type=json['contentType'], url=json['url'])

    return None


async def start() -> None:
    # TODO:
    #  1. Create DialModelClient
    dial_client = DialModelClient(api_key=API_KEY, endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, deployment_name="gpt-4o")

    attachemnt_task = [_put_image(img) for img in ['dialx-banner.png', '20260224151722_Image.png']]
    attachements = await asyncio.gather(*attachemnt_task)
    if not all(attachements):
        raise Exception("Failed to upload image")

    print(f"Image(s) uploaded to DIAL bucket. URLs: {[att.url for att in attachements]}")
    message =  Message(role=Role.USER, content="What do you see on this picture(s)?", custom_content=CustomContent(attachments=attachements))
    resp_msg = dial_client.get_completion(messages=[message])
    print(f"Model response: {resp_msg.content}")

asyncio.run(start())
