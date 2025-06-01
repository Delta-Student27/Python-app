# backend.py
import database

def get_candidates():
    return [
        {"party": "Bhajap", "candidate": "Ramesh Yadav", "symbol": "🌾"},
        {"party": "Kongress", "candidate": "Priya Sharma", "symbol": "🌹"},
        {"party": "BJP", "candidate": "Amit Verma", "symbol": "⚙️"},
        {"party": "AAP", "candidate": "Neha Singh", "symbol": "🧹"},
    ]

def vote(party, username):
    data = database.load_votes()
    voted_users = database.load_voted_users()

    if username in voted_users:
        return False  # Already voted

    if party in data:
        data[party] += 1
    else:
        data[party] = 1

    voted_users.append(username)

    database.save_votes(data)
    database.save_voted_users(voted_users)
    return True

def get_results():
    return database.load_votes()
