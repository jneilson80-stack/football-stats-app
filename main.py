from nicegui import ui, app
import shared

# ----------------------------------------
# FOOTBALL HOME PAGE
# ----------------------------------------

@ui.page('/')
def home_page():
    shared.ensure_storage()
    shared.render_nav()

    ui.label('🏈 Welcome to Fast Football Stats!').classes('text-2xl font-bold p-4')
    ui.markdown(
        "This app is designed for **fast, reliable stat tracking** right at the field.\n\n"
        "Use the navigation bar above to jump between **Lineup**, **Game Mode**, "
        "**Add/Merge**, and **Export**."
    ).classes('p-4')

    # -------------------------
    # 💾 How to Save a Season
    # -------------------------
    ui.label('💾 How to Save a Season').classes('text-xl font-bold p-2')
    ui.markdown(
        "1. Go to the **📤 Export** page.\n"
        "2. Tap **Download Season JSON**.\n"
        "3. This file contains your entire season:\n"
        "   - All player stats\n"
        "   - Lineup order\n"
        "   - Last play info\n"
        "   - Fast Tap mode (tracking 1 or 2-player)\n"
        "4. Store it safely (Downloads, cloud drive, etc.)."
    ).classes('p-2')

    # -------------------------
    # 📁 How to Load a Season
    # -------------------------
    ui.label('📁 How to Load a Season').classes('text-xl font-bold p-2')
    ui.markdown(
        "1. Go to the **📤 Export** page.\n"
        "2. Upload your saved JSON file.\n"
        "3. The app restores:\n"
        "   - Player stats\n"
        "   - Lineup\n"
        "   - Fast Tap mode\n"
        "   - Last play info\n"
        "4. Continue scoring immediately."
    ).classes('p-2')

    # -------------------------
    # ⚡ Fast Tap & Lineup Behavior
    # -------------------------
    ui.label('⚡ Game (Fast Tap) & 👥 Lineup Behavior').classes('text-xl font-bold p-2')
    ui.markdown(
        "- Game Mode tracks stats for one or two players at a time.\n"
        "- +1 and +5 yard buttons for fast input.\n"
        "- Fast Tap works for Passing, Receiving, Rushing, and Defense.\n"
        "- **Undo Last Play** rolls back the most recent Fast Tap action.\n"
        "- Stats persist on your device — safe, private, and reliable even if your phone restarts."
    ).classes('p-2')

    # -------------------------
    # 📊 Exporting Stats
    # -------------------------
    ui.label('📊 Exporting Stats').classes('text-xl font-bold p-2')
    ui.markdown(
        "- Export **TXT** for readable summaries.\n"
        "- Export **CSV** for spreadsheets.\n"
        "- Export **JSON** for full season save/restore."
    ).classes('p-2')

    # -------------------------
    # 📘 Stat Acronyms & Definitions
    # -------------------------
    ui.label('📘 Stat Acronyms & Definitions').classes('text-xl font-bold p-2')
    ui.markdown(
        "### 🛡️ Defense\n"
        "- **FP** — Flag Pulls\n"
        "- **SK** — Sacks\n"
        "- **INT** — Interceptions\n"
        "- **PBU** — Pass Breakups\n"
        "- **SFTY** — Safety (2‑point defensive score)\n"
        "- **DTD** — Defensive Touchdown\n"
        "- **FF** — Forced Fumble\n\n"

        "### 🤲 Receiving\n"
        "- **REC** — Receptions\n"
        "- **RY** — Receiving Yards\n"
        "- **RTD** — Receiving Touchdowns\n\n"

        "### 🏃 Rushing\n"
        "- **RA** — Rush Attempts\n"
        "- **RY** — Rushing Yards\n"
        "- **RTD** — Rushing Touchdowns\n\n"

        "### 🎯 Passing\n"
        "- **PA** — Pass Attempts\n"
        "- **PC** — Pass Completions\n"
        "- **PY** — Passing Yards\n"
        "- **PTD** — Passing Touchdowns\n"
        "- **INT‑T** — Interceptions Thrown"
    ).classes('p-2')

    # -------------------------
    # 📐 Offensive Formulas
    # -------------------------
    ui.label('📐 Offensive Formulas').classes('text-xl font-bold p-2')
    ui.markdown(
        "- **Pass Completion %** = Completions ÷ Attempts\n"
        "- **Yards per Attempt** = Pass Yards ÷ Attempts\n"
        "- **Yards per Catch** = Rec Yards ÷ Receptions\n"
        "- **Total TDs** = Pass TD + Rec TD + Rush TD"
    ).classes('p-2')

    # -------------------------
    # 🛡️ Defensive / Flag Football Formulas
    # -------------------------
    ui.label('🛡️ Defensive / Flag Football Formulas').classes('text-xl font-bold p-2')
    ui.markdown(
        "- **Flag Pulls** = number of flags pulled\n"
        "- **Sacks** = QB pulled behind LOS\n"
        "- **INT** = interceptions\n"
        "- **PBU** = pass breakups\n"
        "- **Def TD** = defensive touchdowns\n"
        "- **Safety** = 2‑point defensive score\n"
        "- **Forced Fumble** = ball knocked loose"
    ).classes('p-2')

    # ---------------------------------------------------------
    # GLOBAL VERSION DOT (must be inside a page for older NiceGUI)
    # ---------------------------------------------------------
    def show_version():
        ui.notify('Version: 2026-01-05-2')

    dot = ui.button('•', on_click=show_version)
    dot.props('flat dense round')
    dot.classes(
        'fixed bottom-2 right-2 text-gray-300 text-xl '
        'cursor-pointer z-[9999] bg-transparent shadow-none'
    )




# ----------------------------------------
# Import subpages
# ----------------------------------------

import pages.lineup
import pages.game
import pages.export


# ----------------------------------------
# Run app
# ----------------------------------------

ui.run(
    host='0.0.0.0',
    port=8080,
    storage_secret='flagstats_2026_live',
    reload=False,
    workers=1
)