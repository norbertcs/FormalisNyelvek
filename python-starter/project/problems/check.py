from project.problem import Problem
import argparse


class SumProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments
        """
        parser.add_argument('--check', help='')

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return bool(args.check)

    def run(self, args):
        """
        Run the program
        """
        # Access the input and output file paths
        input_file = args.input
        output_file = args.output
        words = args.check.split(',')

        with open(input_file, 'r') as f:
            states = f.readline().split()
            alphabet = f.readline().split()
            start = f.readline().strip()
            end = f.readline().split()
            transitions: dict = {}
            for lines in f.readlines():
                a,b,c = lines.split()
                transitions[(a, b)] = c

        output_string = []
        for word in words:
            current_state = start
            for l in word:
                key = (current_state, l)
                current_state = transitions.get(key)
            if current_state not in end: output_string += ['NEM']
            else: output_string += ['IGEN']

        # Write the result into the file
        with open(output_file, 'w') as f:
            f.write('\n'.join(output_string))