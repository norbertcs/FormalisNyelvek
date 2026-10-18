from project.problem import Problem
import argparse


class Deterministic(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments
        """
        parser.add_argument('--det', help='', action='store_true')

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return bool(args.det)

    def run(self, args):
        """
        Run the program
        """
        # Access the input and output file paths
        input_file = args.input
        output_file = args.output

        with open(input_file, 'r') as f:
            states = f.readline().split()
            alphabet = f.readline().split()
            start = f.readline().strip()
            end = f.readline().split()
            transitions: dict = {}
            for lines in f.readlines():
                a,b,c = lines.split()
                if transitions.__contains__((a, b)): transitions[(a, b)] += [c]
                else: transitions[(a, b)] = [c]

            # print(transitions)

            q_s : dict = {} # dict q -> S
            s_t : dict = {} # S transitions
            s_i = 0         # index of S
            queue = [tuple([start])]
            q_s[queue[0]] = 's' + str(s_i)
            s_i += 1
            for tup in queue:
                for a in alphabet:
                    list_of_t = set()
                    for i in tup:
                        if transitions.__contains__((i, a)):
                            for i_lt in transitions[(i, a)]: list_of_t.add(i_lt)
                    if list_of_t.__len__() == 0: continue;
                    list_of_t = tuple(sorted(list_of_t))
                    if not q_s.__contains__(list_of_t):
                        q_s[list_of_t] = 's' + str(s_i)
                        s_i += 1
                    s_t[(q_s[tup], a)] = q_s[list_of_t]

                    if not queue.__contains__(list_of_t):
                        if not list_of_t == tup:
                            queue += [list_of_t]

            # print(f"S list: {q_s}")
            # print(f"S trans: {s_t}")

        # Write the result into the file
        with open(output_file, 'w') as f:
            f.write(' '.join(q_s.values()) + '\n')
            f.write(' '.join(alphabet)+'\n')
            f.write(q_s[tuple([start])]+'\n')
            ends = []
            for tup in q_s:
                for i in tup:
                    for e in end:
                        if i == e:
                            ends += [ q_s[tup] ]
            f.write(' '.join(ends)+'\n')
            for tr in s_t:
                f.write(f"{tr[0]} {tr[1]} {s_t[tr]}\n")