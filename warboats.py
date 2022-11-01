import numpy as np
import random as rand
import tkinter as tk
import random
import time
from functools import partial

#This code works, but is not great, as it uses a large amount of brute force (Especially to place the ships)
# There is also a massive amount of redundant code due to the different storage methods for the boards (also because I was lazy)
#  
    # EM = Empty
    # HT = Hit
    # -- = Unkown
    # 
    # B(C1) = Boat (Letter and Number after b signifies which boat it is): 
        # A = Aircraft Carrier (Length = 6, Available = 1)
        # C = Cruiser (Length = 5, Available = 1)
        # B = Battleship (Length = 4, Available = 2)
        # S = Submarine (Length = 3, Available = 1)
        # R = Repair (Length = 2, Available = 1)
    # (BC1)H = H after the boat/empty square signifys a hit

# [Ship name, Length, health, destroyed]
# Submarine [4] is orientation| True is Vertical, False is Horizontal
player_ships = [["AIR", 6, 6, False], ["CRU", 5, 5, False], ["B1", 4, 4, False], ["B2", 4, 4, False], ["SUB", 3, 3, False, None], ["REP", 2, 2, False]]
ship_key = {
    "AIR" : 0,
    "CRU" : 1, 
    "SUB" : 4,
    "REP" : 5,
    "AI" : 0,
    "CR" : 1, 
    "B1" : 2,
    "B2" : 3,
    "SU" : 4,
    "RE" : 5
}
computer_ships = [["AIR", 6, 6, False], ["CRU", 5, 5, False], ["B1", 4, 4, False], ["B2", 4, 4, False], ["SUB", 3, 3, False, None], ["REP", 2, 2, False]]
known_locations = []
possible_locations = []
# [turns until available, cost turns to be available]
# [Big Missile, Sonar, Plane flyover]
powerup_wait = [[0,6],[0,7],[0,6]] 
comp_powerup_wait = [[0,6],[0,7],[0,6]] 

comp_board = np.full((16,16), "--")
comp_map = np.full((16,16), "--")

"""
Comp map key

HT = Hit
KN = Known
Em = Empty
-- = Unknown
"""

def create_board():
    #global button
    for r in range(16):
            for c in range(16):
                player_board.append(tk.Button(win, text="--", borderwidth=1, bg="#4ccdf5", height=2, width=4, command=partial(action, r, c)))
                player_board[-1].grid(row=r,column=c)
    for r in range(16):
            for c in range(16):
                player_map.append(tk.Button(win, text="--", borderwidth=1, bg="#4ccdf5", height=2, width=4, command=partial(map_action, r, c)))
                player_map[-1].grid(row=r,column=c+19)

def computer_place_ship():
    ships_placed = 0
    while ships_placed < len(computer_ships):
        
        orientation = random.randint(0,1) # True = "Vertical"
        x = random.randint(0,15)
        y = random.randint(0,15)
        if orientation == True: # Oriented Vertically 
            blocking_ship = 0
            for i in range(computer_ships[ships_placed][1]): #Checks collisions
                if comp_board[x-i][y] != "--":
                    blocking_ship = True
                    break
            if x - computer_ships[ships_placed][1] < -1 or blocking_ship == True: 
                print("FALSE")

            else:
                if ships_placed == 4:
                    computer_ships[4][4] = False
                for i in range(computer_ships[ships_placed][1]): 
                    comp_board[x-i][y] = computer_ships[ships_placed][0]
                ships_placed += 1
        
        elif orientation == False: #Horizontal
            blocking_ship = 0
            for i in range(computer_ships[ships_placed][1]): #Checks collisions
                if comp_board[x][y-i] != "--":
                    blocking_ship = True
                    break
            if y - computer_ships[ships_placed][1] < -1 or blocking_ship == True: 
                print("FALSE")

            else:
                if ships_placed == 4:
                    computer_ships[4][4] = True
                for i in range(computer_ships[ships_placed][1]): 
                    comp_board[x][y-i] = computer_ships[ships_placed][0]
                ships_placed += 1
            


        print(comp_board, "\n")
    print("Placed all ships")
    
def place_ship(r, c):
    global selected_ship
    if hor_ver["text"] == "Vertical":
        orientation = True # True = "Vertical"
    else:
        orientation = False #False = "Horizontal"

    
    if orientation == True: # Oriented Vetically
        
        blocking_ship = False
        print(player_ships[selected_ship][1])
        for i in range(player_ships[selected_ship][1]): #Checks collisions
            if player_board[((r-i)*16)+ c]["text"] != "--":
                blocking_ship = True
                break
        if r - player_ships[selected_ship][1] < -1 or blocking_ship == True: #Checks if it intersects with wall
            print("FALSE")

        else:
            if selected_ship == 4:
                    player_ships[4][4] = True
            for i in range(player_ships[selected_ship][1]): #
                player_board[((r-i)*16)+ c]["text"] = player_ships[selected_ship][0]
                player_board[((r-i)*16)+ c]["bg"] = "grey"

            selected_ship += 1

    elif orientation == False: #Horizontal

        blocking_ship = False
        
        for i in range(player_ships[selected_ship][1]): #Checks collisions
            if player_board[((r)*16)+ c-i]["text"] != "--":
                blocking_ship = True
                break
        if c - player_ships[selected_ship][1] < -1 or blocking_ship == True: 
            print("FALSE")

        else:
            if selected_ship == 4:
                    player_ships[4][4] = False
            for i in range(player_ships[selected_ship][1]): #
                player_board[((r)*16)+ c-i]["text"] = player_ships[selected_ship][0]
                player_board[((r)*16)+ c-i]["bg"] = "grey"

            selected_ship += 1

def toggle(): #Toggles horizontal or vertical place ship button
    if hor_ver["text"] == "Horizontal":
        hor_ver["text"] = "Vertical"
    else: 
        hor_ver["text"] = "Horizontal"

def reset_placement(): #restarts the placement of ships if the reset button clicked
    global selected_ship
    for button in player_board:
        button["text"] = "--"
        button["bg"] = "#4ccdf5"
    selected_ship = 0

def ready():
    global selected_ship
    if selected_ship == len(player_ships): #Checks if all the ships have been placed
        selected_ship += 1
        hor_ver.grid_forget()
        reset_placement_btn.grid_forget()
        ready_btn.grid_forget()
        # Show all the option buttons
        turn_lbl.grid(row=1, column=17, columnspan=2) 
        missile.grid(row=3, column=17, columnspan=2) 
        large_missile.grid(row=4, column=17, columnspan=1) 
        sonar.grid(row=5, column=17, columnspan=1) 
        plane_flyover.grid(row=6, column=17, columnspan=1) 
        large_missile_lbl.grid(row=4, column=18, columnspan=1) 
        sonar_lbl.grid(row=5, column=18, columnspan=1) 
        plane_flyover_lbl.grid(row=6, column=18, columnspan=1) 


        rand_func = True #random.randint(0,1) #Random player starts
        if rand_func == True:  
            player_turn() 
        else: 
            computer_turn() 

def player_turn(): 
         
    for powerup in powerup_wait:
        if powerup[0] != 0:
            powerup[0] -= 1
    missile["state"] = "normal"
    large_missile["state"] = "normal"
    sonar["state"] = "normal"
    plane_flyover["state"] = "normal"
    large_missile_lbl["text"] = powerup_wait[0][0]
    sonar_lbl["text"] = powerup_wait[1][0]
    plane_flyover_lbl["text"] = powerup_wait[2][0]

    turn_lbl["text"] = "Your Turn" 
    for button in player_board:
        button["state"] = "normal"
    for button in player_map:
        button["state"] = "normal"
    win.update_idletasks()
    print("player turn")

def computer_turn():  
    global player_board, player_map, player_ships, comp_powerup_wait
    for powerup in comp_powerup_wait:
        if powerup[0] != 0:
            powerup[0] -= 1
    missile["state"] = "disabled"
    large_missile["state"] = "disabled"
    sonar["state"] = "disabled"
    plane_flyover["state"] = "disabled"
    turn_lbl["text"] = "Computer Turn"
    for button in player_board:
        button["state"] = "disabled"
    for button in player_map:
        button["state"] = "disabled"
    win.update_idletasks()
    print("computer turn")

    choice = random.randint(0,1) #Random True or false
    print(known_locations)
    if choice == True: # Fire Missile
        print("Computer fire missile")              
        r, c = comp_get_rc(True, False)
        computer_fire(r,c, True)
        
    else: # Use Powerup
        print("Computer Powerup")
        computer_action()
    check_victory(player_ships, "Compter")
    win.update_idletasks()
    time.sleep(0.1)
    player_turn()

def check_victory(ships, current_player):
    x = 0
    for boats in ships:
        if boats[3] == False: #Stops the loops when a ship is not destroyed
            break
        x += 1
    if x == len(ships):
        print(f"GAME OVER - Winner {current_player}")
        selected_action = tk.IntVar()
        missile.grid_forget()
        large_missile.grid_forget()
        sonar.grid_forget()
        plane_flyover.grid_forget()
        
        large_missile_lbl.grid_forget()
        sonar_lbl.grid_forget()
        plane_flyover_lbl.grid_forget()

        for button in player_board:
            button["state"] = "disabled"
        for button in player_map:
            button["state"] = "disabled"
        winner_lbl["text"] = f"GAME OVER - Winner {current_player}"
        winner_lbl.grid(row=4,column=17, columnspan=2)
        time.sleep(0.1)
        win.update_idletasks()
        
        #quit()

def comp_get_rc(remove, rand_loc): #Gets a location to fire into |Remove is if you should remove from the known and possible value arrays | Rand_loc is if to get a value / loc from the known/pos arrays
    if len(known_locations) > 0 and rand_loc == False: #First finds a location it is certain of.
        r,c = known_locations[0]
        if remove == True or comp_map[r][c] != "--":
            known_locations.pop(0)
    elif len(possible_locations) > 0 and rand_loc == False: # If it is not certain of any location, then checks possible locations
        r,c = possible_locations[0]
        if remove == True or comp_map[r][c] != "--":
            possible_locations.pop(0)
    else: #If no possible or certain locations, get random location
        r = random.randint(0,15)
        c = random.randint(0,15)
    if comp_map[r][c] == "EM": #The square is known to be empty
        return comp_get_rc(remove, False) #It is set to false to avoid max recursion depth
    return r, c

def computer_fire(r,c, refire):
    global player_board, player_ships, comp_map, possible_locations
    if player_board[(r*16)+c]["text"] != "--": #Checks if a ship is in the square
        print(player_board[(r*16)+c]["text"])
        if player_ships[ship_key[player_board[(r*16)+c]["text"]]][3] == True: #Ship destroyed
            r, c = comp_get_rc(True, False)
            if refire == True:
                computer_fire(r,c, True)   
        elif player_board[(r*16)+c]["bg"] == "red" or player_board[(r*16)+c]["bg"] == "white":
            print("Ship already hit")
            r, c = comp_get_rc(True, False)
            if refire == True:
                computer_fire(r,c, True)
            
        else:
            print("Hit")
            player_board[(r*16)+c]["bg"] = "red"
            comp_map[r][c] = "HT"
            
            horiz_vert = 0 #0 = unkown, 1 = Horizontal, 2 = Vertical 
            num = 0 # To see how much to pop from possible_locations list if vertical
            num2 = 0
            if r-1 != -1: #Is r-1 a valid locaion on the board, ensures no out of range errors
                if comp_map[r-1][c] == "--" or comp_map[r-1][c] == "EM": #is that square empty as we don't want to have an already hit location be possible
                    possible_locations.append([r-1, c])
                    num += 1
                else:
                    horiz_vert = 2
                    
            if r+1 != 16:
                if comp_map[r+1][c] == "--" or comp_map[r+1][c] == "EM":
                    possible_locations.append([r+1, c])
                    num += 1
                else:
                    horiz_vert = 2
                    
            if c-1 != -1:
                if (comp_map[r][c-1] == "--" or comp_map[r][c-1] == "EM") and horiz_vert != 2:
                    possible_locations.append([r, c-1])
                    num2 += 1
                elif horiz_vert != 2:
                    horiz_vert = 1
            if c+1 != 16:
                if (comp_map[r][c+1] == "--" or comp_map[r][c+1] == "EM") and horiz_vert != 2:
                    possible_locations.append([r, c+1])
                    num2 += 1 
                elif horiz_vert != 2: 
                    horiz_vert = 1
            if horiz_vert == 1:
                for i in range(num):
                    possible_locations.pop(-1 - num2)

               
            player_ships[ship_key[player_board[(r*16)+c]["text"]]][2] -= 1 #Reduces its health
            if player_ships[ship_key[player_board[(r*16)+c]["text"]]][2] == 0: #checks if ship is destroyed
                print("SHIP DESTROYED")
                player_ships[ship_key[player_board[(r*16)+c]["text"]]][3] = True
            
    else: #No ship
        if player_board[(r*16)+c]["bg"] == "red" or player_board[(r*16)+c]["bg"] == "white":
            print("Square already hit")
            r, c = comp_get_rc(True, False)
            if refire == True:
                computer_fire(r,c, True)     

        print("Miss \n")
        player_board[(r*16)+c]["bg"] = "white"
        comp_map[r][c] = "EM"

    win.update_idletasks()

def fire(r,c):
    global comp_board, computer_ships, ship_key, player_map
    if comp_board[r][c] != "--": #Checks if a ship is in the square
        if computer_ships[ship_key[comp_board[r][c]]][3] == True: #Ship destroyed
            print("Ship already destroyed")
        elif player_map[(r*16)+c]["bg"] == "red":
            print("Ship already hit")
        else:
            print("Hit")
            player_map[(r*16)+c]["bg"] = "red"
            computer_ships[ship_key[comp_board[r][c]]][2] -= 1 #Reduces its health
            if computer_ships[ship_key[comp_board[r][c]]][2] == 0: #checks if ship is destroyed
                print("SHIP DESTROYED")
                computer_ships[ship_key[comp_board[r][c]]][3] = True
            

    else: #No ship
        print("Miss \n")
        player_map[(r*16)+c]["bg"] = "white"
    check_victory(computer_ships, "PLAYER")

def computer_action():
    global comp_powerup_wait, computer_ships
    comp_action = random.randint(1,3)

    if comp_action == 1: #Large Missile
        r, c = comp_get_rc(True, False)
        
        if comp_powerup_wait[0][0] == 0 and comp_map[r][c] == "--" :
            print("Fire Large Missile")
            comp_powerup_wait[0][0] = int(comp_powerup_wait[0][1]) #Changes the value so the powerup can only be used so many turns (The const wait value is powerup_wait[x][1])
            
            computer_fire(r,c, False)
            if r-1 != -1 and c-1 != -1:
                computer_fire(r-1,c-1, False)
            if r - 1 != -1:
                computer_fire(r-1,c, False)
            if c -1 != -1:
                computer_fire(r,c-1, False)
            
        else:
            print("Still need to wait")
            computer_fire(r,c, True)

    elif comp_action == 2: # SONAR
        r, c = comp_get_rc(False, True)
        print("Sonar")
        if comp_powerup_wait[1][0] == 0:
            comp_powerup_wait[1][0] = int(comp_powerup_wait[1][1]) #Changes the value so the powerup can only be used so many turns (The const wait value is powerup_wait[x][1])
            if computer_ships[4][4] == True: #Checks sub orientation
                print("Sub vertical")
                
                if r < 8: #set sonar up for different map sides
                    start = 0
                    end = random.randint(5,15)
                    increment = 1
                else:
                    start = 15
                    end = random.randint(0,10)
                    increment = -1
                for dist in range(start,end,increment): #Loops for the range of the sonar
                    if player_board[(dist*16)+c]["text"] == "--": # Empty
                        comp_map[dist][c] = "EM"
                    else: #Ship in that square
                        if comp_map[dist][c] == "HT": #Already hit
                            break
                        else: # New find
                            known_locations.append([dist,c])
                            break # Sonar ends when ship has been found
            else:
                print("Sub Horizontal")
                
                if c < 8: #set sonar up for different map sides
                    start = 0
                    end = random.randint(5,15)
                    increment = 1
                else:
                    start = 15
                    end = random.randint(0,10)
                    increment = -1
                for dist in range(start,end,increment): #Loops for the range of the sonar
                    if player_board[(r*16)+dist]["text"] == "--": # Empty
                        comp_map[r][dist] = "EM"
                    else: #Ship in that square
                        if comp_map[r][dist] == "HT": #Already hit
                            break
                        else: # New find
                            known_locations.append([r,dist])
                            break # Sonar ends when ship has been found
            
        else:
            print("Still need to wait")
            r, c = comp_get_rc(False, False)
            computer_fire(r,c, True)

    elif comp_action == 3: # Plane Flyover
        
        if comp_powerup_wait[2][0] == 0:
            comp_powerup_wait[2][0] = int(comp_powerup_wait[2][1])
            print("Plane Flyover")
            kill_plane = 4#random.randint(1,6)
            if kill_plane != 5:
                r, c = comp_get_rc(False, True)
                #Main square
                if player_board[(r*16)+c]["text"] == "--":
                    comp_map[r][c] = "EE"
                else:
                    known_locations.append([r,c])
                
                if r-1 != -1 and c-1 != -1: #Top Left
                    x = r-1
                    y = c-1
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EE"
                    else:
                        known_locations.append([x,y])


                if r+1 != 16 and c+1 != 16: #Bottom right
                    x = r+1
                    y = c+1
                    if player_board[(x*16)+y]["text"] == "--":
                       
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if r-1 != -1 and c+1 != 16: #Top Right
                    x = r-1
                    y = c+1
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if r+1 != 16 and c-1 != -1: #Bottom Left
                    x = r+1
                    y = c-1
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if r-1 != -1: #Left
                    x = r-1
                    y = c
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if r+1 != 16: #Right
                    x = r+1
                    y = c
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if c-1 != -1: #Down
                    x = r
                    y = c-1
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])

                if c+1 != 16: #Up
                    x = r
                    y = c+1
                    if player_board[(x*16)+y]["text"] == "--":
                        comp_map[x][y] = "EM"
                    else:
                        known_locations.append([x,y])
            else:
                print("Plane destroyed")
                comp_powerup_wait[2][0] = int(comp_powerup_wait[2][1]) * 2 + 1 #Greatly increases wait time if plane is destroyed
        else:
            print("Still need to wait")
            r, c = comp_get_rc(False, False)
            computer_fire(r,c, True)

def map_action(r,c):
    global selected_ship, selected_action
    print("\n")
    if selected_ship > len(player_ships): #still placing ships so can't do an action
        if selected_action.get() == 1: #Missile    
            print("Fire Missile")
            fire(r,c)
            computer_turn()

        elif selected_action.get() == 2: #Large Missile
            if powerup_wait[0][0] == 0:
                print("Fire Large Missile")
                powerup_wait[0][0] = int(powerup_wait[0][1]) #Changes the value so the powerup can only be used so many turns (The const wait value is powerup_wait[x][1])
                fire(r,c)
                if r-1 != -1 and c-1 != -1:
                    fire(r-1,c-1)
                if r - 1 != -1:
                    fire(r-1,c)
                if c -1 != -1:
                    fire(r,c-1)
    
                computer_turn()

            else:
                print("Still need to wait")
        elif selected_action.get() == 3: # SONAR
            print("Sonar")
            if powerup_wait[1][0] == 0:
                powerup_wait[1][0] = int(powerup_wait[1][1]) #Changes the value so the powerup can only be used so many turns (The const wait value is powerup_wait[x][1])

                if player_ships[4][4] == True: #Checks sub orientation
                    print("Sub vertical")
                    if r < 8: #set sonar up for different map sides
                        start = 0
                        end = random.randint(5,15)
                        increment = 1
                    else:
                        start = 15
                        end = random.randint(0,10)
                        increment = -1
                    for dist in range(start,end,increment): #Loops for the range of the sonar
                        if player_map[(dist*16)+c]["bg"] == "#4ccdf5": # Doesn't display over hit squares
                            player_map[(dist*16)+c]["bg"] = "#4B9DBA" #Displays those squares
                        player_map[(dist*16)+c]["text"] = comp_board[dist][c]
                        if comp_board[dist][c] != "--" and player_map[(dist*16)+c]["bg"] != "red":
                            player_map[(dist*16)+c]["bg"] = "grey"
                            break # Sonar ends when ship has been found

                else:
                    print("Sub Horizontal")
                    if c < 8: #set sonar up for different map sides
                        start = 0
                        end = random.randint(5,15)
                        increment = 1
                    else:
                        start = 15
                        end = random.randint(0,10)
                        increment = -1
                    for dist in range(start,end,increment): #Random sonar range
                        if player_map[(r*16)+dist]["bg"] == "#4ccdf5": # Doesn't display over hit squares
                            player_map[(r*16)+dist]["bg"] = "#4B9DBA" #Displays those squares
                        player_map[(r*16)+dist]["text"] = comp_board[r][dist]
                        if comp_board[r][dist] != "--" and player_map[(r*16)+dist]["bg"] != "red":
                            player_map[(r*16)+dist]["bg"] = "grey"
                            break # Sonar ends when ship has been found

                computer_turn()    
            else:
                print("Wait")

        elif selected_action.get() == 4: # Plane Flyover
            if powerup_wait[2][0] == 0:
                powerup_wait[2][0] = int(powerup_wait[2][1])
                print("Plane Flyover")
                #Main square
                kill_plane = random.randint(1,6)
                if kill_plane != 5:
                    player_map[(r*16)+c]["text"] = comp_board[r][c]
                    if player_map[(r*16)+c]["bg"] != "white" and player_map[(r*16)+c]["bg"] != "red": # Doesn't display over hit squares
                            if comp_board[r][c] != "--":
                                player_map[(r*16)+c]["bg"] = "grey"
                            else:
                                player_map[(r*16)+c]["bg"] = "#4B9DBA" #Displays those squares

                    
                    if r-1 != -1 and c-1 != -1: #Top Left
                        x = r-1
                        y = c-1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares


                    if r+1 != 16 and c+1 != 16: #Bottom right
                        x = r+1
                        y = c+1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares
                    
                    if r-1 != -1 and c+1 != 16: #Top Right
                        x = r-1
                        y = c+1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares

                    if r+1 != 16 and c-1 != -1: #Bottom Left
                        x = r+1
                        y = c-1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares
                    
                    if r-1 != -1: #Left
                        x = r-1
                        y = c
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares

                    if r+1 != 16: #Right
                        x = r+1
                        y = c
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares
                
                    if c-1 != -1: #Down
                        x = r
                        y = c-1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares

                    if c+1 != 16: #Up
                        x = r
                        y = c+1
                        player_map[(x*16)+y]["text"] = comp_board[x][y]
                        if player_map[(x*16)+y]["bg"] != "white" and player_map[(x*16)+y]["bg"] != "red": # Doesn't display over hit squares
                                if comp_board[x][y] != "--":
                                    player_map[(x*16)+y]["bg"] = "grey"
                                else:
                                    player_map[(x*16)+y]["bg"] = "#4B9DBA" #Displays those squares
                else:
                    print("Plane destroyed")
                    powerup_wait[2][0] = int(powerup_wait[2][1]) * 2 + 1 #Greatly increases wait time if plane is destroyed
                computer_turn()
            else:
                print("Wait")

        else: 
            print("Nothing selected for tactical map")
    else:
        print("Can't Place Yet") 

def action(r,c):
    global selected_ship, selected_action
    print(selected_action.get())

    if selected_ship < len(player_ships): #Places a ship if there are ships to place
        place_ship(r,c)
    elif selected_action.get() == 5: #Repair is selected
        print("Repairing that grid")
    else:
        print("Placed all the ships or repair not selected")

win = tk.Tk()
win.resizable(False, False)

player_board = []
player_map = []
selected_ship = 0

create_board()
computer_place_ship()
title = tk.Label(win, text="WAR-BOATS", borderwidth=1, width = 14, height = 1)
title.grid(row=0, column=17, columnspan=2)

# Place Ship buttons

hor_ver = tk.Button(win, text="Horizontal", borderwidth=1, bg="grey", width = 10, height=1, command=toggle)
hor_ver.grid(row=2, column= 17, columnspan=2)

reset_placement_btn = tk.Button(win, text="Reset Placement", borderwidth=1, bg="grey", width = 11, height=1, command=reset_placement)
reset_placement_btn.grid(row=3, column=17, columnspan=2)

ready_btn = tk.Button(win, text="Ready", borderwidth=1, bg="grey", width = 10, height=1, command=ready)
ready_btn.grid(row=4,column=17, columnspan=2)

#Main game buttons

turn_lbl = tk.Label(win, text="your turn")

selected_action = tk.IntVar()
selected_action.set(1)
missile = tk.Radiobutton(win, text="Missile", width = 10, indicatoron = 0, variable=selected_action, value=1)
large_missile = tk.Radiobutton(win, text="Large Missile", width = 10, indicatoron = 0, variable=selected_action, value=2)
sonar = tk.Radiobutton(win, text="Sonar", width = 10, indicatoron = 0, variable=selected_action, value=3)
plane_flyover = tk.Radiobutton(win, text="Plane Flyover", width = 10, indicatoron = 0, variable=selected_action, value=4)

large_missile_lbl = tk.Label(win, text = powerup_wait[0][0])
sonar_lbl = tk.Label(win, text = powerup_wait[1][0])
plane_flyover_lbl = tk.Label(win, text = powerup_wait[2][0])


winner_lbl = tk.Label(win)


win.mainloop()