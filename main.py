from nicegui import ui, app

# ----------------------------------------
# Persistent user storage initialization
# ----------------------------------------

def ensure_storage():
    defaults = {
        'stats': [],
        'lineup': [],
        'last_play_p1': None,
        'last_play_p2': None,
    }
    for k, v in defaults.items():
        if k not in app.storage.user:
            app.storage.user[k] = v

# ----------------------------------------
# Shared navigation bar
# ----------------------------------------

def render_nav():
    with ui.header().classes('items-center justify-between bg-blue-700 text-white p-4'):
        ui.label('🏈 Unified Flag Football Stats & Fast Tap').classes('text-xl font-bold')

    with ui.row().classes('w-full justify-around bg-gray-100 p-3'):
        ui.link('Home', '/')
        ui.link('Lineup Setup', '/lineup')
        ui.link('Add / Merge Players', '/add')
        ui.link('Fast Tap Game Mode', '/game')
        ui.link('Export / Season', '/export')
        ui.link('FAQ', '/faq')

# ----------------------------------------
# HOME PAGE
# ----------------------------------------

@ui.page('/')
def home_page():
    ensure_storage()   # <-- runs safely here on first page load
    render_nav()
    ui.label('Welcome! Use the navigation above to begin.').classes('text-lg p-4')

# ----------------------------------------
# Import subpages
# ----------------------------------------

import pages.lineup
import pages.add_merge
import pages.game
import pages.export
import pages.faq

# ----------------------------------------
# Run app
# ----------------------------------------

ui.run(
    host='0.0.0.0',
    port=8080,
    storage_secret='flagstats_2026_live'
)