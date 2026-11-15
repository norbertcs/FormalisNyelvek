from project.problem import Problem
import argparse
import re
from collections import Counter

class Minimalisation(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments
        """
        parser.add_argument('--rgx', help='', type=int, choices=[1, 2, 3, 4, 5])

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return bool(args.rgx)

    def run(self, args):
        """
        Run the program
        """
        # Access the input and output file paths
        input_file = args.input
        output_file = args.output

        with open(input_file, encoding="utf-8") as f:
            text = f.read()

        if args.rgx == 1:
            results = task1(text.splitlines())
        elif args.rgx == 2:
            results = task2(text)
        elif args.rgx == 3:
            results = task3(text)
        elif args.rgx == 4:
            results = task4(text)
        else:
            results = task5(text)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + ("\n" if results else ""))


TASK1_PATTERNS = [
    r"^10-15 ",                                            # 10. 15-en letrejott sorok
    r"^10-15 10:18:51\.[0-9]+ ",                           # 10-15, 10:18:51
    r"^[0-9-]+ [0-9]{2}:[0-9]{2}:51\.[0-9]+ ",             # 51 masodperckor
    r"[IDVEFAW] lowmemorykiller:",                         # lowmemorykiller tag
    r"^[0-9-]+ 10:18:51\.[0-9]+ +221 ",                    # 10:18:51, 221-es PID
    r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ E ",               # hibak (E)
    r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ W PackageManager:",# PackageManager warningok
    r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ D [^:\s]*ExoPlayer[^:\s]*:",    # ExoPlayer debug
    r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ [EW] .*\.java:",                # java pozicio E/W sorokban
    r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ [IDVEFAW] [^:]+: .*\bThread\b", # Thread az uzenetben
]
STACK_CLASS_RE = re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ E .*at .*?\((\w+\.java):[0-9]+\)", re.M)
PID_RE = re.compile(r"^[0-9-]+ [0-9:.]+ +([0-9]+) +[0-9]+ [IDVEFAW] ", re.M)
ERR_PID_RE = re.compile(r"^[0-9-]+ [0-9:.]+ +([0-9]+) +[0-9]+ E ", re.M)
MAIN_THREAD_ERR_RE = re.compile(r"^[0-9-]+ [0-9:.]+ +([0-9]+) +\1 E ", re.M)

def task1(lines):
    results = []
    for pattern in TASK1_PATTERNS:
        rgx = re.compile(pattern)
        results.append(str(sum(1 for line in lines if rgx.search(line))))
    return results

def task2(text):
    return STACK_CLASS_RE.findall(text)

def task3(text):
    return list(dict.fromkeys(PID_RE.findall(text)))

def task4(text):
    counts = Counter(ERR_PID_RE.findall(text))
    if not counts: return []
    pid, n = counts.most_common(1)[0]
    return [f"PID={pid} ({n} errors)"]

def task5(text):
    return [str(len(MAIN_THREAD_ERR_RE.findall(text)))]