import sys
import pickle
from copy import deepcopy

AVAILABLE_PRODUCTS = 'available_products'
DIMENSIONS = 'dimensions'
WAREHOUSES = 'warehouses'
CLIENTS = 'clients'
INITIAL_POSITION = 'initial_position'
NUMBER_OF_PRODUCTS = 'number_of_products'
ORDERS = 'orders'

plan = []
operators = []


class Fly:
    def __init__(self, startCell, stopCell):
        self.name = 'Fly'
        self.startCell = startCell
        self.stopCell = stopCell
        self.preconditions = [("Position", startCell)]
        self.additions = [("Position", stopCell)]
        self.deletions = [("Position", startCell)]

    def __str__(self):
        return '%s(%s, %s)' % (self.name, self.startCell, self.stopCell)


class Load:
    def __init__(self, productId, position):
        self.name = 'Load'
        self.productId = productId
        self.position = position
        self.preconditions = [("Empty",), ("Position", position), ("Warehouse", position),
                              ("hasProduct", position, productId)]
        self.additions = [("Carries", productId)]
        self.deletions = [("Empty",)]

    def __str__(self):
        return '%s(%s)' % (self.name, self.productId)


class Deliver:
    def __init__(self, productId, position):
        self.name = 'Deliver'
        self.productId = productId
        self.position = position
        self.preconditions = [("Carries", productId), ("Position", position), ("Client", position),
                              ("Order", position, productId)]
        self.additions = [("Empty",), ("OrderCompleted", position, productId)]
        self.deletions = [("Carries", productId)]

    def __str__(self):
        return '%s(%s)' % (self.name, self.productId)


def get_valid_operators(goal, state):
    valid_operators = []
    for operator in operators:
        if goal in operator.additions:  # and can_apply_operator(operator, state):
            valid_operators.append(operator)

    return valid_operators


def apply_operator(operator, state, stack):
    new_state = goals_regression(operator.preconditions, state, stack)

    if new_state:
        plan.append(operator)
        for e in operator.deletions:
            new_state.remove(e)
        return new_state + operator.additions
    else:
        return False


def accomplish_goal(goal, state, stack):
    if goal in state:
        # print(goal)
        return state

    if goal in stack:
        return False

    valid_operators = get_valid_operators(goal, state)
    # print(valid_operators)

    for operator in valid_operators:
        new_state = apply_operator(operator, state, stack + [goal])
        if new_state:
            stack.append(goal)
            return new_state

    return False


def goals_regression(goals, state, stack):
    for goal in goals:
        state = accomplish_goal(goal, state, deepcopy(stack))
        if not state:
            return False

    all_goals_satisfied = True
    for goal in goals:
        if goal not in state:
            u = False

    if all_goals_satisfied:
        return state
    return False


def make_plan(scenario):
    global plan
    global operators

    # generate goals
    goals = [("OrderCompleted", goal[0], goal[1]) for goal in scenario[ORDERS]]

    # generate initial state
    initial_state = [("Position", scenario[INITIAL_POSITION]), ("Empty",)]

    for warehouse in scenario[WAREHOUSES]:
        initial_state.append(("Warehouse", warehouse))

    for client in scenario[CLIENTS]:
        initial_state.append(("Client", client))

    for available_product in scenario[AVAILABLE_PRODUCTS]:
        initial_state.append(("hasProduct", available_product[0], available_product[1]))
        operators.append(Load(available_product[1], available_product[0]))

    for order in scenario[ORDERS]:
        initial_state.append(("Order", order[0], order[1]))
        operators.append(Deliver(order[1], order[0]))

    # generate possible operators
    n, m = scenario[DIMENSIONS]
    no_products = scenario[NUMBER_OF_PRODUCTS]

    for i in range(n):
        for j in range(m):
            for ii in range(n):
                for jj in range(m):
                    if (i, j) != (ii, jj):
                        operators.append(Fly((i, j), (ii, jj)))

    if goals_regression(goals, initial_state, []):
        return plan
    else:
        return False


def main(args):
    input = open('example.pkl', "rb")
    scenario = pickle.load(input)

    plan = make_plan(scenario)

    # print the plan
    print("Plan:")
    for operator in plan:
        print(operator)

    input.close()


if __name__ == '__main__':
    main(sys.argv)
