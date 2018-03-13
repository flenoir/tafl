from tkinter import *
from tkinter import messagebox

window = Tk()

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

def draw_grid():
    for line in range(13):
        canvas.create_line(line*40,0,line*40,440, width= 2, fill="blue")
        canvas.create_line(0,line*40,440,line*40, width=2, fill="red")

def set_pawns():
    rayon = 15

    for item in cases_attaque:
            x = coord_cases[item][0]
            y = coord_cases[item][1]
            canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='black', fill='black')
    
    for item in cases_defense:
        x = coord_cases[item][0]
        y = coord_cases[item][1]
        canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='red', fill='red')
    
    for item in case_king:
        x = coord_cases[item][0]
        y = coord_cases[item][1]
        canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon,outline='blue', fill='blue')

def display_player_turn(newName):
    w.config(text=newName)

def authorized_moves(data):
    temp_auth_moves = []
    # define authorized pawn moves
    if data[0:1] in letters:
        prev = letters.index(data[0:1])-1
        # exception for pawns on row "k"
        if data[0:1] == "k":
            next = letters.index(data[0:1])
        else:
            next = letters.index(data[0:1])+1

        temp_auth_moves.append(data[0:1] + str(int(data[1:])-1))
        temp_auth_moves.append(data[0:1] + str(int(data[1:])+1))
        temp_auth_moves.append(letters[prev] + data[1:])
        temp_auth_moves.append(letters[next] + data[1:])

    actual_turn_pawn_cases = case_king + cases_attaque + cases_defense
    real_arr = [x for x in temp_auth_moves if x not in actual_turn_pawn_cases]
    # print("You can't go here, authorized moves are : ",real_arr, actual_turn_pawn_cases)
    return real_arr

def take_pawns(value, player, players_cases):
    
    print("la value est ", value)
    prev = letters.index(value[0:1])-1
    next = letters.index(value[0:1])+1
    prev1 = letters.index(value[0:1])-2
    next1 = letters.index(value[0:1])+2
    print("next", next, next1, prev, prev1, str(value[0:1]))

    if value[0:1] == "k" or value[0:1] == "j":
        next = 10
        next1 = 10
    else:
        next = letters.index(value[0:1])+1
        next1 = letters.index(value[0:1])+2
    
    print("next2", next, next1, prev, prev1)

    close_arr = []
    up = value[0:1] + str(int(value[1:])-1)
    down = value[0:1] + str(int(value[1:])+1)
    left = letters[prev] + value[1:]
    right = letters[next] + value[1:]
    close_arr.append(up)
    close_arr.append(down)
    close_arr.append(left)
    close_arr.append(right)
    
    up1 = value[0:1] + str(int(value[1:])-2)
    down1 = value[0:1] + str(int(value[1:])+2)
    left1 = letters[prev1] + value[1:]
    right1 = letters[next1] + value[1:]

    if player == "Red plays":
        if up in cases_attaque and up1 in cases_defense:
            cases_attaque.remove(up)
        if down in cases_attaque and down1 in cases_defense:
            cases_attaque.remove(down)
        if left in cases_attaque and left1 in cases_defense:
            cases_attaque.remove(left)
        if right in cases_attaque and right1 in cases_defense:
            cases_attaque.remove(right)

    if player == "Black plays":
        if up in cases_defense and up1 in cases_attaque:
            cases_defense.remove(up)
        if down in cases_defense and down1 in cases_attaque:
            cases_defense.remove(down)
        if left in cases_defense and left1 in cases_attaque:
            cases_defense.remove(left)
        if right in cases_defense and right1 in cases_attaque:
            cases_defense.remove(right)


    
def red_wins(king_case):
    print("king", king_case[0])
    escape_cases = ["a0", "k0", "a10", "K10"]

    for y in escape_cases:
        print(y)
        if y == king_case[0]:
            messagebox.showinfo("Red Wins", "Les Rouges ont gagné ")
            window.destroy()

    
def black_wins(kvalue):
    kvalue = str(kvalue[0])
    prev = letters.index(kvalue[0:1])-1

#   # exception for pawns on row "k"
#     if kvalue[0:1] == "k":
#         next = letters.index(kvalue[0:1])
#     else:
#         next = letters.index(kvalue[0:1])+1

    next = letters.index(kvalue[0:1])+1
    closest_arr = []
    up = kvalue[0:1] + str(int(kvalue[1:])-1)
    down = kvalue[0:1] + str(int(kvalue[1:])+1)
    left = letters[prev] + kvalue[1:]
    right = letters[next] + kvalue[1:]
    closest_arr.append(up)
    closest_arr.append(down)
    closest_arr.append(left)
    closest_arr.append(right)

    # result = all(x in cases_attaque for x in closest_arr)
    # print(result, closest_arr, cases_attaque, case_king)
    if all(x in cases_attaque for x in closest_arr):
        print("Black wins")
        messagebox.showwarning("Black Wins", "Les Noires ont gagné, vouslez-vous rejouer ? ")


def move_pion(data,target,case_lists):
    # effectively move the pawn
    for el in case_lists:
        auth_arr = authorized_moves(data) # check authorized moves
        global player

        if el == data and target in auth_arr: # if case is found by mouse_point and target is in authorized cases for move
        # the we move the pawn on the proper case list         
            case_lists[case_lists.index(data)] = target

            # add take pawn function to remove opponent pawns if they are framed by two pawns
            take_pawns(target, player, case_lists)

            # switch player after effective move 
            if player == "Red plays":
                player = "Black plays"
            else:
                player = "Red plays"
            canvas.delete("all")
            red_wins(case_king)
            black_wins(case_king)
            return set_pawns(), draw_grid(),display_player_turn(player)


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
        # print(d + " not in selected cases")
        turn -=1


def mouse_coords(event):
    global turn # need to be a global variable
    global player
    # retreive x and y coordinates from the mouse
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
                    # print(" even " + str(turn))
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


canvas = Canvas(window, height= 440, width= 440, background= "grey")
canvas.pack()
bouton1 = Button(window, text="Quitter", command = window.destroy)
bouton1.pack()
w = Label(window, text="Red plays")
w.pack()

canvas.bind("<1>",mouse_coords)
# print(current_game)
# print("resultat = " + str(mouse_coords))


# creation d'une window de saisie
# player1_label = Label(window, text="enter player's one name")
# player1_label.pack()
# player1_name = Entry(window)
# player1_name.pack()



draw_grid()
set_pawns()


window.mainloop() 
