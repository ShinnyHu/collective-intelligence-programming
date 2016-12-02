import math
from PIL import Image,ImageDraw

people = ['Charlie', 'Augustus', 'Veruca', 'Violet', 'Mike', 'Joe', 'Willy', 'Miranda']

links = [('Augustus', 'Willy'),
		 ('Mike', 'Joe'),
		 ('Miranda', 'Mike'),
		 ('Violet', 'Augustus'),
		 ('Miranda', 'Willy'),
		 ('Charlie', 'Mike'),
		 ('Veruca', 'Joe'),
		 ('Miranda', 'Augustus'),
		 ('Willy', 'Augustus'),
		 ('Joe', 'Charlie'),
		 ('Veruca', 'Augustus'),
		 ('Miranda', 'Joe')]

def crosscount(v):
	# Convert the number list into a dictionary of person: (x, y)
	loc = dict([(people[i], (v[i*2], v[i*2+1])) for i in range(0, len(people))])
	total = 0

	# Loop through every pair of links
	for i in range(len(links)):
		for j in range(i+1, len(links)):
			# Get the locations
			(x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
			(x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]

			x1 = float(x1)
			x2 = float(x2)
			x3 = float(x3)
			x4 = float(x4)
			y1 = float(y1)
			y2 = float(y2)
			y3 = float(y3)
			y4 = float(y4)

			den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

			# den==0 if the lines are parallel
			if den == 0: continue

			# Otherwise ua and ub are the fraction of the line where they cross
			ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
			ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

			# If the fraciton is between 0 and 1 for both lines:
			# Then they cross each other
			if ua > 0 and ua < 1 and ub > 0 and ub < 1:
				total += 1

	# penalty when two nodes are two close
	for i in range(len(people)):
		for j in range(i+1, len(people)):
			# Get the locations of the two nodes
			(x1, y1), (x2, y2) = loc[people[i]], loc[people[j]]

			# Find the distance between them
			dist = float(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))
			# Penalize any nodes closer than 50 pixels
			if dist < 50:
				total += (1.0 - (dist/50))

	# penalty when the angel of links to one person is too small
	for i in range(len(links)):
		count = []
		for j in range(len(links)):
			# the link to the same person
			if links[i][0] == links[j][1]: 
				count.append(j)
			if links[i][0] == links[j][0] and i != j:
				count.append(...)
		print "i: %d" % i
		print count
		# iterate all the links to the same person
		for x in count:		
			degree = getdegree(i, x, loc)
			if -45 < degree < 45: 
				#print "degree: %d" % degree
				#print "i: %d, x: %d" % (i, x)
				total += 1
				#print "too small angle"

	return total

domain = [(10, 370)] * (len(people) * 2)


def drawnetwork(sol, jpeg="networks.jpg"):
	# Create the image
	img = Image.new('RGB', (400, 400), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	# Create the position dict
	pos = dict([(people[i], (sol[i*2], sol[i*2+1])) for i in range(0, len(people))])

	# Draw links
	for (a, b) in links:
		draw.line((pos[a], pos[b]), fill = (255, 0, 0))

	# Draw people
	for n, p in pos.items():
		draw.text(p,n,(0,0,0))

	img.save(jpeg,'JPEG')

def getdegree(i, j, loc):
	# Get the locations
	(x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
	(x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]

	dist1 = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
	dist2 = math.sqrt(math.pow(x3 - x4, 2) + math.pow(y3 - y4, 2))
	crossproduct = (x1-x2)*(x4-x3)+(y1-y2)*(y4-y3)
	cosine = crossproduct * 1.0 / ((dist1 * dist2) + 0.00001)
	cos = clean_cos(cosine)
	degree = math.acos(cos) * 360 / float(2 * math.pi)
	return degree

def clean_cos(cos_angle):
	# when cosine = -1, it seems that it is barely below and 
	# math.acos() will throw error
    return min(1,max(cos_angle,-1))














