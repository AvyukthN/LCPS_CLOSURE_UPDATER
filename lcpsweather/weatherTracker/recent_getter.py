with open("detected_tweets.txt") as f:
	lines = f.read()
	lines = lines.split("https")
	lines = lines[0] + " https" + lines[1]
        #lines = lines[0]

print(lines)
