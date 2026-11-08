from project.problem import Problem
import argparse


class Minimalisation(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments
        """
        parser.add_argument('--mini', help='', action='store_true')

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return bool(args.mini)

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
            q_s: dict = {}  # dict q -> S
            si = 0 #s index
            for lines in f.readlines():
                a,b,c = lines.split()
                if a not in states:
                    print(f"'{a}' is not a valid state: {states}")
                    exit()
                if c not in states:
                    print(f"'{c}' is not a valid state: {states}")
                    exit()
                if b not in alphabet:
                    print(f"'{b}' is not a valid symbol: {alphabet}")
                    exit()
                if not q_s.__contains__(a):
                    q_s[a] = f's{si}'
                    si += 1
                if transitions.__contains__((a, b)): transitions[(a, b)] += [c]
                else: transitions[(a, b)] = [c]

            starred = []
            not_starred = []

            #base stars list
            for e in end:
                for st in states:
                    if st in end: continue
                    starred += [(e, st)]
            #no stars list
            for st1 in states:
                for st2 in states:
                    if st1 == st2: continue
                    if (st1, st2) in starred or (st2, st1) in starred: continue
                    if (st2, st1) in not_starred: continue
                    not_starred += [(st1, st2)]
            #filling stars list
            stars = True
            while stars:
                stars = False
                for nst in not_starred:
                    a,b = nst
                    for sym in alphabet:
                        at = transitions[(a, sym)][0]
                        bt = transitions[(b, sym)][0]
                        if at == bt: continue
                        if at in end or bt in end or (at, bt) in starred or (bt, at) in starred:
                            if (a,b) not in starred and (b,a) not in starred:
                                starred += [(a,b)]
                                stars = True
            #removing starred pairs from the no-star list
            for star in starred:
                if star in not_starred:
                    not_starred.remove(star)
            #renaming the nodes without a star
            for nst in not_starred:
                q_s[ nst[1] ] = q_s[ nst[0] ]
            #removing duplicates and storing output
            out = set()
            s_states = set()
            for tr in transitions:
                s_states.add(q_s[tr[0]])
                out.add(f'{q_s[tr[0]]} {tr[1]} {q_s[ transitions[tr][0] ]}')

        # Write the result into the file
        with open(output_file, 'w') as f:
            f.write(' '.join(sorted(s_states)) + '\n')
            f.write(' '.join(alphabet)+'\n')
            f.write(q_s[start]+'\n')
            ends = set()
            for q in q_s:
                for e in end:
                    if q == e:
                        ends.add(q_s[q])
            f.write(' '.join(sorted(ends))+'\n')
            f.write('\n'.join(sorted(out)))