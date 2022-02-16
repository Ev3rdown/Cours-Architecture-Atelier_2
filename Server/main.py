from flask import Flask, request, Response

server = Flask(__name__)
bag = {}


@server.route('/')
def home():
    global bag

    return "\n".join([f"{k}\t{bag[k]}" for k in bag.keys()])


@server.route('/<key>', methods=['GET'])
def get_data(key):
    global bag

    return bag[key] if key in bag else f'Not found', 200 if key in bag else 404


@server.route('/<key>', methods=['POST'])
def set_data(key):
    global bag

    bag[key] = request.get_data(False, True)
    return bag[key]



def switch_player():
    global bag
    if bag['player_turn']==1:
        bag['player_turn']=2
    else:
        bag["player_turn"]=1

# à appeler à chaque modification de la grille (reception d'un POST valide d'un joueur)
def check(m):
    #on verifie les colonnes
    for i in range(0,3):
        if(m[i][0]==m[i][1]==m[i][2]!=" "):
            return m[i][0]

    #on verifie les lignes
    for i in range(0,3):
        if(m[0][i]==m[1][i]==m[2][i]!=" "):
            return m[0][i]

    #on verifie les diagonales
    if(m[0][0]==m[1][1]==m[2][2]!=" "):
        return m[1][1]

    if(m[0][2]==m[1][1]==m[2][0]!=" "):
        return m[1][1]

    #on verifie qu'il reste des cases a remplir
    for i in range(0,3):
        for j in range(0,3):
            if(m[i][j]==" "):
                return 0
    return 3

@server.route('/play', methods=['POST'])
def play_case():
    global bag
    ret = 1 # error, case selected or not your turn

    req = request.get_data(False, True).split("=")
    if bag['player_turn']!=int(req[0]) or len(req)<2:
        return "1",200
    case = int(req[1])
    print(case)
    if isinstance(case,int):
        if(not(-1<case<9)):
            ret= 4
            ret = 1 # error, impossible case
        x=case%3
        y=int((case-x)/3)
        if(bag["grille"][y][x]==' '):
            ret= 5
            bag["grille"][y][x]=bag['player_turn']
            switch_player()
            print(bag["player_turn"])
            ret = 0 # success, next

    check_code = check(bag['grille'])
    if check_code == 1:
        bag['status']=1
        bag['player_turn']=0
    elif check_code == 2:
        bag['status']=2
        bag['player_turn']=0
    elif check_code == 3:
        bag['status']=3
        bag['player_turn']=0

    return str(ret),200

# give status of game and next player
@server.route('/status', methods=['GET'])
def get_status():
    global bag
    bag["status"]

    return str(bag["status"])+"/"+str(bag["player_turn"]),200


# create a render of the grid
# "-----------"
# "|  |   |  |"
# "|  |   |  |"
# "|  |   |  |"
# "-----------"
def draw(m):
    grille = "-------"+"\n"
    for i in range(0,3):
        grille += "|"+str(m[i][0])+"|"+str(m[i][1])+"|"+str(m[i][2])+"|\n"
        grille += "-------\n"
    return grille

@server.route('/grid', methods=['GET'])
def show_grid():
    global bag
    return draw(bag["grille"]),200

# give number to player
@server.route('/player_number', methods=['GET'])
def get_player_number():
    global bag
    bag["player_number"] += 1

    return str(bag["player_number"]),200


if __name__ == '__main__':
    nada=" "
    bag["grille"] = [[nada,nada,nada],[nada,nada,nada],[nada,nada,nada]] # contient la grille de case
    bag["player_number"] = 0 # numéro du joueur, incrémenté de 1 à chaque nouveau joueur connecté
    bag["player_turn"] = 1 # numéro joueur qui doit jouer le prochain coup
    bag["status"] = 0 # statut de la partie "0"="En cours" | "1"="Victoire du joueur 1" | "2"="Victoire du joueur 2" | "3"="Tie"

    server.run(port=5001)