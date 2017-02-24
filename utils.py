
from socket import socket
from cfg import SERVER, PORT, PASS, BOT, CHANNEL, GROUP_CHAT, CLIENT
import datetime
import json
import requests
import sql
from random import randint
import player
# import playsound
from pygame import mixer

def open_socket():
	s = socket()
	s.connect((SERVER, PORT))
	s.send(("PASS " + PASS + "\r\n").encode())
	s.send(("NICK " + BOT + "\r\n").encode())
	s.send(("JOIN #" + CHANNEL + "\r\n").encode())
	s.send(("JOIN #" + GROUP_CHAT + "\r\n").encode())
	s.send(("CAP REQ :twitch.tv/commands\r\n").encode())
	return s

def send_message(s, message):
	message_temp = "PRIVMSG #" + CHANNEL + " :" + message
	s.send((message_temp + "\r\n").encode())

def send_whisper(s, user, message):
	message_temp = "PRIVMSG #" + CHANNEL + " :/w " + user + " " + message
	s.send((message_temp + "\r\n").encode())

def loading_completed(line):
	if ("End of /NAMES list" in line):
		return False
	else:
		return True

def join_chat(s):
	readbuffer_join = "".encode()
	Loading = True
	while Loading:
		readbuffer_join = s.recv(1024)
		readbuffer_join = readbuffer_join.decode()
		temp = readbuffer_join.split("\n")
		readbuffer_join = readbuffer_join.encode()
		readbuffer_join = temp.pop()
		for line in temp:
			Loading = loading_completed(line)
	print(datetime.datetime.now().strftime("%H:%M:%S") + " [S] >> Bot has joined the channel!")

def get_user(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user.strip()

def get_message(line):
	global message
	try:
		message = (line.split(":", 2))[2]
	except:
		message = ""
	return message.strip()

def get_command(message):
	try:
		cmd = message.split(" ", 2)[0]
	except:
		cmd = ""
	return cmd.strip()

def get_argument(message):
	try:
		arg = message.split(" ", 2)[1]
	except:
		arg = ""
	return arg.strip()

def get_text(message):
	try:
		text = message.split(" ")
		del text[0:2]
		result = ' '.join(text)
	except:
		result = ""
	return result.strip()

def get_quote(message):
	try:
		quote = message.split(" ")
		del quote[0:1]
		quote = ' '.join(quote)
	except:
		quote = ""
	return quote.strip()

# checks the relationship between the passed user and channel
def is_follower(user):
	response = requests.get("https://api.twitch.tv/kraken/users/" + 
		user + "/follows/channels/" + CHANNEL + "?client_id=" + CLIENT)
	data = json.loads(response.text)
	if 'error' in data:
		return False
	else:
		return True

# gets the current list of viewers and returns a list
# the Twitch API updates every 5 minutes, so this should not be checked more
# than every 10 minutes or so. 
def get_viewers():
	timestamp = datetime.datetime.now().strftime("%H:%M:%S")
	try:
		response = requests.get('https://tmi.twitch.tv/group/user/theangryginger/chatters?client_id=' + CLIENT)
		data = json.loads(response.text)
		chatters = []
		for user in data['chatters']['moderators']:
			chatters.append(user)
		for user in data['chatters']['viewers']:
			chatters.append(user)
		return chatters
	except:
		print(timestamp + " [S] >> [!] Retrieving viewers list failed")
		pass

def mass_add_points(pts):
	try:
		users = get_viewers()
		for user in users:
			if is_follower(user):
				sql.add_points(user, int(pts) + 2)
			else:
				sql.add_points(user, int(pts))
	except:
		print(datetime.datetime.now().strftime("%H:%M:%S") + " [S] >> [!] Mass points addition failed")
		pass

def roll_dice(num_of_dice, num_of_sides):
	roll = []
	for x in range(int(num_of_dice)):
		roll.append(randint(1, int(num_of_sides)))
	roll.sort()
	return roll

# splits the message into a list of substrings
def parse_character(message):
	player = message.split(" ")
	del player[0:1]
	print ("Player information parsed.")
	return player

# check if player already exists
def load_player(user):
	player = sql.get_player(user)
	if player:
		print ("player loaded")
		return player

def change_name(user, name):
	pass

# pid, name, race, sex, class, hp, age, religion, str, dex, con, wis, int, xp, level
def create_player(user, character):
	pid = user
	name = player[0]
	race = player[1]
	if race.lower() not in player.RACES:
		send_message(s, "Race is not valid!")
		send_message(s, "The proper format is !createplayer Name Race Sex Class")
		return
	_class = player[2]
	if _class.lower() not in player.CLASSES:
		send_message(s, "Class is not valid!")
		send_message(s, "The proper format is !createplayer Name Race Sex Class")
		return
	sex = player[3]
	if sex.lower() not in ['male', 'female']:
		send_message(s, "Sex is not valid!")
		send_message(s, "The proper format is !createplayer Name Race Sex Class")
	hp = calculate_hp(race, _class)
	age = get_player_age(race, _class)
	send_message(s, "Huzzah! The adventurer, {}, has joined the ranks of the kingdon!".format(name))
	
def play_sound():
	mixer.init()
	mixer.music.load(r'C:\Users\Brandon\Desktop\TwitchBot\resources\sounds\jaws.mp3')
	mixer.music.play()

def increase_death_counter():
	workfile = "deaths.txt"
	f = open(workfile, 'r+')
	current_deaths = int(f.read())
	f.close()
	new_deaths = str(current_deaths + 1)
	f = open(workfile, 'r+')
	f.write(new_deaths)
	f.close()

def reset_death_counter():
	workfile = "deaths.txt"
	f = open(workfile, 'r+')
	f.write("0")
	f.close()
	
def promote_charity(s):
	pass