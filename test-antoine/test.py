with open("sampleNoDependencies.py") as f:
	line = f.readline()

	while line:
		print(line)
		exec(line)
		line = f.readline()
