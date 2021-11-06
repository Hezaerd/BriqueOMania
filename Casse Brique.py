# ---  Swann ROUANET T01 & Raphael DAUBELCOUR T01 --- #

# Les librairies qu'on utilise sont : Pygame, system et random
import pygame, sys, random, os
from pygame.locals import *

# Setup general
pygame.init()
fps = pygame.time.Clock()

#global
balle_rayon=15

pad_largeur=100
pad_hauteur=8
pad_vel=0

brique_x = 30
brique_y = 55
brique_largeur=70
brique_hauteur=20
brique_liste = []
liste_tempo = []

score = 0
lives = 4

#Couleurs
couleurs = [(200,200,200),(0,0,0)] # | couleurs[0] = Gris Clair | couleurs[1] = Noir |
bg_couleur = pygame.Color('grey11') # La couleur utilisé pour le fond de la fenetre est un gris prédéfini par pygame


balle_vitesse_x = 3 # La vitesse horizontal de départ de la balle est de 3 pixels par image
balle_vitesse_y = -3 # La vitesse vertical de la balle est de -3 pixels par image (-3 pour que la balle se dirige vers le bas)

# Fenetre
fenetre_largeur=800
fenetre_hauteur=600
screen = pygame.display.set_mode((fenetre_largeur, fenetre_hauteur),0,0) # On créer notre fenetre qui s'appelle screen
pygame.display.set_caption('BriqueOMania') # on change le nom de la fenetre


# On créer les "rectangles" des objets
balle = pygame.Rect(fenetre_largeur/2 - balle_rayon/2,fenetre_hauteur/2 - balle_rayon/2 - balle_rayon/2,balle_rayon,balle_rayon)
pad = pygame.Rect(fenetre_largeur/2 - pad_largeur/2,fenetre_hauteur-(pad_hauteur+3),pad_largeur,pad_hauteur)

started = False
CarryOn = False

# -- Gestion du menu démarer
def start_game():
    ''' On ne commence pas la partie temps que le joueur n'appuie sur la touche espace, pour ne pas que la partie défile à l'insu de l'utilisateur'''
    global CarryOn
    PC_info()
    screen.fill(bg_couleur) # On remplit le fond de gris clair,
    font = pygame.font.SysFont("Ailerons-Regular.otf", 35) # On définie la police d'écriture sur celle choisis
    text = font.render("ESPACE pour commencer", 1, couleurs[0]) # On créer le texte
    screen.blit(text, (245,200)) # On affiche le texte 
    text = font.render("ECHAP pour quitter", 1, couleurs[0]) # On créer le texte
    screen.blit(text, (270,350)) # On affiche le texte
    pygame.display.flip() # On actualise la fenetre
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE: # Si le joueur appuie sur espace, on la quite la boucle du début et on rentre dans la boucle principal
                CarryOn = not(CarryOn)
            if event.key == pygame.K_ESCAPE: # Si le joueur appuie sur echap, il ferme la fenetre et quite pygame
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

# -- Gestion de la balle
def balle_animation():
    ''' On gère les colisions & les déplacements de la balle. '''
    global balle_vitesse_x, balle_vitesse_y
    balle.x += balle_vitesse_x
    balle.y += balle_vitesse_y

    if balle.top <= 35: #Si le haut de la balle dépasse la ligne du haut, elle rebondit dans le sens inverse
        balle_vitesse_y *= -1
    elif balle.left <= 0 or balle.right >= fenetre_largeur: #Si la balle touche la droite ou la gauche de l'ecran elle rebondit
        balle_vitesse_x *= -1
    elif balle.colliderect(pad): # la balle rebondit si elle touche le pad
        balle_vitesse_y *= -1
    elif balle.bottom >= fenetre_hauteur: # On teleporte la balle au centre de l'ecran dirigé vers le haut et de façon aléatoire la droite ou la gauche
        balle_restart()
    collision_brique()

def balle_restart():
    ''' On remet la balle au milieu, dans une direction aléatoire et on enleve une vie  '''
    global balle_vitesse_y, balle_vitesse_x, lives, CarryOn
    if lives > 0: # Si le joueur à une ou plusieurs vie, on lui enlève 1
        lives -= 1
        balle.center = (fenetre_largeur/2, fenetre_hauteur/2) # On teleporte la balle au centre
        balle_vitesse_y *= -1 # On inverse sa vitesse sur l'axe vertical
        balle_vitesse_x *= random.choice((1,-1)) # On lui donne une vitesse aléatoire sur l'axe horizontal
    else: # Cependant, si il en a plus, on affiche le message de défaite et on ferme la fenetre
        lives = 0
        loose(screen)
        CarryOn = False

# -- Gestion du pad
def pad_animation():
    ''' On gère les colisions du pad sur les bords de l'écran '''
    pad.x += pad_vel
    if pad.left <= 0: # Si le pad depasse à gauche, on le teleporte au bord
        pad.left = 0
    if pad.right >= fenetre_largeur: # Si il depasse à droite, on le teleporte sur le bord
        pad.right = fenetre_largeur

# -- Gestion des dessins à l'écran
def draw(screen):
    ''' On dessine les éléments qui sont à l'écran '''
    screen.fill(bg_couleur)
    pygame.draw.ellipse(screen, couleurs[0], balle)
    pygame.draw.rect(screen, couleurs[0], pad)
    pygame.draw.aaline(screen, couleurs[0], (0,35), (fenetre_largeur,35))

# -- Gestion affichage user informations
def PC_info():
    ''' On change le nom de la fenetre a BriqueOMania (nom du projet) suivis du nombre de fps de la fenetre '''
    pygame.display.set_caption('BriqueOMania   %d fps' % fps.get_fps())

def player_stats(screen,hauteur_text):
    ''' On affiche le score et la vie du joueur en haut de l'écrant.
    Screen est la fenetre d'affichage.
    hauteur_text est la hauteur du texte '''
    font = pygame.font.SysFont("Ailerons-Regular.otf", 34) # On définie la police d'écriture sur celle choisis
    text = font.render("Score: " + str(score), 1, couleurs[0]) # On créer 
    screen.blit(text, (20,hauteur_text))
    text = font.render("Vies restante: " + str(lives), 1, couleurs[0])
    screen.blit(text, (600,hauteur_text))

def loose(screen):
    '''Permet d'afficher un message de défeche. Screen est la fenetre sur laquelle c'est affiché'''
    font = pygame.font.SysFont("Ailerons-Regular.otf", 74) # On définie la police d'écriture sur celle choisis
    text = font.render("PERDU", 1, couleurs[0]) # On créer le texte "Perdu" en gris clair
    screen.blit(text, (300,275)) # On affiche le texte sur la fenetre
    pygame.display.flip() # On actualise la fenetre
    pygame.time.wait(3000) # On attend 3 secondes avant de reprendre le programme

def win(screen):
    '''Permet d'afficher un message de victoire. Screen est la fenetre sur laquelle c'est affiché'''
    font = pygame.font.SysFont("Ailerons-Regular.otf", 74) # On définie la police d'écriture sur celle choisis
    text = font.render("PARTIE FINI", 1, couleurs[0]) # On créer le texte "Perdu" en gris clair
    screen.blit(text, (200,300)) # On affiche le texte sur la fenetre
    pygame.display.flip() # On actualise la fenetre
    pygame.time.wait(3000) # On attend 3 secondes

# -- Gestion des briques
def creer_brique(screen):
    ''' On créer les rectangles des briques et on les ajoutes dans une liste pour pouvoir les manipuler facilement'''
    global brique_x, brique_y, brique_liste, liste_tempo
    ligne = 0 # Ligne correspond au nombre de ligne de brique deja dessiné
    while ligne <= 0: # Tant qu'il y a 4 lignes ou moins, on en rajoute une
        for colonne in range(11): # On repete la 
            brique = pygame.Rect(brique_x, brique_y ,brique_largeur, brique_hauteur) # On définie les propriétés d'une brique
            brique_x += 77 # On ajoute 77 pixels (largeur de la brique + un espace) pour la prochaine brique
            brique_liste.append(brique) # On ajoute cette brique dans une liste 
        brique_x = 30 # Quand la ligne est fini, on remet le brique_x sur la gauche 
        brique_y += 30 # Quand la ligne est fini, on ajoute 30 pixel vers le bas (hauteur de la brique + un espace)
        ligne += 1 # On passe a la ligne suivante
    afficher_brique(screen) 

def afficher_brique(screen):
    ''' On dessine chaque briques qui sont présente dans la liste brique_list '''
    global brique_liste
    for i in brique_liste:
        pygame.draw.rect(screen, couleurs[0], i) # On dessine la brique i qui est dans la liste créer dans la fonction creer_brique

def collision_brique():
    ''' Quand la balle touche une brique, elle repart (théoriquement) dans le sens inverse et en ajoutant 1 point au score '''
    global  brique_x, brique_y, brique_liste, score, balle_vitesse_y
    for i in brique_liste:
        if balle.colliderect(i): # Si la balle rentre en collision avec une des briques
            balle_vitesse_y *= -1 # On inverse sa vitesse verticale
            brique_liste.pop(brique_liste.index(i)) # On enleve la brique de la liste
            score += 1 # On incremente le score de 1
            afficher_brique(screen) # On affiche a nouveau les briques
        

# ------- Lancement de la partie -------
while not(CarryOn):
    start_game()

# ------- BOUCLE PRINCIPAL -------
while CarryOn:

    if not(started):
        creer_brique(screen)
        started = not(started)

    #Entrées commandes
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT: #Si la touche "fleche gauche" est appuyé, le pad va vers la gauche
                pad_vel -= 7
            if event.key == pygame.K_RIGHT: #Si la touche "fleche droite" est appuyé, le pad va vers la droite
                pad_vel += 7
            if event.key == pygame.K_ESCAPE: # Si la touche "Echape" est appuyé, on sort de la boucle, ce qui met fin au programme
                CarryOn = False

        if event.type == KEYUP:
            if event.key == pygame.K_LEFT: #Si on releve la fleche gauche, on remet la vitesse du pad à 0 (-7 + 7 = 0)
                pad_vel += 7
            if event.key == pygame.K_RIGHT: #Si on releve la fleche droite, on remet la vitesse du pad à 0 (7 - 7 = 0)
                pad_vel -= 7

        if event.type == QUIT: #Si on ferme en cliquant sur la croix, on sort de la boucle principal.
            CarryOn = False

    draw(screen)
    afficher_brique(screen)
    PC_info()
    player_stats(screen,9)
    balle_animation()
    pad_animation()

    # Actualiser la fenetre
    pygame.display.flip()
    if score == 10:
            win(screen)
            CarryOn = False
    fps.tick(120) # La boucle l'imite l'ordinateur à un maximum de 120 rafraichissements par seconde

pygame.quit()
sys.exit()