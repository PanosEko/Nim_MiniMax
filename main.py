class Node(object):
    """
    Represents a tree node.
    """
    def __init__(self, value, level, is_leaf):
        self.value = value  # Node value
        self.level = level  # Depth level
        self.children = []  # List with children nodes
        self.is_leaf = is_leaf  # Boolean. True if node is leaf
        self.minmax_eval = None  # Min-max evaluation value

    def add_child(self, child_node):
        """
        adds child node to parent nodes list
        :param child_node: Node object
        """
        self.children.append(child_node)

    # In this particular instance the parameter value is used to store
    # the remaining blocks of nim game


class NimGame:
    """
    A variation of the Nim game versus the computer
    Computer uses min-max decision rule to determine next move
    """
    def __init__(self):
        self.k = 0  # Maximum number of blocks that can be removed
        self.remaining_blocks = 0  # Number of remaining blocks
        self.winner = None  # Denotes game winner

    def start_new_game(self):
        """
        Starts a new Nim game
        """
        # Prompt user for maximum number of blocks to remove each turn
        while self.k < 3:
            self.k = int(input("Please select maximum number of blocks that "
                               "can be removed in each turn\n(must be integer "
                               "greater than 2)\n"))
        # Prompt user for starting number of blocks
        while self.remaining_blocks < self.k:
            self.remaining_blocks = int(input("Please select starting number of "
                                              "blocks (must be integer greater "
                                              f"than {self.k})\n"))

        # Repeatedly execute each players turn until there are no remaining blocks
        while self.remaining_blocks != 0:
            root = Node(self.remaining_blocks, 0, False)
            self.generate_tree(root)
            print("\nGame tree:")
            self.print_tree(root, False)
            self.run_minmax(root, 1)  # Evaluate tree with min-max
            print("\nGame tree with Minimax values:")
            self.print_tree(root, True)
            self.max_remove_blocks(root)  # MAXs turn
            if self.remaining_blocks == 0:
                break
            self.player_remove_blocks()  # Players turn

        #  Output winner to console
        if self.winner == "MAX":
            print("\nYou lose. Max wins. Good luck next time.")
        else:
            print("\nYou win! Congratulations you beat the computer!")

    def max_remove_blocks(self, node):
        """
        Executes Max's turn based on minmax evaluation of nodes.
        Max chooses node with maximum minmax value
        :param node: Root node at current phase of the game
        """
        max_choice = 0
        chosen_child = node.children[0]
        for child in node.children:
            if child.minmax_eval > max_choice:
                chosen_child = child
                max_choice = child.minmax_eval
        print(f"\nMax removes {self.remaining_blocks-chosen_child.value}"
              f" blocks.")
        self.remaining_blocks = chosen_child.value
        if self.remaining_blocks == 0:
            self.winner = "MAX"

    def player_remove_blocks(self):
        """
        Executes player's turn. Prompts player for number of blocks to remove.
        """
        while True:
            try:
                min_choice = int(input(f"There are {self.remaining_blocks} "
                                       f"blocks remaining. Do you want to "
                                       f"remove 1, 2 or {self.k} blocks?\n"))
                if min_choice != 1 and min_choice != 2 and min_choice != self.k or\
                        min_choice > self.remaining_blocks:
                    print(f"Error: Choice is not valid. Pick again.")
                else:
                    self.remaining_blocks -= min_choice
                    break
            except ValueError:
                print(f"Error: Number should be integer. Pick again.")
                continue

    def generate_tree(self, node):
        """
        Generates a tree that represents all possible player moves in a game of Nim
        Evaluates leaves depending on who won(1 for Max, 0 for Min)
        :param node: Starting node-root(Node object)
        """
        if node.value - self.k > 0:
            child1 = Node(node.value - self.k, node.level + 1, False)
            self.generate_tree(child1)
            node.add_child(child1)
        elif node.value - self.k == 0:
            if node.level % 2:
                minmax_value = 0
            else:
                minmax_value = 1
            leaf1 = Node(0, node.level + 1, True)
            leaf1.minmax_eval = minmax_value
            node.add_child(leaf1)
        if node.value - 2 > 0:
            child2 = Node(node.value - 2, node.level + 1, False)
            self.generate_tree(child2)
            node.add_child(child2)
        elif node.value - 2 == 0:
            if node.level % 2:
                minmax_value = 0
            else:
                minmax_value = 1
            leaf2 = Node(node.value - 2, node.level + 1, True)
            leaf2.minmax_eval = minmax_value
            node.add_child(leaf2)
        if node.value - 1 > 0:
            child3 = Node(node.value - 1, node.level + 1, False)
            self.generate_tree(child3)
            node.add_child(child3)
        elif node.value - 1 == 0:
            if node.level % 2:
                minmax_value = 0
            else:
                minmax_value = 1
            leaf3 = Node(0, node.level + 1, True)
            leaf3.minmax_eval = minmax_value
            node.add_child(leaf3)

    def run_minmax(self, node, max_turn):
        """
        Recursively evaluates each tree node based on min-max decision rule
        :param node: Starting node(root)
        :param max_turn: Boolean. Denotes max or min turn
        """
        if node.is_leaf:
            return node.minmax_eval

        if max_turn:
            max_eval = -999999999999
            for child in node.children:
                evaluation = self.run_minmax(child, False)
                max_eval = max(max_eval, evaluation)
            node.minmax_eval = max_eval
            return max_eval
        else:
            min_eval = 999999999999
            for child in node.children:
                evaluation = self.run_minmax(child, True)
                min_eval = min(min_eval, evaluation)
            node.minmax_eval = min_eval
            return min_eval

    def print_tree(self, node, show_value, indent=""):
        """
        Recursively generates tree structure as string and displays it in console
        :param node: Root node
        :param show_value: if true node value will be displayed for each node
        :param indent: indentation for each level
        """
        if show_value:
            print(indent[:-3] + "|_ " * bool(indent) + str(node.value) +
                  "(" + str(node.minmax_eval) + ")")
            for more, child in enumerate(node.children, 1 - len(node.children)):
                child_indent = "|  " if more else "   "
                self.print_tree(child, True, indent + child_indent)

        else:
            print(indent[:-3] + "|_ " * bool(indent) + str(node.value))
            for more, child in enumerate(node.children, 1 - len(node.children)):
                child_indent = "|  " if more else "   "
                self.print_tree(child, False, indent + child_indent)


def main():
    game = NimGame()
    game.start_new_game()


if __name__ == "__main__":
    main()
