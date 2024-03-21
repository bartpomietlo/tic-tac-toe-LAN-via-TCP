import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.104', 5556))
print("---------------------------------------------------------------------------------------")
print("                         Witaj w grze kółko krzyżyk")
print("---------------------------------------------------------------------------------------\n")
print("Zasady gry:")
print("1. Gra jest przeznaczona dla dwóch graczy, którzy na przemian wykonują ruchy.")
print("2. Gracze wprowadzają swoje ruchy, wybierając pozycję na planszy od 1 do 9.")
print("3. Jeśli jest twoja tura, wprowadź numer pozycji, na której chcesz postawić swój znak:")
print("                                     |1|2|3|")
print("                                     |4|5|6|")
print("                                     |7|8|9|")
print("Oczekiwanie na przeciwnika...")



while True:
    response = client.recv(2048).decode()
    print(response)
    if "Twoja tura!" in response or "Niepoprawny ruch!" in response:
        while True:
            inp = input("Podaj pozycję do ruchu (1-9): ")
            if inp.isdigit() and 1 <= int(inp) <= 9:
                client.send(str.encode(inp))
                response = client.recv(2048).decode()
                print(response)
                if "Niepoprawny ruch!" not in response:
                    break
            else:
                print("Niepoprawna wartość! Podaj liczbę od 1 do 9.")
