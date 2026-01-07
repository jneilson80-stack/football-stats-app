from nicegui import ui, app
import shared
import os

# ------------------------------------------------------------
# STATIC FILES (NiceGUI 1.4.18)
# ------------------------------------------------------------
app.add_static_files(
    url_path='/static',
    local_directory=os.path.join(os.path.dirname(__file__), 'static'),
)

# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------
@ui.page('/')
def home_page():
    shared.ensure_storage()
    shared.render_nav()
    shared.inject_global_styles()

    # ------------------------------------------------------------
    # BACKGROUND IMAGE (Home page only)
    # ------------------------------------------------------------
    ui.add_head_html("""
    <style>
        /* Desktop background image */
        @media (min-width: 901px) {
            body {
                background-image: url('/static/football.jpg');
                background-repeat: no-repeat;
                background-position: right center;
                background-size: 40%;
                background-attachment: fixed;
            }
        }

        /* Mobile: remove background image */
        @media (max-width: 900px) {
            body {
                background-image: none !important;
            }

            .mobile-footer-image {
                display: block;
                width: 100%;
                margin-top: 40px;
                text-align: center;
            }

            .mobile-footer-image img {
                width: 80%;
                max-width: 350px;
                opacity: 0.9;
                border-radius: 12px;
            }
        }

        /* Hide footer image on desktop */
        @media (min-width: 901px) {
            .mobile-footer-image {
                display: none;
            }
        }
    </style>
    """)

    # ------------------------------------------------------------
    # HERO HEADER
    # ------------------------------------------------------------
    ui.label("🏈").classes("text-7xl text-center mt-6")
    ui.label("Welcome to Fast Football Stats!").classes("text-4xl font-bold text-center mb-8")

    # ------------------------------------------------------------
    # INTRO
    # ------------------------------------------------------------
    ui.markdown(
        "This app is designed for **fast, reliable stat tracking** right at the field.\n\n"
        "Use the navigation bar above to jump between **Lineup**, **Game Mode**, "
        "**Add/Merge**, and **Export**."
    ).classes('p-4')

    # ------------------------------------------------------------
    # SAVE SEASON
    # ------------------------------------------------------------
    ui.label('💾 How to Save a Season').classes('text-xl font-bold p-2')
    ui.markdown(
        "1. Go to the **📤 Export** page.\n"
        "2. Tap **Download Season JSON**.\n"
        "3. This file contains your entire season:\n"
        "   - All player stats\n"
        "   - Lineup order\n"
        "   - Last play info\n"
        "   - Fast Tap mode (tracking 1 or 2-player)\n"
        "4. Store it safely."
    ).classes('p-2')

    # ------------------------------------------------------------
    # LOAD SEASON
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # FAST TAP
    # ------------------------------------------------------------
    ui.label('⚡ Game (Fast Tap) & 👥 Lineup Behavior').classes('text-xl font-bold p-2')
    ui.markdown(
        "- Game Mode tracks stats for one or two players.\n"
        "- +1 and +5 yard buttons for fast input.\n"
        "- Undo Last Play rolls back the most recent action.\n"
        "- Stats persist on your device."
    ).classes('p-2')

    # ------------------------------------------------------------
    # EXPORTING
    # ------------------------------------------------------------
    ui.label('📊 Exporting Stats').classes('text-xl font-bold p-2')
    ui.markdown(
        "- Export **TXT** for readable summaries.\n"
        "- Export **CSV** for spreadsheets.\n"
        "- Export **JSON** for full season save/restore."
    ).classes('p-2')

    # ------------------------------------------------------------
    # ACRONYMS
    # ------------------------------------------------------------
    ui.label('📘 Stat Acronyms & Definitions').classes('text-xl font-bold p-2')
    ui.markdown(
        "### 🛡️ Defense\n"
        "- FP — Flag Pulls\n"
        "- SK — Sacks\n"
        "- INT — Interceptions\n"
        "- PBU — Pass Breakups\n"
        "- SFTY — Safety\n"
        "- DTD — Defensive Touchdown\n"
        "- FF — Forced Fumble\n\n"

        "### 🤲 Receiving\n"
        "- REC — Receptions\n"
        "- RY — Receiving Yards\n"
        "- RTD — Receiving Touchdowns\n\n"

        "### 🏃 Rushing\n"
        "- RA — Rush Attempts\n"
        "- RY — Rushing Yards\n"
        "- RTD — Rushing Touchdowns\n\n"

        "### 🎯 Passing\n"
        "- PA — Pass Attempts\n"
        "- PC — Pass Completions\n"
        "- PY — Passing Yards\n"
        "- PTD — Passing Touchdowns\n"
        "- INT‑T — Interceptions Thrown"
    ).classes('p-2')

    # ------------------------------------------------------------
    # VERSION DOT
    # ------------------------------------------------------------
    def show_version():
        ui.notify('Version: 2026-01-05-2')

    dot = ui.button('•', on_click=show_version)
    dot.props('flat dense round')
    dot.classes(
        'fixed bottom-2 right-2 text-gray-300 text-xl '
        'cursor-pointer z-[9999] bg-transparent shadow-none'
    )

    # ------------------------------------------------------------
    # MOBILE FOOTER IMAGE
    # ------------------------------------------------------------
    with ui.row().classes('mobile-footer-image'):
        ui.image('/static/football.jpg')


# ------------------------------------------------------------
# IMPORT SUBPAGES (REQUIRED FOR ROUTES TO REGISTER)
# ------------------------------------------------------------
import pages.lineup
import pages.game
import pages.export


# ------------------------------------------------------------
# RUN APP
# ------------------------------------------------------------
ui.run(
    host='0.0.0.0',
    port=8080,
    storage_secret='flagstats_2026_live',
    reload=False,
    workers=1,
)