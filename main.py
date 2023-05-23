from onlinegame import OnlineGame
from localgame import LocalGame
import pygame as pg
from constants import *
import socket
from button import Button
from roommenu import RoomMenu

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption("Battleships game")
    background = pg.image.load(MENU_IMAGE_PATH)
    background = pg.transform.scale(background,(WIN_SIZE[0]//3*2,WIN_SIZE[1]))

    
    screen.blit(background,(0,0))
    buttons = [Button("Computer",WIN_SIZE[0]-WIN_SIZE[0]//3,WIN_SIZE[1]//4,(255,255,255),WIN_SIZE[0]//3,WIN_SIZE[1]//5),
               Button("Player",WIN_SIZE[0]-WIN_SIZE[0]//3,WIN_SIZE[1]//2,(255,255,255),WIN_SIZE[0]//3,WIN_SIZE[1]//5)]
    for btn in buttons:
        btn.draw(screen)
    pg.display.update()
    running = True
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    #     client_socket.connect((HOST,PORT))
    #     client_socket.send("Close".encode())
    # except ConnectionRefusedError:
    #     print("no server")



    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if buttons[0].click(pg.mouse.get_pos()): # game with computer
                    game = LocalGame(screen)
                    running = False
                elif buttons[1].click(pg.mouse.get_pos()): # game with other player
                    RoomMenu(screen)
                    running = False

