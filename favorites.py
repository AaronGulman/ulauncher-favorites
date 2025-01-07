from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

class FavoritesExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        try:
            code_command = extension.preferences.get("code_command", "code") 
            favorites = extension.preferences.get("favorites", [])
            
            items = []
            query = event.get_argument()

            if query:
                favorites = [fav for fav in favorites if query.lower() in fav.lower()]

            if favorites:
                for favorite in favorites:
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=favorite,
                        description=f'Favorite: {favorite}',
                        on_enter=RunScriptAction(f"{code_command} {favorite}")
                    ))
            else:
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name='No favorites found',
                    description='No favorites matching your query.',
                    on_enter=HideWindowAction()
                ))

            return RenderResultListAction(items)

        except Exception as e:
            print(f"Error: {e}")
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name="Error",
                description="An error occurred.",
                on_enter=HideWindowAction()
            )])

if __name__ == '__main__':
    FavoritesExtension().run()
