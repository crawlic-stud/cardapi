from vk_getter import VKGetter

from config import TOKEN

getter = VKGetter(TOKEN)


def get_cat_photos_urls():
    """Returns a list with a lot of cat photo URLs"""


    groups = ["ilovekitsi", "kot9ta", "ko73n0k", "public212942935"]
    all_attachments = []

    for group in groups:
        posts = getter.get_posts(group, 1000)
        attachments = getter.extract(posts, "photo")
        all_attachments += attachments
    return all_attachments
