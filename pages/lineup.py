from nicegui import ui, app
import shared


@ui.page('/lineup')
def lineup_page():
    shared.render_nav()
    ui.label('📋 Lineup Setup').classes('text-2xl font-bold p-4')

    stats = app.storage.user['stats']
    added_players = [p['Player'] for p in stats]
    default_players = ['Nevan', 'Theo', 'Kekoa']
    all_players = sorted(set(default_players + added_players))

    lineup = app.storage.user['lineup']

    def save_lineup(selected):
        app.storage.user['lineup'] = sorted(selected)
        ui.notify('Lineup saved successfully.')

    with ui.column().classes('p-4 gap-4'):
        multi = ui.select(
            options=all_players,
            label='Select players for the lineup (alphabetical)',
            value=lineup,
            multiple=True,
        )

        ui.button('💾 Save Lineup', on_click=lambda: save_lineup(multi.value))

        ui.label('Current lineup (alphabetical):').classes('mt-4 font-semibold')
        lineup_str = ', '.join(sorted(app.storage.user['lineup'])) or 'No players yet.'
        ui.label(lineup_str)

    # --- Game & Season Controls ---
    ui.separator()

    ui.label('Game & Season Controls').classes('text-xl font-bold mt-6')

    # New Game (safe)
    def new_game():
        app.storage.user['game_stats'] = []          # clear current game only
        app.storage.user['last_play_p1'] = None      # clear undo history
        app.storage.user['last_play_p2'] = None
        ui.notify('New game started — game stats cleared!', type='positive')

    ui.button('Start New Game', on_click=new_game).classes('mt-2')

    # Start New Season (dangerous, with confirmation)
    def confirm_new_season():
        with ui.dialog() as dialog:
            with ui.column().classes('p-4 items-center'):
                ui.label('Are you sure you want to start a new season?').classes('text-lg font-bold')
                ui.label('This will erase ALL stats and season data (lineup will be kept).')

                with ui.row().classes('gap-4 mt-4'):
                    ui.button('Cancel', on_click=dialog.close)
                    ui.button('Yes, Start New Season', 
                              on_click=lambda: do_new_season(dialog)
                    ).classes('bg-red-600 text-white')

        dialog.open()

    def do_new_season(dialog):
        # Keep lineup, clear everything else
        lineup = app.storage.user.get('lineup', [])

        app.storage.user.clear()

        # Restore lineup after clearing
        app.storage.user['lineup'] = lineup
        app.storage.user['stats'] = []
        app.storage.user['game_stats'] = []
        app.storage.user['last_update'] = None
        app.storage.user['last_play_p1'] = None
        app.storage.user['last_play_p2'] = None

        dialog.close()
        ui.notify('New season started — all data cleared!', type='positive')

    ui.button('Start New Season', on_click=confirm_new_season).classes('bg-red-600 text-white mt-4')