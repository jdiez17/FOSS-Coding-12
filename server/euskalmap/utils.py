from random import shuffle

ROWS = 2
BLOCKS_PER_ROW = 5
ROWS_PER_BLOCK = 2
COLS_PER_BLOCK = 2

def get_near(letters, numbers, radius):
	"""
			
			AA1		AA2		AA3
			AB1		AB2		AB3
			
			BA1		BA2		BA3
				
			Number of locations close to a location: (9 * range) - 1
	"""
	
	directions = [
				(-1, -1), (-1, 0), (-1, 1),
				(0, -1), (0, 0), (0, 1),
				(1, -1), (1, 0), (1, 1)
			]
	
	locations = [(letters, numbers)]
	
	def compute(set):
		local_copy = []
		[local_copy.append(i) for i in set]
	
		for letters, numbers in local_copy:
			for dir in directions:
				discriminator = ord(letters[1]) + dir[0] - ord('A')
				l_letters = chr(ord('A') + discriminator / ROWS_PER_BLOCK) if discriminator % ROWS_PER_BLOCK == 0 else letters[0]
				l_letters += chr((ord('A') + discriminator % ROWS_PER_BLOCK if discriminator >= ROWS_PER_BLOCK else ord(letters[1]) + dir[0]))
				
				if ord(letters[1]) + dir[0] < ord('A'):
					continue
				
				l_numbers = numbers + dir[1]
				
				if numbers + dir[1] < 1:
					continue
				
				if not (l_letters, l_numbers) in locations:
					locations.append((l_letters, l_numbers))
		
	
	for i in range(0, radius):
		compute(locations)
		
	return locations
	

def trending_order(dataset):
	def trending(x, y):
		if x['comments'] > y['comments']:
			return -1
		elif x['comments'] == y['comments']:
			return 0
		else:
			return 1
	
	dataset.sort(trending)
	
	return dataset

def chrono_order(dataset):
	def chrono(x, y):
		if x['id'] > y['id']:
			return -1
		elif x['id'] == y['id']:
			return 0
		else:
			return 1
	
	if len(dataset) == 0:
		return dataset
	if "id" not in dataset[0].keys():
		return dataset # fail gracefully
		
	dataset.sort(chrono)
	
	return dataset
	
def random_order(dataset):
	shuffle(dataset)
	
	return dataset