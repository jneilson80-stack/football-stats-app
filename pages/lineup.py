from nicegui import ui, app
import shared


@ui.page('/lineup')
def lineup_page():
    shared.ensure_storage()
    shared.render_nav()

    ui.label('📋 Lineup Setup').classes('text-2xl font-bold p-4')

    # Ensure lineup exists
    if 'lineup' not in app.storage.user:
        app.storage.user['lineup'] = []

    # ----------------------------------------
    # UI LAYOUT (UI FIRST — CALLBACKS LATER)
    # ----------------------------------------
    with ui.column().classes('p-4 gap-4'):

        # Input field + Add button
        name_input = ui.input(
            label='Enter Name',
            placeholder='Type a player name...',
        )
        add_button = ui.button('➕ Add Player')

        # Current lineup list
        ui.label('Current Lineup:').classes('mt-4 font-semibold')

        list_area = ui.column()

        # Reset lineup section
        ui.separator()
        ui.label('Reset Lineup').classes('mt-4 font-semibold text-red-600')
        clear_button = ui.button(
            '🗑️ Clear Entire Lineup',
            color='red',
        ).classes('mt-2')

        # Game & Season controls
        ui.separator()
        ui.label('Game & Season Controls').classes('text-xl font-bold mt-6')

        new_game_button = ui.button(
            '🔄 Start New Game',
        ).classes('mt-2')

        new_season_button = ui.button(
            '🔥 Start New Season',
        ).classes('bg-red-600 text-white mt-2')

    # ----------------------------------------
    # HELPERS
    # ----------------------------------------
    def get_lineup():
        return app.storage.user.get('lineup', [])

    def set_lineup(new_list):
        app.storage.user['lineup'] = new_list

    # ----------------------------------------
    # REFRESH LIST
    # ----------------------------------------
    def refresh_list():
        lineup = get_lineup()
        list_area.clear()

        if not lineup:
            with list_area:
                ui.label('No players yet.')
        else:
            with list_area:
                ui.label('Tap a name to remove it.').classes(
                    'text-sm text-gray-600 mb-2'
                )
                for p in lineup:
                    ui.button(
                        f'• {p}',
                        on_click=lambda name=p: tap_to_remove(name),
                    ).classes('w-full text-left')
                ui.label(f'Total Players: {len(lineup)}').classes(
                    'mt-2 text-sm text-gray-600'
                )

    # ----------------------------------------
    # CALLBACKS (AFTER UI EXISTS)
    # ----------------------------------------
    def add_player():
        lineup = get_lineup()
        name = name_input.value.strip()
        if not name:
            ui.notify('Please enter a name.', type='warning')
            return

        name = name.title()
        if name in lineup:
            ui.notify('Player already in lineup.', type='warning')
            return

        lineup.append(name)
        lineup.sort()
        set_lineup(lineup)
        name_input.value = ''
        refresh_list()
        ui.notify(f'Added {name} to lineup.')

    def tap_to_remove(name):
        lineup = get_lineup()
        if name in lineup:
            lineup.remove(name)
            set_lineup(lineup)
            refresh_list()
            ui.notify(f'Removed {name} from lineup.')

    def clear_lineup():
        set_lineup([])
        refresh_list()
        ui.notify('Lineup cleared.', type='positive')

    def start_new_game():
        app.storage.user['game_stats'] = []
        app.storage.user['last_play_p1'] = None
        app.storage.user['last_play_p2'] = None
        ui.notify(
            'New game started — current game stats cleared.',
            type='positive',
        )

    def confirm_new_season():
        with ui.dialog() as dialog:
            with ui.column().classes('p-4 items-center'):
                ui.label('Start a NEW SEASON?').classes('text-lg font-bold')
                ui.label(
                    'This will erase ALL stats, including season totals.'
                )

                with ui.row().classes('gap-4 mt-4'):
                    ui.button('Cancel', on_click=dialog.close)
                    ui.button(
                        'Yes, Start New Season',
                        on_click=lambda: do_new_season(dialog),
                    ).classes('bg-red-600 text-white')

        dialog.open()

    def do_new_season(dialog):
        app.storage.user['game_stats'] = []
        app.storage.user['season_stats'] = []
        app.storage.user['last_play_p1'] = None
        app.storage.user['last_play_p2'] = None
        dialog.close()
        ui.notify(
            'New season started — all stats cleared!',
            type='positive',
        )

    # ----------------------------------------
    # BIND CALLBACKS TO UI
    # ----------------------------------------
    name_input.on('keydown.enter', add_player)
    add_button.on_click(add_player)
    clear_button.on_click(clear_lineup)
    new_game_button.on_click(start_new_game)
    new_season_button.on_click(confirm_new_season)

    # Initial list render
    refresh_list()