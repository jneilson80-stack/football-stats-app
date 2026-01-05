from nicegui import ui, app
import shared

@ui.page('/game')
def game_page():

    ui.label('⚡ Fast Tap Game Mode (Two Players)').classes('text-2xl font-bold p-4')

    lineup = app.storage.user['lineup']
    if not lineup:
        ui.label('No players in lineup. Add players first.').classes('text-red-600 text-lg p-4')
        return

    # ----------------------------------------
    # Player selectors
    # ----------------------------------------

    with ui.row().classes('w-full justify-around p-4'):
        p1 = ui.select(lineup, label='Player 1').classes('w-1/3')
        p2 = ui.select(lineup, label='Player 2').classes('w-1/3')

    # ----------------------------------------
    # Side-by-side Fast Tap columns
    # ----------------------------------------

    with ui.row().classes('w-full justify-around p-4'):

        # ---------------- Player 1 ----------------
        with ui.column().classes('w-1/2 bg-gray-100 p-4 rounded-lg'):
            ui.label('Player 1 Actions').classes('text-xl font-bold')

            def tap1(field, delta):
                shared.record_fast_tap(p1.value, field, delta, 'p1')

            ui.button('🏳️ Flag Pull', on_click=lambda: tap1('Flag_Pulls', 1))
            ui.button('💥 Sack', on_click=lambda: tap1('Sacks', 1))
            ui.button('🎣 Interception', on_click=lambda: tap1('INT', 1))
            ui.button('🛑 Pass Breakup', on_click=lambda: tap1('PBU', 1))
            ui.button('🧨 Safety', on_click=lambda: tap1('Safety', 1))
            ui.button('🏈 Defensive TD', on_click=lambda: tap1('Def_TD', 1))
            ui.button('👐 Forced Fumble', on_click=lambda: tap1('Forced_Fumble', 1))

            ui.separator()

            ui.button('🤲 Reception', on_click=lambda: tap1('Rec', 1))
            ui.button('🟢 Rec TD', on_click=lambda: tap1('Rec_TD', 1))
            ui.button('📏 +1 Rec Yard', on_click=lambda: tap1('Rec_Yds', 1))
            ui.button('📏 +5 Rec Yards', on_click=lambda: tap1('Rec_Yds', 5))

            ui.separator()

            ui.button('🏃 Rush Attempt', on_click=lambda: tap1('Rush_Att', 1))
            ui.button('🟢 Rush TD', on_click=lambda: tap1('Rush_TD', 1))
            ui.button('📏 +1 Rush Yard', on_click=lambda: tap1('Rush_Yds', 1))
            ui.button('📏 +5 Rush Yards', on_click=lambda: tap1('Rush_Yds', 5))

            ui.separator()

            ui.button('🏈 Pass Attempt', on_click=lambda: tap1('Pass_Att', 1))
            ui.button('🎯 Pass Completion', on_click=lambda: tap1('Pass_Comp', 1))
            ui.button('🟢 Pass TD', on_click=lambda: tap1('Pass_TD', 1))
            ui.button('📏 +1 Pass Yard', on_click=lambda: tap1('Pass_Yds', 1))
            ui.button('📏 +5 Pass Yards', on_click=lambda: tap1('Pass_Yds', 5))
            ui.button('❌ INT Thrown', on_click=lambda: tap1('Pass_INT', 1))

            ui.separator()

            def undo1():
                if shared.undo_last('p1'):
                    ui.notify('Player 1: Last action undone')
                else:
                    ui.notify('Player 1: Nothing to undo')

            ui.button('↩️ Undo', on_click=undo1, color='red')

        # ---------------- Player 2 ----------------
        with ui.column().classes('w-1/2 bg-gray-100 p-4 rounded-lg'):
            ui.label('Player 2 Actions').classes('text-xl font-bold')

            def tap2(field, delta):
                shared.record_fast_tap(p2.value, field, delta, 'p2')

            ui.button('🏳️ Flag Pull', on_click=lambda: tap2('Flag_Pulls', 1))
            ui.button('💥 Sack', on_click=lambda: tap2('Sacks', 1))
            ui.button('🎣 Interception', on_click=lambda: tap2('INT', 1))
            ui.button('🛑 Pass Breakup', on_click=lambda: tap2('PBU', 1))
            ui.button('🧨 Safety', on_click=lambda: tap2('Safety', 1))
            ui.button('🏈 Defensive TD', on_click=lambda: tap2('Def_TD', 1))
            ui.button('👐 Forced Fumble', on_click=lambda: tap2('Forced_Fumble', 1))

            ui.separator()

            ui.button('🤲 Reception', on_click=lambda: tap2('Rec', 1))
            ui.button('🟢 Rec TD', on_click=lambda: tap2('Rec_TD', 1))
            ui.button('📏 +1 Rec Yard', on_click=lambda: tap2('Rec_Yds', 1))
            ui.button('📏 +5 Rec Yards', on_click=lambda: tap2('Rec_Yds', 5))

            ui.separator()

            ui.button('🏃 Rush Attempt', on_click=lambda: tap2('Rush_Att', 1))
            ui.button('🟢 Rush TD', on_click=lambda: tap2('Rush_TD', 1))
            ui.button('📏 +1 Rush Yard', on_click=lambda: tap2('Rush_Yds', 1))
            ui.button('📏 +5 Rush Yards', on_click=lambda: tap2('Rush_Yds', 5))

            ui.separator()

            ui.button('🏈 Pass Attempt', on_click=lambda: tap2('Pass_Att', 1))
            ui.button('🎯 Pass Completion', on_click=lambda: tap2('Pass_Comp', 1))
            ui.button('🟢 Pass TD', on_click=lambda: tap2('Pass_TD', 1))
            ui.button('📏 +1 Pass Yard', on_click=lambda: tap2('Pass_Yds', 1))
            ui.button('📏 +5 Pass Yards', on_click=lambda: tap2('Pass_Yds', 5))
            ui.button('❌ INT Thrown', on_click=lambda: tap2('Pass_INT', 1))

            ui.separator()

            def undo2():
                if shared.undo_last('p2'):
                    ui.notify('Player 2: Last action undone')
                else:
                    ui.notify('Player 2: Nothing to undo')

            ui.button('↩️ Undo', on_click=undo2, color='red')