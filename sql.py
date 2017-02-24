
import sqlite3

conn = sqlite3.connect('twitch.db')
c = conn.cursor()

def is_mod(u):
	u = u.strip()
	c.execute("SELECT * FROM moderators WHERE user = (?)", (u,))
	mod = c.fetchone()
	if mod:
		result = True
	else:
		result = False
	return result

def add_mod(u):
	u = u.strip()
	c.execute("INSERT INTO moderators VALUES (?)", (u,))
	conn.commit()
	print ("Moderator added.")

def remove_mod(u):
	u = u.strip()
	c.execute("DELETE FROM moderators WHERE user = (?)", (u,))
	conn.commit()
	print ("Moderator removed.")

def add_command(trigger, response):
	c.execute("INSERT INTO commands VALUES (?,?)", (trigger, response,))
	conn.commit()
	print ("Command added.")

def delete_command(trigger):
	c.execute("DELETE FROM commands WHERE trigger = (?)", (trigger,))
	conn.commit()
	print ("Command deleted.")

def modify_command(trigger, response):
	c.execute("UPDATE commands SET response = (?) WHERE trigger = (?)", (response, trigger,))
	conn.commit()
	print ("Command Updated.")

def get_commands():
	c.execute("SELECT trigger FROM commands")
	commands = c.fetchall()
	return commands

def run_command(trigger):
	c.execute("SELECT response FROM commands WHERE trigger = (?)", (trigger,))
	response = c.fetchone()
	r = str(response[0])
	return r

def add_quote(quote):
	c.execute("INSERT INTO quotes VALUES (?,?)", (None, quote,))
	conn.commit()
	print ("Quote added.")

def get_quote():
	c.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;")
	result = c.fetchone()
	quote = "Quote #" + str(result[0]) + ": " + str(result[1])
	return quote.strip()

def add_suggestion(suggestion):
	c.execute("INSERT INTO suggestions VALUES (?,?)", (None, suggestion,))
	conn.commit()
	print ("Suggestion added.")

def get_suggestions():
	c.execute("SELECT suggestion, count(suggestion) FROM suggestions GROUP BY suggestion ORDER BY count(suggestion) DESC LIMIT 3")
	r = c.fetchall()
	return r

def purge_suggestions():
	c.execute("DELETE FROM suggestions")
	c.execute("VACUUM")
	conn.commit()

# pid, name, race, sex, class, hp, age, religion, str, dex, con, wis, int, xp, level
def create_character(user, player):
	c.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?,?)", (user, name, race, 
															_class, sex, hp, age, None, 
															None, None, None, 0, 1))
	conn.commit()

# look at add_challenger for help on preventing duplicated requests
def add_request(request):
	c.execute("INSERT INTO requests VALUES (?)", (request,))
	print ("Song Request added.")
	conn.commit()

def skip_request():
	c.execute("DELETE FROM requests WHERE ROWID IN (SELECT ROWID FROM requests ORDER BY ROWID ASC LIMIT 1)")
	print ("Next Song Request skipped.")
	conn.commit()

def add_result(challenger, result):
	c.execute("INSERT INTO results VALUES (?,?)", (challenger, result,))
	conn.commit()

def get_results(user):
	c.execute("SELECT result, count(result) FROM results WHERE user = (?) GROUP BY result ORDER BY result DESC", (user,))
	results = c.fetchall()
	return results
	print (results)

def add_challenger(user):
	try:
		c.execute("INSERT INTO challengers SELECT (?) WHERE NOT EXISTS (SELECT 1 FROM challengers WHERE user = (?))", (user, user,))
		print ("Challenger added to queue.")
		conn.commit()
	except sqlite3.IntegrityError:
		print ("Challenger not added.")

def remove_challenger(result):
	c.execute("SELECT * FROM challengers WHERE ROWID IN (SELECT ROWID FROM challengers ORDER BY ROWID ASC LIMIT 1)")
	challenger = c.fetchone()
	challenger = challenger[0]
	c.execute("DELETE FROM challengers WHERE ROWID IN (SELECT ROWID FROM challengers ORDER BY ROWID ASC LIMIT 1)")
	conn.commit()
	add_result(challenger, result)

def add_points(user, pts):
	c.execute("SELECT points FROM points WHERE user = (?)", (user,))
	u = c.fetchone()
	if u != None:
		new_points_total = int(u[0]) + int(pts)
		c.execute("UPDATE points SET points = (?) WHERE user = (?)", (new_points_total, user,))
		conn.commit()
	else:
		c.execute("INSERT INTO points VALUES (?,?)", (user, pts,))
		conn.commit()

def subtract_points(user, pts):
	c.execute("SELECT points FROM points WHERE user = (?)", (user,))
	u = c.fetchone()
	new_points_total = int(u[0]) - int(pts)
	c.execute("UPDATE points SET points = (?) WHERE user = (?)", (new_points_total, user,))
	conn.commit()

def get_points(user):
	c.execute("SELECT points FROM points WHERE user = (?)", (user,))
	points = c.fetchone()
	return points[0]

def get_player(user):
	c.execute("SELECT pid FROM players WHERE pid = (?)", (user,))
	player = c.fetchone()
	return player