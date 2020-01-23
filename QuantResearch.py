"""
Three players A, B, C play the following game.
First, A picks a real number between 0 and 1 (both inclusive),
then B picks a number in the same range (different from A’s choice)
and finally C picks a number, also in the same range, (different from the two chosen numbers).
We then pick a number in the range uniformly randomly.
Whoever’s number is closest to this random number wins the game.
Assume that A, B and C all play optimally and their sole goal is to maximise their chances of winning.
Also assume that if one of them has several optimal choices,
then that player will randomly pick one of the optimal choices.

--If A chooses 0, then what is the best choice for B?
--What is the best choice for A?
--Can you write a program to figure out the best choice for the first player
when the game is played among four players?
"""


from random import choice
from itertools import permutations
from fractions import Fraction

###############################################################
# Utility Functions
###############################################################

def avg(x):
	return round(sum(x)/len(x), 10)

def print_dict(d, level):
	# d: dict
	# level: int
	if level == 0:
		print("optimal choices:")

	for k,v in d.items():
		if type(v) == dict:
			print(k, ":")
			print_dict(v, level+1)
		else:
			space = ""
			for i in range(level):
				space += "  "
			print(space, k, ":")
			for j in v:
				print(j)
	print()

def transform_dict(d):
	# d: dict
	new_dict = {}

	for key,vals in d.items():
		outer_key = key[:-1]
		inner_key = key[-1]

		if outer_key not in new_dict:
			new_dict[outer_key] = {}

		new_dict[outer_key][inner_key] = vals

	return new_dict


###############################################################
# Game-specific Functions
###############################################################

def get_fractions():
	# returns the discretized state-space we work on:
	# the list of possible choices for each player

	eps = 1 / 10000000
	fractions = set([0, 1, eps, 1-eps])
	# fractions.add(2*eps)
	# fractions.add(1-2*eps)

	for denom in [2,4,6,8]:
		for num in range(1, denom):
			f = num/denom # Fraction(num, denom)
			fractions.add(f)
			fractions.add(f + eps)
			fractions.add(f - eps)

			# fractions.add(f + 2 * eps)
			# fractions.add(f - 2 * eps)
	return fractions

def prob_win(x, others):
	# returns the probability that someone playing "x" wins given what the others play

	value = -2

	m = min(others)
	M = max(others)

	if x < m:
		value = x + (m - x)/2

	elif x > M:
		value = 1 - x + (x - M)/2

	elif x > m and x < M:
		others_less = [j for j in others if j < x]
		other_greater = [j for j in others if j > x]

		left = max(others_less)
		right = min(other_greater)

		value = (x - left)/2 + (right - x)/2

	return round(value, 10)

def make_next_dict(d):
	# d: dict
	# 
	# memoization, gives optimal choices for each player at different game "levels"

	next_dict = {}

	for prev in d.keys():

		# find best choice

		optimal_P = -1
		optimal_choices = []

		for choice in d[prev].keys():
			if len(d[prev][choice]) == 0:
				p_win = prob_win(choice, prev)

			else:
				p_win = avg([prob_win(choice, prev + post) for post in d[prev][choice]])

			if p_win > optimal_P:
				optimal_P = p_win
				optimal_choices.clear()
				optimal_choices.append(choice)

			elif p_win == optimal_P:
				optimal_choices.append(choice)


		next_dict[prev] = []

		for oc in optimal_choices:
			if len(d[prev][choice]) == 0:
				next_dict[prev].append((oc,))
			
			else:
				for post in d[prev][oc]:
					next_dict[prev].append((oc,) + post)

	return next_dict

###############################################################
###############################################################
###############################################################




n_players = int(input("\nEnter number of players: "))
assert(1 < n_players < 6)



print("\nSOLVING...")
print("using backwards induction on a modified (finite, discrete) state-space")

X = {i : [] for i in permutations(get_fractions(), n_players)}

for i in range(n_players):
	X = make_next_dict(transform_dict(X))

print("...SOLVED!\n")
print_dict(X, 0)

print("strategy profiles for", n_players, "players:")

if n_players == 2:
	print("A : 1/2")
	print("B : random selection from {1/2 + epsilon, 1/2 - epsilon}")
	pass

elif n_players == 3:
	print("A : random selection from {1/4, 3/4}")
	print("B : {1/4 if A==3/4; 3/4 if A==1/4}")
	print("C : random selection from (1/4, 3/4)")

elif n_players == 4:
	print("A : random selection from {1/6, 5/6}")
	print("B : {1/6 if A==5/6; 5/6 if A==1/6}")
	print("C : 1/2")
	print("D : random selection from (1/6, 1/2) U (1/2, 5/6)")

elif n_players == 5:
	print("(WARNING -- May be incorrect due to finite state-space approximation)")
	print("A : random selection from {1/8, 7/8}")
	print("B : random selection from {3/8, 5/8}")
	print("C : {1/8 if A==7/8; 7/8 if A==1/8}")
	print("D : {3/8 if B==5/8; 5/8 if B==3/8}")
	print("E : random selection from (1/8, 3/8) U (3/8, 5/8) U (5/8, 7/8)")

