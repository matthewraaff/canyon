import requests

def fetchData(profile, month, year):
    if len(str(month)) == 1:
        month = '0' + str(month)
    url = "https://api.chess.com/pub/player/{}/games/{}/{}".format(profile, year, month)
    r = requests.get(url)
    b = r.json()
    print(b)
    for game in b['games']:
        print(game['pgn'])
        # save EVERY pgn file to a folder called games
        with open('GAMES/{}.pgn'.format(game['uuid']), 'w') as f:
            f.write(game['pgn'])



def main():
    profile = input("Enter chess.com username: ")
    games = fetchData(profile, 1, 2023)

if __name__ == "__main__":
    main()