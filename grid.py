def index_cases():
    values = list(range(20,440,40))
    letters = ["a","b","c","d","e","f","g","h","i","j","k"]

    grid = {}

    for i,v in enumerate(letters):
        for j,w in enumerate(values):
            grid[v + str(j)] = (values[i],w)
    
    return grid


print(index_cases())

