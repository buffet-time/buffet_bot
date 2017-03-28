import socket
import cfg
import re
from time import sleep      # for sleep
from random import randint  # for random integer

# Connecting to Twitch Chat
soc = socket.socket()
soc.connect((cfg.HOST, cfg.PORT))
soc.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
soc.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
soc.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))
chatMsg = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

# variable initializations
counter = 0
counterMax = 600

# infinite loop -- the actual program
while True:

    response = soc.recv(1024).decode("utf-8")

    # keeps the bot from being disconnected automatically
    if response == "PING :tmi.twitch.tv\r\n":
        soc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("Pong!")

    # where the commands exist
    else:
        username = re.search(r"\w+", response).group(0)
        message = chatMsg.sub("", response)
        print(username + ": " + message)
        randomNum = randint(1, 12)

        for pattern in cfg.MP:
            if re.match(pattern, message):
                soc.send("PRIVMSG #buffet_time :Meme% is in fact best%\n".encode("utf-8"))
                break

        for pattern in cfg.NTC:
            if re.match(pattern, message):
                soc.send("PRIVMSG #buffet_time :@Not_Thomas_123\n".encode("utf-8"))
                break

        for pattern in cfg.RN:
            if re.match(pattern, message):
                soc.send("PRIVMSG #buffet_time :You Rolled: " + str(randomNum) + "\n".encode("utf-8"))
                break

        while True:
            counter += 1
            sleep(.5)
            print(counter)
            if counter == counterMax:
                soc.send("PRIVMSG #buffet_time :thatfeelwhenyoupickupadoublebarrelandCREAM\n".encode("utf-8"))
                counter = 0
