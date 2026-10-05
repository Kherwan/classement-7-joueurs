import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SEASON = 10
API = (
    f"https://api.latabledessavoirs.fr"
    f"/leaderboards/season/{SEASON}/facile/search"
)

PLAYERS = [
    "Elisa10",
    "Kerwan",
    "Lroux",
    "hugovdal11",
]


def fetch_player(username):
    url = API + "?q=" + urllib.parse.quote(username)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    player = next(
        (
            entry
            for entry in data
            if entry.get("username", "").lower() == username.lower()
        ),
        None,
    )

    if player is None:
        print(f"ATTENTION : joueur introuvable : {username}")
        return None

    return {
        "username": player.get("username", username),
        "score": player.get("score"),
        "rank": player.get("rank"),
    }


def main():
    print("Pseudos recherchés :", PLAYERS)

    players = []
    missing_players = []

    for username in PLAYERS:
        print(f"Recherche de {username}...")
        player = fetch_player(username)

        if player is None:
            missing_players.append(username)
            continue

        if player["score"] is None or player["rank"] is None:
            raise RuntimeError(
                f"Données invalides pour {username}: {player}"
            )

        players.append(player)

    if not players:
        raise RuntimeError(
            "Aucun joueur trouvé : le classement existant est conservé."
        )

    players.sort(key=lambda player: player["rank"])

    result = {
        "season": SEASON,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "players": players,
        "missing_players": missing_players,
    }

    with open("classement.json", "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("Classement mis à jour avec succès.")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
