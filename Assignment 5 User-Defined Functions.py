"""Assignment 5 — User-defined functions (no external modules)

This file provides a simple pure-Python implementation of a function that
finds song titles that are exactly a specified character length, or, if
none match exactly, the title(s) whose lengths are closest to the target.

No imports or external libraries are used.
"""


def find_titles_by_length(titles, target, return_lengths=False):
	"""Return titles with length exactly `target`, or the closest ones.

	Parameters
	----------
	titles : iterable of strings
		Song titles to inspect.
	target : int
		Desired character count (must be >= 0).
	return_lengths : bool, optional
		If True, return list of (title, length) tuples; otherwise return
		list of titles only. Default False.
	Returns
	-------
	list
		Either a list of titles (str) or a list of (title, length) tuples.

	Raises
	------
	ValueError
		If target is negative.
	"""
	# Input validation
	if not isinstance(target, int):
		raise TypeError("target must be an integer")
	if target < 0:
		raise ValueError("target must be non-negative")

	# Convert titles to list of (title, length)
	processed = []
	for t in titles:
		s = '' if t is None else str(t)
		processed.append((s, len(s)))

	if not processed:
		return []

	# Find exact matches
	exact = []
	for s, ln in processed:
		if ln == target:
			exact.append((s, ln) if return_lengths else s)
	if exact:
		return exact

	# Compute minimum absolute difference
	min_diff = None
	for _, ln in processed:
		diff = ln - target
		if diff < 0:
			diff = -diff
		if min_diff is None or diff < min_diff:
			min_diff = diff

	# Collect all titles with that min_diff
	result = []
	for s, ln in processed:
		d = ln - target
		if d < 0:
			d = -d
		if d == min_diff:
			result.append((s, ln) if return_lengths else s)

	return result


def _demo():
	# small demo for quick manual verification
	sample = ["Love Story", "Blank Space", "All Too Well (10 Minute Version)", "Mine", "You"]
	print('Sample:', sample)
	print('Exact length 4 ->', find_titles_by_length(sample, 4))
	print('Exact length 3 ->', find_titles_by_length(sample, 3))
	print('Closest to 7 ->', find_titles_by_length(sample, 7))


if __name__ == '__main__':
	# Run interactive loop so the user can input lengths repeatedly
	sample = ["Love Story", "Blank Space", "All Too Well (10 Minute Version)", "Mine", "You"]

	def interactive_title_search(titles):
		print("Interactive title search. Enter a number to find titles by length; type 'q' to quit.")
		while True:
			s = input("Enter target length (or 'q' to quit): ").strip()
			if s.lower() in ('q', 'quit', 'exit'):
				print('Goodbye.')
				break
			try:
				target = int(s)
			except ValueError:
				print("Please enter a whole number, or 'q' to quit.")
				continue
			results = find_titles_by_length(titles, target, return_lengths=True)
			if not results:
				print('No titles available to search.')
				continue
			print(f"Found {len(results)} result(s):")
			for title, ln in results:
				print(f"  {title}  (length={ln})")

	# Show a small demo then launch the interactive loop
	_demo()
	interactive_title_search(sample)


