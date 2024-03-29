nickname = "fregy"
nickname2 = "lukas"
nickname3 = "ondrej"

groups = {"000005": ["nikdo"],"999999": ["madar"], "123456": ["jeden", "druhý"], "555555": ["morena"]}

# Function to find free lobby
def find_free_lobby(groups):
    for lobby_id in range(1000000):  # IDs from 0 to 999999
        lobby_id_str = str(lobby_id).zfill(6)  # Convert to string with leading zeros
        if lobby_id_str in groups and len(groups[lobby_id_str]) == 1:
            return lobby_id_str
    return None

free_lobby = find_free_lobby(groups)
if free_lobby:
    print("Free lobby found:", free_lobby)
    groups[free_lobby].append(nickname)
else:
    print("No free lobby found.")

free_lobby = find_free_lobby(groups)
if free_lobby:
    print("Free lobby found:", free_lobby)
    groups[free_lobby].append(nickname2)
else:
    print("No free lobby found.")

free_lobby = find_free_lobby(groups)
if free_lobby:
    print("Free lobby found:", free_lobby)
    groups[free_lobby].append(nickname3)
else:
    print("wrong")

print(groups)
