from random import choice
from itertools import permutations
from fractions import Fraction


def avg(x):
	# x: list of floats/ints
	return round(sum(x)/len(x), 10)


def prob_win(x, others):
	# x: float
	# others: list of floats
	#
	# returns the probability that player "x" wins given what the others play
	# ASSUMES ALL VALUES DISTINCT

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


def print_dict(d, level):
	# d: dict
	# level: int
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


def make_next_dict(d):
	# d: dict
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



def get_fractions():
	# fractions = [i/80 for i in range(0, 80+1)]

	eps = 1 / 10000000
	fractions = set([0, 1, eps, 1-eps])
	# fractions.add(2*eps)
	# fractions.add(1-2*eps)

	for denom in [2,3,4,5,6]:
		for num in range(1, denom):
			f = num/denom # Fraction(num, denom)
			fractions.add(f)
			fractions.add(f + eps)
			# fractions.add(f + 2 * eps)
			fractions.add(f - eps)
			# fractions.add(f - 2 * eps)
	return fractions


def main():

	n_players = int(input("number of players?\n"))
	print("solving the problem for", n_players, "players...")

	X = {i : [] for i in permutations(get_fractions(), n_players)}

	for i in range(n_players):
		X = make_next_dict(transform_dict(X))

	print("\n...solved. optimal selections:")
	print_dict(X, 0)



if __name__== "__main__":
	main()