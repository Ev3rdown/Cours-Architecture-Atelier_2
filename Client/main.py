import socket
from time import sleep

def request(verb, url, value):
    string = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 5001))
        sock.send(f"{verb} /{url} HTTP/1.1\r\n".encode())
        sock.send("Content-Type: text/plain\r\n".encode())
        sock.send(f"Content-Length: {len(value)}\r\n\r\n".encode())
        sock.send(f"{value}\r\n".encode())
        while True:
            s = sock.recv(4096).decode('utf-8')
            if s == '':
                break;
            #print(s)
            string+=str(s)
        sock.close()
    return string

def get_player_number():
    req = request("GET","player_number","").split("\n")[-1]
    return int(req);

def update_status():
    req = request("GET","status","").split("\n")[-1]
    vals = req.split("/")
    status_GAME = int(vals[0]);
    status_PLAYER = int(vals[1]);
    return status_GAME,status_PLAYER

if __name__ == '__main__':

    player_number = get_player_number()
    status_GAME=0
    status_PLAYER=1
    status_GAME,status_PLAYER  = update_status()

    print("Vous êtes le joueur "+str(player_number))
    while status_GAME==0:
        if status_PLAYER==player_number:
            print(request("GET","grid",""))
            print("Joueur "+ str(player_number) +" a vous de jouer :")
            case=int(input("Entrer un numéro de case entre 1 et 9:"))-1
            req = request("POST","play",str(player_number)+"="+str(case))
            if req == 1:
                print("Erreur")
                continue
            print(request("GET","grid",""))
        else:
            print("En attente de l'autre joueur")
        status_GAME,status_PLAYER = update_status()
        sleep(1)
    if status_GAME!=3:
        print("Victoire du joueur "+str(status_GAME))
    elif status_GAME==3:
        print("Pas de vainqueur")
    else:
        print("Erreur Fatale")