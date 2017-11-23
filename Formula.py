from Clause import Clause

class Formula:
    """ File format
        p wcnf 4 5 15
        15 1 -2 4 0
        15 -1 -2 3 0
        1 -2 -4 0
        1 -3 2 0
        1 1 3 0
    """

    def __init__(self, num_literals = 0, hard_cost = 1, clause_list = []):
        self.soft_clauses, self.hard_clauses = self.__filter_clauses(clause_list)
        self.num_literals = num_literals
        self.hard_cost = hard_cost


    def __filter_clauses(self, clause_list):
        if len(clause_list) == 0:
            return [], []

        soft_clauses = filter(lambda c :not (c.cost == self.hard_cost), clause_list)
        hard_clauses = filter(lambda c : c.cost == self.hard_cost, clause_list)

        return soft_clauses, hard_clauses


    def add_clauses(self, clauses):
        for c in clauses:
            self.add_clause(c)


    def add_clause(self, clause):
        if clause.cost == self.hard_cost:
            self.hard_clauses.append(clause)
        else:
            self.soft_clauses.append(clause)


    def read_file(self, file_path):
        for line in open(file_path):
            if "wcnf" in line: # first line
                # Get num
                self.num_literals = int(line.split()[2])
                # Get hard_cost
                self.hard_cost = int(line.split()[4])
            else:
                cost = int(line.split()[0])
                if cost == self.hard_cost:   # if hard clause
                    self.hard_clauses.append(Clause.clause_from_dimacs_line(line))
                else:
                    self.soft_clauses.append(Clause.clause_from_dimacs_line(line))

        self.aux_count = self.num_literals


    def create_literal(self):
        self.num_literals += 1
        return self.num_literals


    def to_1_3(self):
        new_formula = Formula(self.num_literals,self.hard_cost)

        for soft_clause in self.soft_clauses:
            new_formula.add_clauses(new_formula.__convert_soft(soft_clause))

        for hard_clauses in self.hard_clauses:
            new_formula.add_clauses(new_formula.__convert_hard(hard_clauses))

        return new_formula


    def __convert_soft(self, soft):
        new_literal = self.create_literal()
        new_soft = Clause(soft.cost, [new_literal * (-1)]) # (!b,soft_cost)
        soft.add(new_literal)
        new_hard = Clause(self.hard_cost, soft.literals)
        hardslist = self.__convert_hard(new_hard)
        return [new_soft] + hardslist


    def __convert_hard(self, hard):
        clause = Clause(self.hard_cost,[])
        clause_list = []

        clause.add(hard.literals[0])
        literals_left = len(hard.literals) - 1

        for literal in hard.literals[1:]:
            if len(clause.literals) == 2:
                if literals_left == 1:
                    clause.add(literal)
                else:
                    literal_aux=self.create_literal()
                    clause.add(literal_aux)
                    clause_list+=[clause]
                    clause = Clause(self.hard_cost,[literal_aux * (-1)])
                    clause.add(literal)
                    literals_left-=1

            elif len(clause.literals) == 1:
                clause.add(literal)
                literals_left-=1

        return clause_list + [clause]


    def __str__(self):
        # Calculate num_clauses
        num_clauses = len(self.hard_clauses) + len(self.soft_clauses)

        # Get hard_cost
        hard_cost = self.hard_clauses[0].cost

        # Format first line of dimacs
        f_line = "p wcnf " + str(self.num_literals) + " " \
                            + str(num_clauses) + " " \
                            + str(self.hard_cost) + "\n"
        # Fomrat soft clauses
        soft_clauses = "\n".join(map(str, self.soft_clauses)) + "\n"
        # Format hard claues
        hard_clauses = "\n".join(map(str, self.hard_clauses))
        return f_line + soft_clauses + hard_clauses

if __name__ == '__main__':
    f = Formula()
    f.read_file('dimacs.txt')
    print str(f)
