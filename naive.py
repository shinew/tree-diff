import functools
# Naive O(F_1^2 * F_2^2) algorithm


# adapted from https://wiki.python.org/moin/PythonDecoratorLibrary
def memoize(f):
    cache = {}
    @functools.wraps(f)
    def g(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return g


empty_forest = ()
empty_node = None
class Tree(object):
    def __init__(self, label, children=empty_forest):
        self.label = label
        self.children = children

    @property
    @memoize
    def size(self):
        return sum(child.size for child in self.children) + 1


def cost(old_node, new_node):
    # This is the metric function for:
    # 1) adding a node if (old is empty and new is not empty)
    # 2) deleting a node if (old is not empty and new is empty)
    # 3) relabelling a node if (old is not empty and new is not empty)
    if old_node is empty_node or new_node is empty_node:
        return 1
    if old_node.label == new_node.label:
        return 0
    return 1


@memoize
def diff(old, new):
    v = old[-1] if old is not empty_forest else empty_node
    w = new[-1] if new is not empty_forest else empty_node
    old_minus_v = old[:-1] + v.children if old is not empty_forest else empty_forest
    new_minus_w = new[:-1] + w.children if new is not empty_forest else empty_forest

    if old is empty_forest and new is empty_forest:
        return 0
    if new is empty_forest:
        return diff(old_minus_v, empty_forest) + cost(v, empty_node)
    if old is empty_forest:
        return diff(empty_forest, new_minus_w) + cost(empty_node, w) 
    return min(
            diff(old_minus_v, new) + cost(v, empty_node),
            diff(old, new_minus_w) + cost(empty_node, w),
            diff(v.children, w.children) + diff(old[:-1], new[:-1]) + cost(v, w))


tree1 = Tree('f',
        (Tree('d',
            (Tree('a'),
             Tree('c', (Tree('b'),)))),
         Tree('e')))
tree2 = Tree('a',
        (Tree('c',
            (Tree('d',
                (Tree('a'), Tree('b'))),)),
         Tree('d')))

assert diff((tree1,), (tree1,)) == 0
assert diff((tree1,), (tree2,)) == 4
