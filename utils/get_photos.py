import os

from vk_getter import VKGetter


TOKEN = os.getenv("VK_TOKEN")
getter = VKGetter(TOKEN)


CAT_GROUPS = ["ilovekitsi", "kot9ta", "ko73n0k", "public212942935"]
DOG_GROUPS = ["whoisthegoodestboy", "ot_shib", "gavkakuso"]


def get_photos_urls(groups: list[str] = CAT_GROUPS, count: int = 3000) -> list[str]:
    """Returns a list with a lot of cat photo URLs"""

    all_attachments = []
    for group in groups:
        posts = getter.get_posts(group, count)
        attachments = getter.extract(posts, "photo")
        all_attachments += attachments
    return all_attachments
