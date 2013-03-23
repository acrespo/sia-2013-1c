# ?
import copy


number_of_states = 0
number_of_explosions = 0


def get_lines(match):
    line1, line2 = match
    if line1 < 0:
        line1 = -line1
    if line2 < 0:
        line2 = -line2
    return line1-1, line2-1

def get_positions(match):
    position1 = 0 if match[0] > 0 else -1
    position2 = 0 if match[1] > 0 else -1
    return position1, position2

class Board(object):

    def __init__(self, tiles, number_of_tiles = None):
        self.__tiles = tiles

    def get_border_sets(self):
        """Returns a list of sets of removable tiles.
        Each set is represented as the number of tiles in that set.
        """

        tile_sets = {}
        for line in self.__tiles:
            line_len = len(line)
            if line_len > 0:
                tile_sets[line[0]] = tile_sets.get(line[0], 0) + 1
            if line_len > 1:
                tile_sets[line[-1]] = tile_sets.get(line[-1], 0) + 1

        return tile_sets.values()

    def get_matches(self):
        """Returns a list of tuples with the possible moves.
        (token1, token2). token1 and token2 are integers in the range
        [1..len(self.__tiles)] if the token is on the left
        [-len(self.__tiles)..-1] if the token is on the right side
        """
        matches = []
        for line in range(len(self.__tiles)):
            if not self.__tiles[line]:
                continue
            # Lefty with another lefty
            for second_line in range(line+1, len(self.__tiles)):
                if not self.__tiles[second_line]:
                    continue
                if self.__tiles[line][0] == self.__tiles[second_line][0]:
                    matches.append((line+1, second_line+1))
            # Lefty with righty
            for second_line in range(len(self.__tiles)):
                if len(self.__tiles[second_line]) <= 1:
                    # Either empty or already covered as lefty + lefty
                    continue
                if self.__tiles[line][0] == self.__tiles[second_line][-1]:
                    matches.append((line+1, ~second_line))
            # righty with righty
            if len(self.__tiles[line]) == 1: # Skip, already covered as a lefty
                continue
            for second_line in range(line+1, len(self.__tiles)):
                if not self.__tiles[second_line]:
                    continue
                if self.__tiles[line][-1] == self.__tiles[second_line][-1]:
                    matches.append((~line, ~second_line))
        return matches

    def mutate_board(self, match):
        new_tiles = copy.deepcopy(self.__tiles)

        line1, line2 = get_lines(match)
        position1, position2 = get_positions(match)
        new_tiles[line1].pop(position1)
        new_tiles[line2].pop(position2)

        return Board(new_tiles)

    def get_kind_for_match(self, match):
        line1, line2 = get_lines(match)
        position1, position2 = get_positions(match)
        return self.__tiles[line1][position1]

    def number_of_lines(self):
        return len(self.__tiles)

    def is_empty(self):
        return not len([line for line in self.__tiles if len(line)])

    def tiles_left(self):
        return sum(len(l) for l in self.__tiles)

    def __repr__(self):
        return repr(self.__tiles)

    def __hash__(self):
        return sum([line[0] for line in self.__tiles if line])

    def _get_board(self):
        return self.__tiles

    def __eq__(self, other):
        return other._get_board() == self.__tiles

def count_kinds(board, kind):
    count = 0
    for line in board._get_board():
        for item in line:
            if item == kind:
                count += 1
    return count

class State(object):

    def __init__(self, board, depth, parent, kinds=None):
        self.board = board
        self.depth = depth
        self.parent = parent
        self.kinds = kinds
        self.h = 0
        global number_of_states
        self.creation_number = number_of_states
        number_of_states += 1
        if not self.kinds:
            self.kinds = {
                kind: count_kinds(self.board, kind)
                      for kind in range((board.tiles_left() + depth*2)/4)
            }

    def is_empty(self):
        return self.board.is_empty()

    def get_new_boards(self):
        global number_of_explosions
        number_of_explosions += 1

        matches = self.board.get_matches()
        new_states = []
        for match in matches:
            kind = self.board.get_kind_for_match(match)
            new_kinds = copy.deepcopy(self.kinds)
            new_kinds[kind] -= 2
            new_state = State(self.board.mutate_board(match), self.depth + 1,
                              self, new_kinds)
            new_states.append(new_state)
        return new_states

    def __repr__(self):
        return "State %d: (h = %d, depth = %d, board = '%s')" % (
                self.creation_number, self.h, self.depth, repr(self.board))

    def __hash__(self):
        return self.board.__hash__()

    def __eq__(self, other):
        return self.board.__eq__(other.board)

