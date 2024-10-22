import json
from code_gen import CodeGen
from anytree import Node, RenderTree


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.code_gen = CodeGen(self.scanner.symbol_table)
        self.grammar = self.get_grammar()
        self.first, self.follow = self.get_first_and_follow()
        self.non_terminals = self.get_non_terminals()
        self.terminals = self.get_terminals()
        self.ll1_table = self.generate_ll1_table()

    def get_grammar(self):
        """
                Read the grammar rules from a file and return them in dictionary format.

                :return: A dictionary where the keys are non-terminals and values are lists of right-hand side productions.
        """
        grammar = {}
        with open('grammar.txt', 'r') as f:
            for line in f:
                lhs = line.split('->')[0].strip()
                rhs = line.split('->')[1].strip()
                if not lhs in grammar:
                    grammar[lhs] = []
                grammar[lhs].append(rhs.strip())
        return grammar

    def get_first_and_follow(self):
        """
        Load the first and follow sets from a JSON file.

        :return: A tuple containing the first set and the follow set.
        """
        with open('fi_fo.json', 'r') as f:
            fi_fo = json.load(f)
        return fi_fo['first'], fi_fo['follow']

    def get_non_terminals(self):
        """
               Extract and return the list of non-terminal symbols from the grammar.

               :return: A list of non-terminal symbols.
        """
        non_terminals = self.grammar.keys()
        return non_terminals

    def get_terminals(self):
        """
                Extract and return the list of terminal symbols from the grammar by examining the right-hand sides of productions.

                :return: A list of terminal symbols.
        """
        terminals = []
        for lhs in self.grammar:
            for rhs in self.grammar[lhs]:
                for token in rhs.split(' '):
                    if token not in self.non_terminals and \
                            token != "EPSILON" and token != '|' \
                            and not token.startswith("#"):
                        terminals.append(token)

        terminals = list(set(terminals))
        return terminals

    def generate_ll1_table(self):
        """
                Generate the LL1 parsing table using the first and follow sets.

                :return: A dictionary representing the LL1 parsing table with (non-terminal, terminal) keys and right-hand side productions as values.
        """
        ll1_table = {}

        for lhs in self.grammar:
            for rhs in self.grammar[lhs]:
                flag = False
                for c in rhs.split(' '):
                    if c in self.terminals:
                        ll1_table[(lhs, c)] = rhs
                        flag = True
                    elif c in self.non_terminals:
                        if "EPSILON" not in self.first[c]:
                            flag = True
                        for fi in self.first[c]:
                            if fi != "EPSILON":
                                ll1_table[(lhs, fi)] = rhs
                    if flag:
                        break
                if not flag:
                    for fo in self.follow[lhs]:
                        ll1_table[(lhs, fo)] = rhs
            for fo in self.follow[lhs]:
                if (lhs, fo) not in ll1_table.keys():
                    ll1_table[(lhs, fo)] = "synch"
        return ll1_table

    def parse(self):
        """
                Perform LL1 parsing on the input tokens, generating a parse tree and handling syntax errors.
                The parse tree is written to a file, and errors are logged.
        """
        stack = ["$", "Program"]
        token = self.scanner.get_next_token()
        root = Node("Program")
        dummy = Node("$", parent=None)
        parents = {}
        anytree_stack = [dummy, root]
        parse_file = open("./parse_tree.txt", "w")
        error_file = open("./syntax_errors.txt", "w")
        error_exists = False
        while len(stack) > 0:
            if stack[-1].startswith("#"):
                action = stack.pop()[1:]
                self.code_gen.__getattribute__(action)(token.lexeme, token.line_num)
                continue
            elif stack[-1] == token.context:
                stack.pop()
                node = anytree_stack.pop()
                node.name = f"({token.type}, {token.lexeme})"
                if token.context == "$":
                    node.name = "$"
                if node in parents.keys():
                    node.parent = parents[node]
                if token.context != "$":
                    token = self.scanner.get_next_token()
            elif stack[-1] in self.non_terminals:
                if (stack[-1], token.context) not in self.ll1_table.keys():
                    if token.context == "$":
                        error_file.write(f"#{token.line_num} : syntax error, Unexpected EOF\n")
                        error_exists = True
                        break
                    error_file.write(f"#{token.line_num} : syntax error, illegal {token.context}\n")
                    error_exists = True
                    token = self.scanner.get_next_token()
                elif self.ll1_table[(stack[-1], token.context)] == "synch":
                    error_file.write(f"#{token.line_num} : syntax error, missing {stack.pop()}\n")
                    error_exists = True
                    anytree_stack.pop()
                else:
                    stack_father = stack.pop()
                    anytree_stack_father = anytree_stack.pop()
                    if anytree_stack_father in parents.keys():
                        anytree_stack_father.parent = parents[anytree_stack_father]
                    for phrase in self.ll1_table[(stack_father, token.context)].split(" ")[::-1]:
                        if phrase == "":
                            continue
                        if phrase != "EPSILON":
                            stack.append(phrase)
                            if not phrase.startswith("#"):
                                node = Node(phrase, parent=None)
                                parents[node] = anytree_stack_father
                                anytree_stack.append(node)
                        else:
                            node = Node("epsilon", parent=anytree_stack_father)
            else:
                if stack[-1] == "$":
                    while stack[-1] == "$" and token.context != "$":
                        token = self.scanner.get_next_token()
                    continue
                error_file.write(f"#{token.line_num} : syntax error, missing {stack[-1]}\n")
                error_exists = True
                stack.pop()
                anytree_stack.pop()
        for pre, fill, phrase in RenderTree(root):
            parse_file.write("%s%s\n" % (pre, phrase.name))
        if not error_exists:
            error_file.write("There is no syntax error.")
        parse_file.close()
        error_file.close()
        self.print_instructions()
        self.code_gen.write_semantic_errors()

    def print_instructions(self):

        if len(self.code_gen.semantic_errors):
            with open("output.txt", "w") as f:
                f.write("The code has not been generated.")

        else:
            print(self.code_gen.pb.items())
            self.code_gen.pb = dict(sorted(self.code_gen.pb.items()))
            with open("output.txt", "w") as f:

                for inst in self.code_gen.pb:
                    f.write(f"{inst}\t{self.code_gen.pb[inst]}\n")
