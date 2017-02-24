
import cfg
import time
import sql
import threading
import string
import datetime
import random
from player import Player
from utils import *

def main():

	def channel(user, num):
		name = "channel " + str(num)
		ts = datetime.datetime.now().strftime("%H:%M:%S")
		print (ts + " [S] >> Channel has spawned a new thread named {}".format(name))
		print (ts + " [S] >> The channel is owned by {}".format(user))
		return

	def Console(line):
		if "PRIVMSG" in line:
			return False
		else:
			return True

	s = open_socket()
	join_chat(s)
	readbuffer = ""
	commands = sql.get_commands()
	channels = []
	timer = 0

	while True:
			try:
				readbuffer = s.recv(1024)
				readbuffer = readbuffer.decode()
				temp = readbuffer.split("\n")
				readbuffer = readbuffer.encode()
				readbuffer = temp.pop()
			except:
				temp = ""
			for line in temp:
				timestamp = datetime.datetime.now().strftime("%H:%M:%S")
				if line == "":
					break
				# So twitch doesn't timeout the bot.
				if "PING" in line and Console(line):
					msgg = "PONG tmi.twitch.tv\r\n".encode()
					print (timestamp + " [S] PONG sent to server")
					timer += 1 # timer increments every 5 minutes
					# every ten minutes, run add_points()
					if (timer % 2 == 0):
						mass_add_points(2)
						print (timestamp + " [S] Automatic points given.")
					s.send(msgg)
					# print(msgg)
					break
				# get user
				user = get_user(line)
				# get message send by user
				message = get_message(line)
				# for you to see the chat from CMD
				if "WHISPER" in line:
					print(timestamp + " [W] >> [" + user + ":] " + message)
				else:
					print(timestamp + " [C] >> [" + user + ":] " + message)
				# sends private msg to the user (start line)
				PMSG = "/w " + user + " "

	################################# Hard-coded utils ######################
	## 	CLEAN THIS UP!!! ###

				cmd = get_command(message)
				arg = get_argument(message)
				text = get_text(message)

				# iterate through custom utils to find a match
				for command in commands:
					if command[0] in cmd:
						response = sql.run_command(command[0])
						send_message(s, response)
						break

				# simple ping response
				if message.startswith("!ping"):
					if "WHISPER" in line:
						send_whisper(s, user, "PONG!")
					else:
						send_message(s, "PONG!")
					break
				
				### Quotes Module ###

				# implement a death counter
				if sql.is_mod(user) and message.startswith("!rekt"):
					increase_death_counter()
					send_message(s, "You just got rekt, son!")

				if sql.is_mod(user) and message.startswith("!reset"):
					reset_death_counter()
					send_message(s, "Death Counter has been reset.")

				# add quote for user
				if message.startswith("!addquote"):
					quote = get_quote(message)
					sql.add_quote(quote)
					break

				# display quote
				if message.startswith("!quote"):
					quote = sql.get_quote()
					if "WHISPER" in line:
						send_whisper(s, user, quote)
					else:
						send_message(s, quote)

				### Custom Command Module

				# add command 
				# syntax: !addcom <new command> <command text>
				if sql.is_mod(user) and message.startswith("!addcom"):
					# add this command
					sql.add_command(arg, text)
					commands = sql.get_commands()
					break
				
				# delete a command
				# syntax: !delcom <command>
				if sql.is_mod(user) and message.startswith("!delcom"):
					# remove this command
					sql.delete_command(arg)
					commands = sql.get_commands()
					break
				
				# modify a current command 
				# maybe check to see if command is valid first
				if sql.is_mod(user) and message.startswith("!modcom"):
					sql.modify_command(arg, text)
					break
				
				### User Administration Module ###

				# add a moderator
				# syntax: !addmod <username>
				if sql.is_mod(user) and message.startswith("!addmod"):
					sql.add_mod(arg)
					break
				
				# remove a moderator
				# syntax: !delmod <username>
				if sql.is_mod(user) and message.startswith("!delmod"):
					sql.remove_mod(arg)
					break
				
				# ban a user
				# syntax: !ban <username>
				if sql.is_mod(user) and message.startswith("!ban"):
					utils.ban_user(s, arg)
					break
				
				# unban a user
				if sql.is_mod(user) and message.startswith("!unban"):
					utils.ban_user(s, arg)
					break

				# timeout a user
				# syntax: !timeout <username>
				if sql.is_mod(user) and message.startswith("!timeout"):
					utils.timeout_user(s, arg)
					break

				### Game Suggestion Module ###

				# user add suggestions for games to be played - similar to Lirik's
				# Sub sunday 
				if message.startswith("!suggestgame"):
					suggestion = get_quote(message)
					sql.add_suggestion(suggestion)
					break

				# retrieves top 3 recommended games
				if sql.is_mod(user) and message.startswith("!suggestions"):
					suggestions = sql.get_suggestions()
					for suggestion in suggestions:
						sugg = "{} had {} votes".format(suggestion[0], suggestion[1])
						send_message(s, sugg)
					break

				# resets the suggestions table
				if (user == cfg.OWNER) and message.startswith("!purgesuggestions"):
					sql.purge_suggestions()
					break

				### Youtube Music Player Requests Module ###

				# adds youtube.com request for now
				if message.startswith("!request"):
					sql.add_request(arg)
					sql.subtract_points(user, )
					break

				# delete the oldest request
				if message.startswith("!skip"):
					sql.skip_request()

				### Challenger Queue Module ###
				if message.startswith("!join"):
					sql.add_challenger(user)
					send_message(s, "TheAngryGinger has been challenged by {}".format(user))
					break

				if sql.is_mod(user) and message.startswith("!win"):
					sql.remove_challenger("win")
					break

				if sql.is_mod(user) and (message.startswith("!loss") or message.startswith("!forfeit")):
					sql.remove_challenger("loss")
					break

				if sql.is_mod(user) and message.startswith("!draw"): 
					sql.remove_challenger("draw")
					break

				if message.startswith("!results"):
					results = sql.get_results(user)
					wins = results[0][1]
					losses = results[1][1]
					draws = results[2][1]
					send_message(s, "{} has {} win(s), {} loss(es), and {} draw(s)".format(user, wins, losses, draws))
					break

				# manually give everyone X points out of cycle
				if (user == cfg.OWNER) and message.startswith("!give"):
					mass_add_points(arg)
					send_message(s, "{} is a merciful leader ".format(cfg.OWNER) +
						"and has given everyone {} {}!".format(arg, cfg.CURRENCY))
					print (timestamp + " [S] >> " + cfg.OWNER + " just gave everyone " 
						+ arg + " points.")
					break

				# retrieves a users points balance and prints it to the chat
				if message.startswith("!points"):
					points = sql.get_points(user)
					if "WHISPER" in line:
						send_whisper(s, user, "You have {} {}!".format(points, cfg.CURRENCY))
					else:
						send_message(s, "{} has {} {}!".format(user, points, cfg.CURRENCY))
					break

				if message.startswith("!dance"):
					send_message(s, ".me dances with {}".format(user))
					send_message(s, "(>'-')> <('-'<) ^('-')^ v('-')v (>'-')>")
					break

				if message.startswith("!rage"):
					send_message(s, "I'm tired of your shit!".format(user))
					send_message(s, "(╯°□°）╯︵ ┻━┻")
					break
				
				# help command. Eventually this will link to a help doc on Github/website
				if message.startswith("!help"):
					send_whisper(s, user, "This will eventually be a link to" +
						" the Github help documentation. PogChamp")
				
				if message.startswith("!roll"):
					arg = get_argument(message)
					num_of_dice = arg.split('d',1)[0]
					num_of_sides = arg.split('d',1)[1]
					roll = roll_dice(str(num_of_dice), str(num_of_sides))
					result = "The results were "
					for r in roll:
						result += "{}, ".format(r)
					if "WHISPER" in line:
						send_whisper(s, user, result[:-2])
					else:
						send_message(s, result[:-2])

				# # creates a new player character for the user
				# if message.startswith("!createplayer"):
				# 	player = load_player(user)
				# 	if player:
				# 		send_message(s, "You already have a character, {}".format(user,))
				# 	else:
				# 		# send_message(s, "We will now create your character, {}".format(user,))
				# 		create_player(user, parse_character(message))
				# 	break

				# Russian roulette
				if message.startswith("!roulette"):
					num = random.randint(1,6)
					if num == 1 or num == 5:
						send_message(s, "*BANG* You're dead, {}".format(user,))
					else:
						send_message(s, "*click* You live to see another day, {}".format(user,))

				if message.startswith("!lurk"):
					send_message(s, "Captain TAG, we have another shark lurkin' " +
						"in the waters. We're gonna need a bigger boat!")
					play_sound()

if __name__ == "__main__":
	main()