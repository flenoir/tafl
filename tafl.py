from tkinter import *

fenetre = Tk()

# print(coord_cases["A1"][0])
cases_attaque = ["a3","a4","a5","a6","a7","b5","d0","e0","f0","g0","h0","f1","f9","d10","e10","f10","g10","h10","j5","k3","k4","k5","k6","k7"]
cases_defense = ["d5","e4","e5","e6",'f3',"f4","f6","f7","g4","g5","g6","h5"]
case_king = ["f5"]
grid = {}
current_game = {}
turn = 0
letters = []
player = "Red plays"

def index_cases():
    global letters
    values = list(range(20,440,40))
    letters = ["a","b","c","d","e","f","g","h","i","j","k"]

    for i,v in enumerate(letters):
        for j,w in enumerate(values):
            grid[v + str(j)] = (values[i],w)
    
    return grid

coord_cases = index_cases()
# print(coord_cases)

def tracer_grille():
    for line in range(13):
        canvas.create_line(line*40,0,line*40,440, width= 2, fill="blue")
        canvas.create_line(0,line*40,440,line*40, width=2, fill="red")
    

def placer_pions():
    rayon = 15

    for item in cases_attaque:
            # print(coord_cases[item][0],coord_cases[item][1])
            x = coord_cases[item][0]
            y = coord_cases[item][1]
            canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='black', fill='black')
    
    for item in cases_defense:
        # print(coord_cases[item][0],coord_cases[item][1])
        x = coord_cases[item][0]
        y = coord_cases[item][1]
        canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='red', fill='red')
    
    for item in case_king:
        # print(coord_cases[item][0],coord_cases[item][1])
        x = coord_cases[item][0]
        y = coord_cases[item][1]
        canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='blue', fill='blue')

def display_player_turn(newName):
    w.config(text=newName)



def move_pion(data,target,case_lists):
    temp_auth_moves = []
    # define authorized pawn moves
    if data[0:1] in letters:
        prev = letters.index(data[0:1])-1
        # exception for pawns on row "k"
        if data[0:1] == "k":
            next = letters.index(data[0:1])
            print("if " + str(next))
        else:
            next = letters.index(data[0:1])+1
            print("else " + str(next))

        temp_auth_moves.append(data[0:1] + str(int(data[1:])-1))
        temp_auth_moves.append(data[0:1] + str(int(data[1:])+1))
        temp_auth_moves.append(letters[prev] + data[1:])
        temp_auth_moves.append(letters[next] + data[1:])
        # print(temp_auth_moves)
        
     # we need to reduce temp_auth_moves owing to pawn already in place.
    for i in temp_auth_moves:
        if i in cases_attaque:
            temp_auth_moves.remove(i)
            print( "you can't go here" + str(temp_auth_moves))
            print(cases_attaque)
        elif i in cases_defense:
            temp_auth_moves.remove(i)
            print( "you can't go here too" + str(temp_auth_moves))
            print(cases_defense)

    # effectively move the pawn
    for el in case_lists:
        global player
        if el == data and target in temp_auth_moves: # if case is found by mouse_point and target is in authorized cases for move
        # the we move the pawn on the proper case list         
            case_lists[case_lists.index(data)] = target
            # switch player after effective move 
            if player == "Red plays":
                player = "Black plays"
            else:
                player = "Red plays"
            print(player)
            canvas.delete("all")
            print(case_lists)
            return placer_pions(), tracer_grille(),display_player_turn(player)

def selected_case(d):
    if d in cases_defense:
        selected = canvas.create_rectangle(grid[d][0]-20, grid[d][1]-20, grid[d][0]+20, grid[d][1]+20,fill='green')
        canvas.tag_lower(selected)
    elif d in cases_attaque:
        selected = canvas.create_rectangle(grid[d][0]-20, grid[d][1]-20, grid[d][0]+20, grid[d][1]+20,fill='green')
        canvas.tag_lower(selected)
    elif d in case_king:
        selected = canvas.create_rectangle(grid[d][0]-20, grid[d][1]-20, grid[d][0]+20, grid[d][1]+20,fill='green')
        canvas.tag_lower(selected)
    else:
        print(d + " not in selected cases")
        turn -=1

# il faut faire un tableau dans lequel on classe les tours et les cases selectionnées par la souris, si le tour != de int, on récupèrera la valeur de la case trouvée au tour précédent.

def mouse_coords(event):
    global turn # préciser que c'est une variable globale sinon pb de scope
    global player
    #recupere les coordonnées du point x,y du clic de la souris
    mouse_point = (event.x, event.y)

    for x in grid: 
        # print(mouse_point[0], grid[x][0])
        varAbs  = mouse_point[0] - grid[x][0] 
        varOrd = mouse_point[1] - grid[x][1]
        abs_min = grid[x][0] - 15
        abs_max = grid[x][0] + 15
        ord_min = grid[x][1] - 15
        ord_max = grid[x][1] + 15
        # mouse selected point is converted in a case from the grid
        if mouse_point[0] > abs_min and mouse_point[0] < abs_max :
            if mouse_point[1] > ord_min and mouse_point[1] < ord_max :
                current_game[turn]= x
                # if turn is even
                if turn % 2 == 0:
                    selected_case(x)
                    print(" even " + str(turn))
                    turn += 1
                # else turn is odd
                else:
                    print(mouse_point, grid[x])
                    #the case is sent to move_pion function as input
                    val = current_game[turn-1]
                    if val in cases_defense and player == "Red plays":
                        move_pion(str(val),str(x),cases_defense)
                    elif val in case_king and player == "Red plays":
                        move_pion(str(val),str(x),case_king)
                    elif val in cases_attaque and player =="Black plays":
                        move_pion(str(val),str(x),cases_attaque)
                    turn += 1
                    print(turn, current_game)
                    
    


canvas = Canvas(fenetre, height= 440, width= 440, background= "grey")
canvas.pack()
bouton1 = Button(fenetre, text="Quitter", command = fenetre.destroy)
bouton1.pack()
# bouton3 = Button(fenetre, text="pions", command = placer_pions)
# bouton3.pack()
# bouton4 = Button(fenetre, text="move", command = lambda: move_pion('f7'))
# bouton4.pack()
w = Label(fenetre, text="Red plays")
w.pack()

canvas.bind("<1>",mouse_coords)
# print(current_game)
# print("resultat = " + str(mouse_coords))


# creation d'une fenetre de saisie
# player1_label = Label(fenetre, text="enter player's one name")
# player1_label.pack()
# player1_name = Entry(fenetre)
# player1_name.pack()



tracer_grille()
placer_pions()
print(turn)


fenetre.mainloop() 
