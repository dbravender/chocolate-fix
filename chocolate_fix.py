# A solver for ThinkFun's Chocolate Fix game
# for puzzles with a lot of overlays it can be pretty slow but it can solve
# the final puzzle (level 40) for the game

from collections import defaultdict

from constraint import AllDifferentConstraint, FunctionConstraint, Problem

colors = ('p', 'b', 'w')
shapes = ('c', 's', 't')

pieces = tuple([color + shape
                for shape in shapes
                for color in colors])

locations = [(x, y) for x in range(3) for y in range(3)]


def get_constraints(criteria):
    if '?' not in criteria:
        return [criteria]
    if criteria[0] == '?':
        return [color + criteria[1] for color in colors]
    elif criteria[1] == '?':
        return [criteria[0] + shape for shape in shapes]


def floating_overlay(overlay):
    overlay_constraints = {}
    height = len(overlay)
    width = len(overlay[0])

    for x in range(height):
        for y in range(width):
            if overlay[x][y] is None:
                continue
            overlay_constraints[(x, y)] = get_constraints(overlay[x][y])

    offsets = [(x, y)
               for x in range(4 - height)
               for y in range(4 - width)]

    def func(*variables):
        assignments = {}
        for variable, location in zip(variables, locations):
            assignments[(location[0], location[1])] = variable
        for dx, dy in offsets:
            if all(assignments[(location[0] + dx,
                                location[1] + dy)] in constraints
                   for location, constraints in (
                       overlay_constraints.iteritems())):
                return True
        return False

    return func


def solve_board(overlays):
    problem = Problem()
    spot_constraints = defaultdict(list)
    for overlay in overlays:
        # the simplest case is a fully 3x3 grid
        if len(overlay) == 3 and len(overlay[0]) == 3:
            for x in range(3):
                for y in range(3):
                    if overlay[x][y] is None:
                        continue
                    spot_constraints[(x, y)].extend(
                        get_constraints(overlay[x][y]))
        else:
            # dealing with a grid that is smaller than 3x3 so we
            # need to make relative constraints
            problem.addConstraint(
                FunctionConstraint(floating_overlay(overlay)),
                locations)

    # the unspecified spots could be any piece
    for x in range(3):
        for y in range(3):
                if (x, y) not in spot_constraints:
                    spot_constraints[(x, y)] = pieces

    for spot, values in spot_constraints.iteritems():
        problem.addVariable(spot, values)

    problem.addConstraint(AllDifferentConstraint())

    solutions = problem.getSolutions()
    assert len(solutions) == 1, ('%d solutions but there should be 1' %
                                 len(solutions))
    solution = solutions[0]

    answer = [[None] * 3 for x in range(3)]
    for x in range(3):
        for y in range(3):
            answer[x][y] = solution[(x, y)]

    print('\n'.join(' '.join(_) for _ in answer))
    print('')

    return answer


____ = None

overlays = [[[____, ____, 'pc'],
             [____, 'ps', ____],
             ['bs', ____, ____]],
            [[____, 'pt', ____],
             ['bc', ____, 'wc'],
             [____, ____, ____]],
            [['wt', ____, ____],
             [____, ____, ____],
             [____, ____, 'bt']]]

assert solve_board(overlays) == [['wt', 'pt', 'pc'],
                                 ['bc', 'ps', 'wc'],
                                 ['bs', 'ws', 'bt']]

overlays = [[['p?', 'wc', ____],
             [____, 'ps', 'bc'],
             ['w?', 'pc', ____]],
            [[____, ____, 'ps'],
             ['b?', 'ws', ____],
             [____, ____, 'bs']]]

assert solve_board(overlays) == [['pt', 'wc', 'ps'],
                                 ['bt', 'ws', 'bc'],
                                 ['wt', 'pc', 'bs']]

overlays = [[['bt', ____, 'ps'],
             [____, ____, ____],
             [____, 'wt', ____]],
            [[____, ____, ____],
             [____, 'bc', ____],
             [____, ____, ____]],
            [[____, 'bs', ____],
             ['wc', ____, 'ws']],
            [[____, ____, ____],
             ['pt', ____, 'pc']]]

assert solve_board(overlays) == [['bt', 'bs', 'ps'],
                                 ['wc', 'bc', 'ws'],
                                 ['pt', 'wt', 'pc']]

overlays = [[['ps', '?c']],
            [['?t', 'pc']],
            [[____, ____],
             [____, 'w?'],
             ['?s', ____]],
            [[____, ____],
             [____, ____],
             ['w?', 'bs']],
            [['b?', ____],
             [____, ____],
             ['?t', ____]],
            [['?s', '?t']],
            [['?t', ____],
             [____, '?t']]]

assert solve_board(overlays) == [['bc', 'bt', 'pc'],
                                 ['ps', 'wc', 'pt'],
                                 ['ws', 'wt', 'bs']]
