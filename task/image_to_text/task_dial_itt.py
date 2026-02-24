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
    bucket_cli = DialBucketClient(api_key=API_KEY, base_url=DIAL_URL)
    # load image bytes
    with open(image_path, 'rb') as f:
        image_bytes = BytesIO(f.read())
        return bucket_cli.put_file(name=file_name, mime_type='image/png', content=image_bytes)

    return None


def start() -> None:
    # TODO:
    #  1. Create DialModelClient
    #  2. Upload image (use `_put_image` method )
    #  3. Print attachment to see result
    #  4. Call chat completion via client with list containing one Message:
    #    - role: Role.USER
    #    - content: "What do you see on this picture?"
    #    - custom_content: CustomContent(attachments=[attachment])
    #  ---------------------------------------------------------------------------------------------------------------
    #  Note: This approach uploads the image to DIAL bucket and references it via attachment. The key benefit of this
    #        approach that we can use Models from different vendors (OpenAI, Google, Anthropic). The DIAL Core
    #        adapts this attachment to Message content in appropriate format for Model.
    #  TRY THIS APPROACH WITH DIFFERENT MODELS!
    #  Optional: Try upload 2+ pictures for analysis
    raise NotImplementedError


start()
