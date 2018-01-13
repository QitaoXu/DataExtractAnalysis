#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys, os

if len(sys.argv) < 2:
    sys.exit("""Usage: The first argument %s should be the name of file you want to excute and the second argument shoulb be the file directory.
			 Both arguments are required.""" % sys.argv[0])

filename = sys.argv[1]

if not os.path.exists(filename):
    sys.exit("Error: File '%s' not found" % sys.argv[1])

player_regex = re.compile(r"^([\w]+\s[\w]+)\sbatted\s([\d]+)\stimes\swith\s([\d]+)\shits\sand\s([\d]+)\sruns$")

year_regex = re.compile(r"^194[0-4]{1}$")

year = input("Please input the year you want to query: \n")

year_match = year_regex.match(year)

file_prefix = "/home/Jeremy/PyFiles/cardinals"

file_suffix = ""

file_dir = ""

if year_match is not None or year == "1930":
	file_suffix = year + ".txt"
	file_dir = file_prefix + file_suffix
else:
	sys.exit("The year you input is not valid.")
	

players = dict()
sorted_players = dict()

class Player(object):
	def __init__(self, name, battedTimes, hits, runs):
		self.name = name
		self.battledTimes = int(battedTimes)
		self.hits = int(hits)
		self.runs = int(runs)
		self.average = 0


with open(file_dir) as f:
	for line in f:
		#print(line.rstrip())
		match = player_regex.match(line)
		if match is not None:#This line is valid
			if match.group(1) in players:#has recorded this player
				players[match.group(1)].battledTimes += int(match.group(2))#renew this player's battleTimes
				players[match.group(1)].hits += int(match.group(3))#renew this player's hits
				players[match.group(1)].runs += int(match.group(4))#renew this player's runs
			else:#need to build a new player
				players[match.group(1)] = Player(match.group(1),match.group(2),match.group(3),match.group(4))
		else:#This line is not about statistics
			continue

for recorded_player in players:
	#Compute hits/battleTimes per player in a season
	players[recorded_player].average = players[recorded_player].hits / players[recorded_player].battledTimes
	
	#Round the result
	players[recorded_player].average = round(players[recorded_player].average,3)

#Players sorted by their average respectively.
#Note: function sorted returns a list rather than a dictionary!!!!!!!!!
sorted_players = sorted(players,key=lambda  k:players[k].average, reverse = True)

print("Hitter: hit/battleTimes")
for sorted_player in sorted_players:
	#Output as directed by wiki
	print("%s: %.3f" % (sorted_player, players[sorted_player].average))
	
		
		
