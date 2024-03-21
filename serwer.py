import socket
import threading

server = "192.168.0.104"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Oczekiwanie na połączenie, Serwer uruchomiony")

board = [' ' for _ in range(9)]
currentPlayer=0
players = [None, None]
first_turn = True

def print_board(board):
    return '\n'.join(['|' + '|'.join(board[i:i+3]) + '|' for i in range(0, len(board), 3)])

def check_win(player_mark, board):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player_mark:
            return True
    return False

def threaded_client(conn, player):
    global currentPlayer, first_turn
    players[player] = conn
    if players[0] is not None and players[1] is not None:
        players[0].send(str.encode("Drugi gracz dołączył do gry! Twoja tura!\n" + print_board(board)))
        players[1].send(str.encode("Dołączyłeś do gry! Gracz 1 zaczyna.\n" + print_board(board)))
    player_mark='X' if player==0 else 'O'
    while True:
        if player == currentPlayer:
            valid_move = False
            while not valid_move:
                data = conn.recv(2048).decode()
                if not data:
                    print("Rozłączono")
                    break
                else:
                    move = int(data)-1
                    if move < 0 or move > 8:
                        reply = "Błędna liczba! Podaj pozycję do ruchu (1-9): "
                    elif board[move] == ' ':
                        board[move] = player_mark
                        valid_move = True
                        if check_win(player_mark, board):
                            reply = "Gracz " + player_mark + " wygrywa!\n"
                            if player_mark == 'X':
                                players[1].send(str.encode(reply + print_board(board)))
                            else:
                                players[0].send(str.encode(reply + print_board(board)))
                        elif ' ' not in board:
                            reply = "Remis!\n"
                            if player_mark=='X':
                                players[1].send(str.encode(reply+print_board(board)))
                            else:
                                players[0].send(str.encode(reply + print_board(board)))
                        else:
                            reply = "Sukces\n"
                            if first_turn:
                                 first_turn = False
                            else:
                                if currentPlayer == 1:
                                    currentPlayer = 0
                                else:
                                    currentPlayer = 1
                            if currentPlayer == 0:
                                players[0].send(str.encode("Twoja tura!\n" + print_board(board)))
                            else:
                                players[1].send(str.encode("Twoja tura!\n" + print_board(board)))
                    else:
                        reply = "Niepoprawny ruch! Podaj pozycję do ruchu (1-9): "
                conn.sendall(str.encode(reply+print_board(board)))
    conn.close()

while True:
    if players[0] is None or players[1] is None:
        conn, addr = s.accept()
        print("Połączono do:", addr)
        threading.Thread(target=threaded_client, args=(conn, currentPlayer)).start()
        if currentPlayer == 0:
            currentPlayer = 1