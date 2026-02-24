import asyncio
import aiofiles
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"


async def _save_images(attachments: list[Attachment]):
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        async def save_img(attachment: Attachment):
            content = await bucket_client.get_file(attachment.url)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{
                attachment.title}.png"
            async with aiofiles.open(filename, "wb") as f:
                await f.write(content)
            print(f"Image {filename} has been saved locally.")

        tasks = [save_img(att)
                 for att in attachments if hasattr(att, "url") and att.url]
        await asyncio.gather(*tasks)


async def start() -> None:
    dial_client = DialModelClient(
        api_key=API_KEY, deployment_name="dall-e-3", endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT)

    config = dict(
        size=Size.square,
        style=Style.vivid,
        quality=Quality.standard
    )

    message = Message(
        role=Role.USER,
        content="Generate an image of a sunny day on a bich of Black Sea.",
    )
    resp = dial_client.get_completion(
        messages=[message], custom_fields=config)
    attachments = resp.custom_content.attachments
    if attachments:
        await _save_images(attachments)


asyncio.run(start())
