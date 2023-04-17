from game import Game
import pygame as pg
from constants import *
import socket

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption("Battleships game")
    background = pg.image.load(MENU_IMAGE_PATH)
    background = pg.transform.scale(background,(WIN_SIZE[0]//3*2,WIN_SIZE[1]))

    button = pg.image.load('assets/buttons/button.png')
    button = pg.transform.scale(button,(WIN_SIZE[0]//3,WIN_SIZE[0]//3))

    button_rect = button.get_rect()
    button_width = button.get_width()
    button_rect.center = (WIN_SIZE[0] - button_width//2,WIN_SIZE[1]//2)
    
    screen.blit(background,(0,0))
    screen.blit(button,button_rect)
    pg.display.update()
    running = True
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    #     client_socket.connect((HOST,PORT))
    #     client_socket.send("Close".encode())
    # except ConnectionRefusedError:
    #     print("no server")

    # TODO Piotr zrobić menu głowne (wybór czy chcemy z komputerem czy z przeciwnikiem)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pg.mouse.get_pos()):

                    game = Game(screen,'computer')

                    # client_socket.close()
                    running = False

