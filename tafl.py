from tkinter import *

fenetre = Tk()

# print(coord_cases["A1"][0])
cases_attaque = ["a3","a4","a5","a6","a7","b5","d0","e0","f0","g0","h0","f1","f9","d10","e10","f10","g10","h10","j5","k3","k4","k5","k6","k7"]
cases_defense = ["d5","e4","e5","e6", "f3","f4","f6","f7","g4","g5","g6","h5"]
case_king = ["f5"]
grid = {}
current_game = {}
# creation de tours pour gèrer les tours de jeu des 2 camps
turn = 0

def index_cases():
    values = list(range(20,440,40))
    letters = ["a","b","c","d","e","f","g","h","i","j","k"]

    # grid = {}

    for i,v in enumerate(letters):
        for j,w in enumerate(values):
            grid[v + str(j)] = (values[i],w)
    
    return grid

coord_cases = index_cases()
print(coord_cases)

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

def move_pion(data,target):
    # print(pion)
    for el in cases_defense:
        if el == data: # si la case identifiée par la souris
        # alors on propose des choix de deplacement autorisés.
            # pion = "f8"
            print("trouvé")           
            cases_defense[cases_defense.index(data)] = target
            # print(cases_defense)
            canvas.delete("all")
            return placer_pions(), tracer_grille()

def selected_case(d):
    selected = canvas.create_rectangle(grid[d][0]-20, grid[d][1]-20, grid[d][0]+20, grid[d][1]+20,fill='green')
    canvas.tag_lower(selected)

# il faut faire un tableau dans lequel on classe les tours et les cases selectionnées par la souris, si le tour != de int, on récupèrera la valeur de la case trouvée au tour précédent.

def mouse_coords(event):
    global turn # préciser que c'est une variable globale sinon pb de scope
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
                # print("inferieur à 15 d'ecart", x)
                current_game[turn]= x
                if turn % 2 == 0:
                    selected_case(x)
                    turn += 1
                    print(turn)
                else:
                    print(mouse_point, grid[x])
                    #the case is sent to move_pion function as input
                    val = current_game[turn-1]
                    # print(str(x),str(val))
                    move_pion(str(val),str(x))
                    # selected_case(x, str(x))
                    turn += 1
                    print(turn)
                    # current_game[turn]= x
                    print(current_game)
    

               



canvas = Canvas(fenetre, height= 440, width= 440, background= "grey")
canvas.pack()
bouton1 = Button(fenetre, text="Quitter", command = fenetre.destroy)
bouton1.pack()
bouton2 = Button(fenetre, text="ligne", command = tracer_grille)
bouton2.pack()
bouton3 = Button(fenetre, text="pions", command = placer_pions)
bouton3.pack()
bouton4 = Button(fenetre, text="move", command = lambda: move_pion('f7'))
bouton4.pack()

canvas.bind("<1>",mouse_coords)
# print(current_game)
# print("resultat = " + str(mouse_coords))




fenetre.mainloop() 
