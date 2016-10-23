import random

# List of available words to use in generation
set1_adject1 = ['Admired', 'Clever', 'Careless', 'Fair', 'Filthy', 'Fumbling', 'Idealistic', 'Salty', 'Shrill', 'Sweet', 'Delightful', 'Dangerous', 'Rich', 'Wealthy', 'Insanely', 'Astoundingly', 'Obviously', 'Deranged']
set2_adject2 = ['Vibrant', 'Posh', 'Nautical', 'Mean', 'Mindless','Lame', 'Jealous', 'Idle', 'Interesting', 'Eager', 'Magical', 'Mystical', 'Mysterious', 'Strange', 'Happy', 'Killer', 'Furious', 'Angry']
set3_nouns = ['Lad', 'Government', 'Master', 'Leader', 'Captain', 'User', 'Dealer', 'Dictator', 'Person', 'Reflection', 'Animal', 'Man', 'Shadow', 'Jester', 'Lump', 'Woman', 'Fighter', 'Hero', 'Villian']

# Generates a name, containing 1 word from each set above.
def generate_name():
   word1 = random.choice(set1_adject1)
   word2 = random.choice(set2_adject2)
   word3 = random.choice(set3_nouns)
   str = "The_" + word1 + "_" + word2 + "_" + word3
   return str

# Test generate_name functionality
"""
print "Completed Successfully"
print generate_name()
"""

def generate_name_lists():
	used = []
	while len(used) < 3000:
		name = generate_name()
		if not name in used:
			used.append(name)
			
	Bronze_1 = used[0:1000]
	Silver_1 = used[1000:2000]
	Gold_1 = used[2000:3000]
	all_three = [Bronze_1, Silver_1, Gold_1]
	return all_three
	
# print generate_name_lists size per section
"""
names = generate_name_lists()
print len(names[0])
print len(names[1])
print len(names[2])
"""

# Test for overlap
"""
for name in names[0]:
	if name in names[1]:
		print "problem"
for name1 in names[0]:
	if name1 in names[2]:
		print "problem"
for name2 in names[1]:
	if name2 in names[2]:
		print "problem"
"""