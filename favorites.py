import logging
import os
from pathlib import Path
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower()
        favorites = extension.get_favorites()
        items = []

        for path in favorites:
            full_path = Path(os.path.expanduser(path))  
            if not full_path.exists():
                logger.warning(f"Path does not exist: {full_path}")
                continue

            if query in full_path.name.lower():
                item = ExtensionResultItem(
                    icon='images/favorites.png',
                    name=full_path.name,
                    description=f"Path: {full_path}",
                    on_enter=OpenUrlAction(f"file://{full_path}"),
                )
                items.append(item)

        if not items:
            logger.info("No matches found for the query.")
            items.append(
                ExtensionResultItem(
                    icon='images/favorites.png',
                    name="No matches found",
                    description="Try a different query or check your paths.",
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
        favorites = [os.path.expanduser(fav.strip()) for fav in favorites_raw.split(",") if fav.strip()]
        
        valid_favorites = []
        for fav in favorites:
            if os.path.exists(fav):
                valid_favorites.append(fav)
            else:
                logger.warning(f"Favorite path not found: {fav}")
        
        logger.debug(f"Loaded valid favorites: {valid_favorites}")
        return valid_favorites

if __name__ == "__main__":
    FavoritesExtension().run()
