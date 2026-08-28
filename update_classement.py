import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://api.latabledessavoirs.fr/leaderboards/season/8/facile/search"

PLAYERS = [
    "Elisa10",
    "Kerwan",
    "Lroux",
]
print("Pseudos recherchés :", PLAYERS)

def fetch_player(username):
    url = API + "?q=" + urllib.parse.quote(username)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    exact = next(
        (
            player
            for player in data
            if player.get("username", "").lower() == username.lower()
        ),
        None
    )

    player = exact or (data[0] if data else None)

    if not player:
        raise RuntimeError(f"Joueur introuvable : {username}")

    return {
        "username": player.get("username", username),
        "score": player.get("score"),
        "rank": player.get("rank")
    }


def main():
    players = []

    for username in PLAYERS:
        print(f"Recherche de {username}...")
        player = fetch_player(username)

        if player["score"] is None or player["rank"] is None:
            raise RuntimeError(
                f"Données invalides pour {username}: {player}"
            )

        players.append(player)

    players.sort(key=lambda player: player["rank"])

    result = {
        "season": 8,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "players": players
    }

    with open("classement.json", "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("Classement mis à jour avec succès.")
print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
