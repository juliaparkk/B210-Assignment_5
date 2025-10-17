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
	# Run interactive loop so the user can input lengths repeatedly.
	# Attempt to load titles from the Taylor CSV (if present) using a
	# tiny no-module CSV parser; otherwise fall back to the sample list.
	csv_path = r"c:\Users\jinas\Downloads\taylor_discography.csv"

	def parse_csv_line(line):
		# Minimal CSV parser: handles commas and quoted fields with "" escapes.
		fields = []
		cur = []
		in_quotes = False
		i = 0
		while i < len(line):
			ch = line[i]
			if ch == '"':
				if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
					cur.append('"')
					i += 1
				else:
					in_quotes = not in_quotes
			elif ch == ',' and not in_quotes:
				fields.append(''.join(cur))
				cur = []
			else:
				cur.append(ch)
			i += 1
		fields.append(''.join(cur))
		return fields

	def load_titles_from_csv_no_module(path, column='track_name'):
		try:
			fh = open(path, 'r', encoding='utf-8')
		except Exception:
			return None
		with fh:
			# Read header
			header = fh.readline()
			if not header:
				return None
			# remove UTF-8 BOM if present
			if header.startswith('\ufeff'):
				header = header.lstrip('\ufeff')
			cols = parse_csv_line(header.strip('\n\r'))
			# find index of column (exact match)
			try:
				idx = cols.index(column)
			except ValueError:
				# helpful debug: print available columns for diagnosis
				print('CSV header columns:', cols[:10])
				return None
			titles = []
			for raw in fh:
				line = raw.strip('\n\r')
				if not line:
					continue
				fields = parse_csv_line(line)
				if idx < len(fields):
					titles.append(fields[idx])
			return titles

	# pick titles: CSV if available else the small sample
	titles = load_titles_from_csv_no_module(csv_path, 'track_name')
	if titles:
		print(f"Loaded {len(titles)} titles from CSV: {csv_path}")
	else:
		titles = ["Love Story", "Blank Space", "All Too Well (10 Minute Version)", "Mine", "You"]
		print("CSV not available or could not be parsed — using sample list.")

	def interactive_title_search(titles):
		print("Interactive title search. Enter a number to find titles by length; type 'q' to quit.")
		print("Commands: 'list' to show first 50 titles, 'all' to show all titles (confirm required).")
		while True:
			s = input("Enter target length (or 'q' to quit): ").strip()
			if not s:
				continue
			if s.lower() in ('q', 'quit', 'exit'):
				print('Goodbye.')
				break
			if s.lower() in ('l', 'list'):
				n = min(50, len(titles))
				print(f"Showing first {n} of {len(titles)} titles:")
				for i, t in enumerate(titles[:n], start=1):
					print(f"{i:4d}: {t}")
				continue
			if s.lower() == 'all':
				yn = input(f"This will print all {len(titles)} titles. Continue? (y/N): ").strip().lower()
				if yn == 'y':
					for i, t in enumerate(titles, start=1):
						print(f"{i:4d}: {t}")
				else:
					print('Cancelled.')
				continue
			# support "find <text>" to search by substring (case-insensitive)
			low = s.lower()
			if low.startswith('find ') or low.startswith('f '):
				query = s.split(' ', 1)[1].strip()
				if not query:
					print("Usage: find <text>")
					continue
				matches = [(t, len(t)) for t in titles if query.lower() in t.lower()]
				if not matches:
					print(f"No titles contain '{query}'.")
				else:
					print(f"Found {len(matches)} title(s) containing '{query}':")
					for t, ln in matches:
						print(f"  {t}  (length={ln})")
				continue

			# support "len N" to list titles with exact length N
			if low.startswith('len '):
				rest = s.split(' ', 1)[1].strip()
				try:
					n = int(rest)
				except Exception:
					print("Usage: len <N> where N is a whole number")
					continue
				matches = find_titles_by_length(titles, n, return_lengths=True)
				if not matches:
					print(f"No titles with exact length {n}.")
				else:
					print(f"Found {len(matches)} title(s) with length {n}:")
					for t, ln in matches:
						print(f"  {t}  (length={ln})")
				continue

			# default: interpret as integer target length
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

	# Launch the interactive loop (do not print demo at startup)
	interactive_title_search(titles)


