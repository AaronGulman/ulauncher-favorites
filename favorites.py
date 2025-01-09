import logging
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        favorites = extension.get_favorites()
        items = []

        for path in favorites:
            if query.lower() in os.path.basename(path).lower():
                item = ExtensionResultItem(
                    icon='images/favorites.png',
                    name=os.path.basename(path),
                    description=f"Path: {path}",
                    on_enter=OpenUrlAction(f"file://{path}"),
                )
                items.append(item)

        if not items:
            items.append(
                ExtensionResultItem(
                    icon='images/favorites.png',
                    name="No matches found",
                    description="Try a different query.",
                    on_enter=None,
                )
            )

        return items


class FavoritesExtension(Extension):
    def __init__(self):
        super(FavoritesExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def get_favorites(self):
        favorites_raw = self.preferences.get("favorites", "")
        favorites = [fav.strip() for fav in favorites_raw.split(",") if fav.strip()]
        logger.debug(f"Loaded favorites: {favorites}")
        return favorites


if __name__ == "__main__":
    FavoritesExtension().run()
