import pygame, sys, time
from button import Button
from grid import Grid
from gridGame import GridGame
import json

pygame.init()

# Fenêtre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")


BACKGROUND_IMAGES = {
    "normal": pygame.image.load("assets/fond.png"),
    "troll": pygame.image.load("assets/backkground.png"),
}

FONT_COLORS = {
    "normal": "deeppink",
    "troll": "orange",
}

BUTTON_COLORS = {
    "normal": {"base": "pink", "hover": "deeppink"},
    "troll": {"base": "gold", "hover": "orange"},
}

MUSICS = {
    "normal": "assets/normal.ogg",
    "troll": "assets/sunshine.ogg",
}

TITLES = {
    "normal": "DEMINEUR",
    "troll": "DES MINEURS"
}

THEME_KEYS = list(BACKGROUND_IMAGES.keys())
theme_index = 0
current_music = None


selected_difficulty = [0]

#Jouer musique
def play_music(theme):
    global current_music
    if current_music:
        current_music.stop()
    current_music = pygame.mixer.Sound(MUSICS[theme])
    current_music.play(-1)


#Police
def get_font(size):
    return pygame.font.Font("assets/norwester.otf", size)


#Texte
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


#Changer theme
def changer_theme():
    global theme_index
    theme_index = (theme_index + 1) % len(THEME_KEYS)
    play_music(THEME_KEYS[theme_index])


#Menu principal
def main_menu():
    bouton_secret_visible = False
    SECRET_KEY = pygame.K_t

    #Bouton secret
    SECRET_BUTTON = Button(image=None,pos=(1150, 650),text_input="SECRET",font=get_font(20),base_color="white",hovering_color="grey"
    )

    play_music(THEME_KEYS[theme_index])

    while True:
        #Mise à jour du fond et des couleurs
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        font_color = FONT_COLORS[current_theme]
        button_colors = BUTTON_COLORS[current_theme]

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Titre
        MENU_TEXT = get_font(100).render(TITLES[current_theme], True, font_color)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #Boutons PLAY et QUIT credit et les saves
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit.png"), pos=(640, 600),
                             text_input="QUIT", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        CREDIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 550),
                             text_input="CREDIT", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        SAVED_GAMES_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1080, 550),
                                    text_input="BEBETTER", font=get_font(75),
                                    base_color=button_colors["base"], hovering_color=button_colors["hover"])


        # Affichage des boutons
        for button in [PLAY_BUTTON, QUIT_BUTTON, CREDIT_BUTTON, SAVED_GAMES_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        #Affichage du bouton secret
        if bouton_secret_visible:
            SECRET_BUTTON.changeColor(MENU_MOUSE_POS)
            SECRET_BUTTON.update(SCREEN)

        options = ["Debutant(9x9)", "Avance(16x16)", "Expert(30x16)"]
        num_options = len(options)
        option_width = 350
        total_width = num_options * option_width
        start_x = (1280 - total_width) // 2

        draw_text("Selectionnez une difficulte", get_font(50), font_color, SCREEN, 640, 350)

        for i, (text, pos) in enumerate(zip(options, range(start_x, start_x + total_width, option_width))):
            button = Button(image=None, pos=(pos + option_width // 2, 425),
                            text_input=text, font=get_font(40),
                            base_color=button_colors["base"], hovering_color=button_colors["hover"])
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            if i == selected_difficulty[0]:
                # Position du cercle
                pygame.draw.circle(SCREEN, (0, 0, 0), (pos + option_width // 2 - 160, 430), 20)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == SECRET_KEY:
                    bouton_secret_visible = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if current_music:
                        current_music.stop()
                    credits_screen()
                if SAVED_GAMES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    load_saved_games()
                if bouton_secret_visible and SECRET_BUTTON.checkForInput(MENU_MOUSE_POS):
                    changer_theme()

                for i, pos in enumerate(range(start_x, start_x + total_width, option_width)):
                    if (MENU_MOUSE_POS[0] - (pos + option_width // 2)) ** 2 + (
                            MENU_MOUSE_POS[1] - 425) ** 2 <= 20 ** 2:
                        selected_difficulty[0] = i  # Met à jour la difficulté

        pygame.display.update()


#Decompte
def afficher_decompte():
    current_theme = THEME_KEYS[theme_index]
    for i in range(3, 0, -1):
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        draw_text(str(i), get_font(100), "black", SCREEN, 640, 360)
        pygame.display.flip()
        time.sleep(1)

def question(grid_content, elapsed_time, first_click_position):
    pseudo = ""
    saisie_active = True
    message = "Entrez votre pseudo :"

    font = pygame.font.Font(None, 40)

    background_snapshot = SCREEN.copy()

    while saisie_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Valider avec Entrée
                    saisie_active = False
                    enregistrer_pseudo(pseudo, grid_content, elapsed_time, first_click_position)  # Sauvegarde des données
                    main_menu()
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    pseudo += event.unicode

        SCREEN.blit(background_snapshot, (0, 0))  # Remet l'état du fond (invisible)

        texte = font.render(f"{message} {pseudo}", True, (0, 0, 0))
        SCREEN.blit(texte, (40, 50))

        pygame.display.update()

#fonction pour enregistrer le pseudo
def enregistrer_pseudo(pseudo,grid_content,elapsed_time,first_click_position):
    fichier_json = "pseudo_data.json"
    try:
        with open(fichier_json, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append({
        "pseudo": pseudo,
        "niveau": selected_difficulty[0],
        "temps": elapsed_time,
        "grille": grid_content,
        "first_click_position": first_click_position})
    with open(fichier_json, "w") as f:
        json.dump(data, f, indent=4)

#Jouer
def play():
    afficher_decompte()

    # Initialisation du timer
    start_time = time.time()

    print(f"Niveau de difficulté choisi: {['Debutant', 'Avance', 'Expert'][selected_difficulty[0]]}")

    # Créez une grille de jeu
    if selected_difficulty[0] == 0:
        grid =         Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720, mines_count=15)
    elif selected_difficulty[0] == 1:
        grid =         Grid(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720)
        gridGame = GridGame(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720, mines_count=45)
    else:
        grid =         Grid(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720)
        gridGame = GridGame(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720, mines_count=99)

    grid_content = grid.grid

    running = True
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        button_colors = BUTTON_COLORS[current_theme]

        # Chronomètre : Si le jeu est en cours, afficher le temps écoulé en secondes
        if running:
            elapsed_time = int(time.time() - start_time)  # Temps écoulé en secondes
            timer_text = get_font(35).render(f"Temps : {elapsed_time} s", True, "black")
            SCREEN.blit(timer_text, (1090, 40))  # Affiche le chronomètre en haut à gauche de l'écran

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Dessiner la grille avec les mines et les chiffres
        gridGame.draw(SCREEN)

        # Créer et dessiner le bouton RETOUR
        PLAY_BACK = Button(image=None, pos=(1185, 670),
                           text_input="RETOUR", font=get_font(60), base_color=button_colors["base"], hovering_color=button_colors["hover"])

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Détection de fin de partie (victoire ou défaite)
        if gridGame.game_over:
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(190, 360))
            SCREEN.blit(text, text_rect)
            running = False

        elif gridGame.victory:
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(190, 360))
            SCREEN.blit(text, text_rect)
            running = False
            question(grid_content, elapsed_time, gridGame.first_click_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si on clique sur le bouton RETOUR
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()


                if not gridGame.game_over and not gridGame.victory:
                    if event.button == 1:  # Clic gauche
                        cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                        if cell:  # Si une cellule a été cliquée
                            row, col = cell
                            if not gridGame.revealed[row][col]:
                                gridGame.changeValue(row, col, grid)

                    elif event.button == 3:  # Clic droit
                        cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                        if cell:
                            row, col = cell
                            gridGame.toggle_flag(row, col)

        pygame.display.update()


def credits_screen():
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Crédits")

    BG_COLOR = "black"
    FONT_COLOR = "white"

    font_large = pygame.font.Font(None, 70)
    font_small = pygame.font.Font(None, 50)


    logo_image = pygame.image.load("assets/riot.png")
    logo_image = pygame.transform.scale(logo_image, (500, 150))

    pygame.mixer.music.load("assets/skibidi.mp3")
    pygame.mixer.music.play(-1)

    # Crédits
    credits = [
        ("- STUDIOS -", "large"),
        ("AntiMajeur x Riot Games", "small"),
        ("- DEVS -", "large"),
        ("Celestin", "small"),
        ("Antonin", "small"),
        ("Mathys", "small"),
        ("Theo", "small"),
        ("- GRAPHISTES -", "large"),
        ("Chat j'ai pété", "small"),
        ("- TESTEURS -", "large"),
        ("Ines Gangsta", "small"),
        ("- SPECIAL THANKS -", "large"),
        ("Merci aux figurants mineurs d'avoir aidé ", "small"),
        ("au développement de ce projet", "small"),
    ]

    scroll_y = 720
    scroll_speed = 0.7

    # Boucle principale
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(BG_COLOR)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Détection clic sur le bouton RETOUR
                mouse_pos = pygame.mouse.get_pos()
                if retour_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Arrêter la musique des crédits
                    play_music(THEME_KEYS[theme_index])  # Relancer la musique du menu principal
                    return  # Retourner au menu principal


        logo_rect = logo_image.get_rect(center=(640, scroll_y - 200))  # Positionner un peu avant les crédits
        SCREEN.blit(logo_image, logo_rect)


        for i, (text, size) in enumerate(credits):
            if size == "large":
                text_surface = font_large.render(text, True, FONT_COLOR)
            else:
                text_surface = font_small.render(text, True, FONT_COLOR)


            text_rect = text_surface.get_rect(center=(640, scroll_y + i * 80))
            SCREEN.blit(text_surface, text_rect)


        scroll_y -= scroll_speed


        if scroll_y + len(credits) * 80 < -100:
            scroll_y = 720


        retour_font = pygame.font.Font(None, 40)
        retour_text = retour_font.render("RETOUR", True, "white")
        retour_rect = retour_text.get_rect(topright=(1250, 20))  # Positionné en haut-droite
        SCREEN.blit(retour_text, retour_rect)


        pygame.display.flip()
        clock.tick(60)

#fonction pour charger une partie enregistree
def load_saved_games():
    fichier_json = "pseudo_data.json"
    try:
        with open(fichier_json, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    while True:
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        button_colors = BUTTON_COLORS[current_theme]

        draw_text("Parties Enregistrees", get_font(50), "black", SCREEN, 640, 50)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(650, 650), text_input="RETOUR", font=get_font(75), base_color=button_colors["base"], hovering_color=button_colors["hover"])

        BACK_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)


        y_offset = 150
        buttons = []
        for i, game in enumerate(data):
            pseudo = game["pseudo"]
            niveau = ["Debutant", "Avance", "Expert"][game["niveau"]]
            temps = game["temps"]


            draw_text(f"{pseudo} - {niveau} - {temps}s", get_font(30), "black", SCREEN, 640, y_offset)


            replay_button = Button(image=None,pos=(1000, y_offset), text_input="REJOUER", font=get_font(30), base_color="green", hovering_color="darkgreen")
            replay_button.changeColor(MENU_MOUSE_POS)
            replay_button.update(SCREEN)
            buttons.append((replay_button, game))
            y_offset += 70


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                for button, game in buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        replay_game(game)  # Rejouer la partie

        pygame.display.update()


def replay_game(game):
    start_time = time.time()  # Début du chronomètre

    grid_content = game["grille"]
    niveau = game["niveau"]
    elapsed_time = game["temps"]

    # Configure la grille et GridGame en fonction du niveau
    if niveau == 0:
        grid = Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720, mines_count=15,
                            is_replay=True)
    elif niveau == 1:
        grid = Grid(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720)
        gridGame = GridGame(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720, mines_count=45,
                            is_replay=True)
    else:
        grid = Grid(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720)
        gridGame = GridGame(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720, mines_count=99,
                            is_replay=True)
    grid.grid = grid_content  # Charger la grille sauvegardée
    gridGame.replay_first_click_position = tuple(
        game["first_click_position"])
    running = True

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        print(PLAY_MOUSE_POS)
        gridGame.draw(SCREEN)

        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1185, 670),
                           text_input="RETOUR", font=get_font(60), base_color="lemonchiffon", hovering_color="deeppink")

        PLAY_BACK.changeColor(pygame.mouse.get_pos())
        PLAY_BACK.update(SCREEN)
        if running:
            elapsed_time = int(time.time() - start_time)
            timer_text = get_font(35).render(f"Temps : {elapsed_time} s", True, "black")
            SCREEN.blit(timer_text, (1090, 40))

        if gridGame.game_over:
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(190, 360))
            SCREEN.blit(text, text_rect)
            running = False

        elif gridGame.victory:
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(190, 360))  #
            SCREEN.blit(text, text_rect)
            running = False
            question(grid_content, elapsed_time, first_click_position)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Détecter les clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                # Gestion des clics sur la grille
                if not gridGame.game_over and not gridGame.victory:
                    if gridGame.is_replay and gridGame.replay_first_click_position:
                        cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                        if cell == gridGame.replay_first_click_position:
                            row, col = cell
                            gridGame.changeValue(row, col, grid)
                            gridGame.replay_first_click_position = None
                    elif not gridGame.replay_first_click_position:
                        if event.button == 1:
                            cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                            if cell:
                                row, col = cell
                                if not gridGame.revealed[row][col]:
                                    gridGame.changeValue(row, col, grid)

                        elif event.button == 3:
                            cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                            if cell:
                                row, col = cell
                                gridGame.toggle_flag(row, col)

        pygame.display.update()
#Lancement menu
main_menu()
