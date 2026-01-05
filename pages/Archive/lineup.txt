from nicegui import ui, app
import shared

@ui.page('/lineup')
def lineup_page():
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