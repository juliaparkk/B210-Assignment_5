## a. What is the purpose of this program(s)?
This script finds song titles that are exactly a given character length — or, if none match exactly, returns the title(s) whose lengths are closest to the requested length — using titles loaded from taylor_discography.csv
## b. What does the program do, including what it takes for input, and what it gives as output?
The program loads song titles from the CSV’s track_name column (or uses a built-in sample). Then, when you enter a number, it searches all loaded titles and returns any titles with length == number; otherwise, it returns titles with the smallest absolute difference in length (ties included). It also provides interactive utilities to inspect and search the loaded titles.
The inputs are the CSV file, the titles, which are a list of strings loaded from the CSV, and user inputs, which are integers greater than or equal to 0.
The output is a printed list of matching titles (and lengths when appropriate). The function can return (title, length) pairs internally.
## c. How do you use the program?
1. Run the script (PowerShell)
If you usually run Python with the full path (you used Anaconda earlier), paste this exact line into PowerShell and press Enter:
  & 'C:\Users\jinas\anaconda\python.exe' 'C:\Users\jinas\Downloads\Assignment 5 User-Defined Functions.py'
  If Python is on PATH instead, use:
  python 'C:\Users\jinas\Downloads\Assignment 5 User-Defined Functions.py'
What the program prints on startup
  Either:
  "Loaded N titles from CSV: c:\Users\jinas\Downloads\taylor_discography.csv" (good — the program will search the whole CSV), or
  "CSV not available or could not be parsed — using sample list." (then only the fallback sample will be searchable)
  Then you immediately see the interactive prompt:
2. Enter target length (or 'q' to quit): This number must be an integer (whole number) greater than or equal to 0. 
  The program returns any titles with exact length N; if none, it returns the title(s) whose length is closest to N (ties included).
3. Use q (or quit / exit) to exit the program.
Essential usage notes (copy-pasteable)
  Do NOT paste shell/PowerShell commands into the program prompt — quit the program first (q), then paste the shell command into PowerShell.
  If the program prints “using sample list”, type list to confirm the small fallback list is loaded.
  If CSV should have loaded but didn’t, run this in PowerShell and paste the output back to me:
    Get-Item "C:\Users\jinas\Downloads\taylor_discography.csv" | Select-Object FullName,Length,LastWriteTime
    Get-Content -Path "C:\Users\jinas\Downloads\taylor_discography.csv" -TotalCount 1
    (Get-Content "C:\Users\jinas\Downloads\taylor_discography.csv" | Measure-Object -Line).Lines
