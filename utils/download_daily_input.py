import json
import requests,shutil

aoc_year = "2024"
aoc_day = "18"
cookieRo = {"session":"53616c7465645f5f2e50eba6b15dfbc6f9a9afc53984a93453c6c9744816907c9ad06ee32d28e9a6994052f0c8c7af5410b5124717914279df106be5263cac4d"}

def download_aoc_file(url, local_filename):
    with requests.get(url, cookies=cookieRo, stream=True) as r:
        with open(local_filename, 'wb') as f:            
           f.write(r.content)
    return local_filename

# download leaderboard information 
download_aoc_file("https://adventofcode.com/" + aoc_year + "/day/" + aoc_day + "/input" , "inputs/input_day" + aoc_day +".txt")