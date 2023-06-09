from ahk import AHK

from handle_youtube import download_with_ui

ahk = AHK()
ahk.add_hotkey('^+!y', callback=download_with_ui)
ahk.start_hotkeys()
ahk.block_forever()