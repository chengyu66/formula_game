"""
Modify by: Chengyu Xin
Student number: 1004068518
utorid: xincheng

# Copyright Nick Cheng, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.

# the symbol for OrTree and AndTree
SYMBOL = ['+', '*']

# Avoid magical numbers
# OrTree and AndTree will have two children
LEFT = 0
RIGHT = 1
# root.get_children()[LEFT] will be the left child of the root
# root.get_children()[RIGHT] will be the right child of the root
# NotTree has only one child
# root.get_children()[LEFT] will be its child of the root from NotTree

# PLAYER_INDEX contains two characters 'A', 'E' that indicate players turn
# the winning value of playerA is 0 which is the index of 'A' in the list
# the winning value of playerE is 1 which is the index of 'E' in the list
PLAYER_INDEX = ['A', 'E']


def get_root_index(formula):
    '''(str of formula) -> int
    This is a helper function to find the root in OrTree or AndTree
    It takes in a string of formula and returns the index of the root in it
    It returns len(formula) - 1 if didn't find the root (case of invalid)
    REQ: <formula> starts with '(' and ends with ')'
    >>> get_root_index('(x+y)')
    2
    >>> get_root_index('((x*z)+(y+x))')
    6
    >>> get_root_index('((x+y))')
    6
    '''
    # initialize a count for counting brakets
    count = 0
    # initialize an index i, starts at 1 since formula[0] is '('
    i = 1
    # count the brakets and loop through the formula to find the root
    # stops when we find the root or
    # until the end of the formula before last ')' (didn't find the root)
    while i < len(formula) - 1 and (count != 0 or formula[i] not in SYMBOL):
        # if '(' in current index i
        if formula[i] == '(':
            # count + 1
            count += 1
        # if ')' in current index i
        elif formula[i] == ')':
            # detect the case when ')' exists before '(' (invalid formula)
            if count == 0:
                # break the loop as we didn't find the root
                # -2 since we will add 1 in index at the end
                i = len(formula) - 2
            # else
            else:
                # count - 1
                count -= 1
        # add one in index i to loop through next character
        i += 1
    # return the index
    return i


def build_tree(formula):
    '''(str of formula) -> obj of FormulaTree
    This function takes in a string of formula and returns the FormulaTree
    that represents <formula> if it is a valid formula.
    Return None if the formula is not valid
    >>> build_tree('x')
    Leaf('x')
    >>> build_tree('-x')
    NotTree(Leaf('x'))
    >>> build_tree('(x+y)')
    OrTree(Leaf('x'), Leaf('y'))
    '''
    # default the result to be None
    # if it doesn't change the result (not go into any if statements),
    # then formula is invalid
    res = None
    # check if the formula is an empty string, b/c I need to use formula[0]
    if formula == '':
        # formula is invalid
        # do nothing since setted default of the result
        pass
    # base case when there is only one valid variable inside, like: 'x'
    elif len(formula) == 1 and formula.islower():
        # then it is a Leaf
        res = Leaf(formula)
    # check if the formula starts with '-'
    elif formula[0] == '-':
        # then it is a NotTree
        # keep recursing the formula after '-'
        res = NotTree(build_tree(formula[1:]))
    # check if the formula starts with '('
    elif formula[0] == '(' and formula[-1] == ')':
        # then it is an OrTree or AndTree
        # use get_root_index helper, find the index of the root in formula
        index = get_root_index(formula)
        # if we find the root (valid formula)
        if index != len(formula) - 1:
            # if the root is '+'
            if formula[index] == '+':
                # then it is an OrTree
                # split the formula into left child and right child
                # left child is on the left hand side of the '+' and vice versa
                res = OrTree(build_tree(formula[1:index]),
                             build_tree(formula[index + 1:-1]))
            # if the root is '*'
            elif formula[index] == '*':
                # then it is an AndTree
                # split the formula into left child and right child
                # left child is on the left hand side of the '*' and vice versa
                res = AndTree(build_tree(formula[1:index]),
                              build_tree(formula[index + 1:-1]))
    # if result have changed, but any of its child is None (formula invalid)
    if res and None in res.get_children():
        # adjust the result to be None again
        res = None
    # return the result
    return res


def draw_formula_tree(root):
    '''(obj of FormulaTree) -> str
    This function takes the FormulaTree rooted at <root> and returns the
    string that draws that tree
    (Change the \n to '\\n' for doctest in 3rd example)
    >>> draw_formula_tree(Leaf('x'))
    'x'
    >>> draw_formula_tree(NotTree(Leaf('x')))
    '- x'
    >>> draw_formula_tree(OrTree(Leaf('x'), Leaf('y')))
    '+ y\\n  x'
    '''
    def draw_helper(root, depth):
        '''(obj of FormulaTree, int) -> str
        This is a helper function which takes a FormulaTree root and the depth
        of this root in the original FormulaTree. Then returns the string that
        draws the tree from this root
        REQ: depth is greater or equals to 0
        '''
        # initialize the result string
        res = ''
        # if the root is a Leaf
        if isinstance(root, Leaf):
            # just simply add it's symbol
            res += root.get_symbol()
        # if the root is a NotTree
        elif isinstance(root, NotTree):
            # add the '-' sign with a space between its child
            res += root.get_symbol() + ' '
            # then keep recursing the only one child with 1 more in depth
            res += draw_helper(root.get_children()[LEFT], depth + 1)
        # else the root is an OrTree or AndTree
        else:
            # add it's symbol with a space between its right child
            res += root.get_symbol() + ' '
            # keep recursing its right child with 1 more in current depth
            # and go to the next line
            res += draw_helper(root.get_children()[RIGHT], depth + 1) + '\n'
            # add indent [2 * (depth + 1)] spaces in front of the left child
            res += '  ' * (depth + 1)
            # keep recursing its left child with 1 more in current depth
            res += draw_helper(root.get_children()[LEFT], depth + 1)
        # return the result
        return res
    # This is the main function
    # return the result of draw_helper function with same root and depth 0
    return draw_helper(root, 0)


def evaluate(root, variables, values):
    '''(obj of FormulaTree, str, str) -> int
    This function takes the FormulaTree rooted at <root>, a string <variables>
    containing the variables in the formula and a string <values> containing
    the corresponding truth values for the variables and returns the truth
    value(1 or 0) of the formula
    REQ: <variables> has all the variables in the formula
    REQ: <variables> and <values> have the same length
    REQ: <values> is made of '1' and '0'
    >>> evaluate(Leaf('x'), 'x', '0')
    0
    >>> evaluate(AndTree(Leaf('x'), Leaf('y')), 'yx', '11')
    1
    >>> evaluate(AndTree(OrTree(Leaf('x'), Leaf('y')), Leaf('x')), 'xy', '01')
    0
    '''
    # if root is a Leaf
    if isinstance(root, Leaf):
        # get the value of its represented variable by corresponding index
        result = values[variables.find(root.get_symbol())]
    # if root is an NotTree
    elif isinstance(root, NotTree):
        # not its one and only one child's return value
        result = not evaluate(root.get_children()[LEFT], variables, values)
    # if root is an OrTree
    elif isinstance(root, OrTree):
        # the result will be its (left child return value) or (right child
        # return value), since the return value can only be int(1 or 0)
        result = evaluate(root.get_children()[LEFT], variables,
                          values) or evaluate(root.get_children()[RIGHT],
                                              variables, values)
    # else root must be an AndTree
    else:
        # the result will be its (left child return value) and (right child
        # return value)
        result = evaluate(root.get_children()[LEFT], variables,
                          values) and evaluate(root.get_children()[RIGHT],
                                               variables, values)
    # return the integer result
    return int(result)


def play2win(root, turns, variables, values):
    '''(obj of FormulaTree, str, str, str) -> int
    This function takes the FormulaTree rooted at <root>, a string to indicate
    turns, a string <variables> containing the variables in the formula and
    a string <values> containing the corresponding truth values for the
    variables(formula game configuration) and returns the best next move
    (0 or 1) for the player whose turn is next
    REQ: the input is a valid formula game configuration
    REQ: length of <turns> must be greater than length of values
    REQ: <turns> is made of 'A' and 'E'
    >>> play2win(Leaf('x'), 'A', 'x', '')
    0
    >>> play2win(Leaf('x'), 'E', 'x', '')
    1
    >>> root = build_tree('((x+y)*((y+z)*(-y+-z)))')
    >>> play2win(root, 'EAA', 'xyz', '')
    1
    '''
    # determine the value to win for current player
    # PLAYER_INDEX contains two characters 'A', 'E' that indicate players turn
    # the winning value of playerA is 0 which is the index of 'A' in the list
    # the winning value of playerE is 1 which is the index of 'E' in the list
    win_value = PLAYER_INDEX.index(turns[len(values)])
    # check if there is a winning strategy if the player chooses 0
    choice0 = win_strategy(root, turns, variables, values + '0', win_value)
    # check if there is a winning strategy if the player chooses 1
    choice1 = win_strategy(root, turns, variables, values + '1', win_value)
    # if any choice would lead to win or there is no winning strategy at all
    if (choice0 and choice1) or (not choice0 and not choice1):
        # then choose the default value(winning value)
        result = win_value
    # if only choosing 0 would lead to win
    elif choice0:
        # choose 0 for next move
        result = 0
    # else only choosing 1 would lead to win
    else:
        # choose 1 for next move
        result = 1
    # return the result choice
    return result


def win_strategy(root, turns, variables, values, win_value):
    '''(obj of FormulaTree, str, str, str, int) -> bool
    This function is a helper function that takes a formula game configuration
    with a winning value of the current player and returns True if
    there is a winning strategy, vise and versa
    REQ: the input is a valid formula game configuration
    REQ: <win_value> can only be 0 or 1
    >>> win_strategy(OrTree(Leaf('x'), Leaf('y')), 'AE', 'xy', '', 0)
    False
    >>> win_strategy(OrTree(Leaf('x'), Leaf('y')), 'EA', 'xy', '1', 1)
    True
    >>> win_strategy(AndTree(Leaf('x'), Leaf('y')), 'AE', 'xy', '0', 1)
    False
    '''
    # if all values are chosen
    if len(turns) == len(values):
        # evaluate the game
        end = evaluate(root, variables, values)
        # let both results represent if the player can win the game
        # to make them do the same function as returning just one boolean
        # since I want to return (res0 and res1)
        res0 = (end == win_value)
        res1 = res0
    # else keep recursing(choosing values)
    else:
        # res0 is the result assuming next player will choose 0 in next turn
        res0 = win_strategy(root, turns, variables, values + '0', win_value)
        # res1 is the result assuming next player will choose 1 in next turn
        res1 = win_strategy(root, turns, variables, values + '1', win_value)
    # return if there is a winning strategy with current values
    return res0 and res1
