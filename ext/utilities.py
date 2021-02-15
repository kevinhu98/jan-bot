from ext.setup import connectToDB
import ast
import operator

poe_client = connectToDB()

_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Invert: operator.neg,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
}


class Calc(ast.NodeVisitor):

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return _OP_MAP[type(node.op)](left, right)

    def visit_Num(self, node):
        return node.n

    def visit_Expr(self, node):
        return self.visit(node.value)

    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])


def find(requested_item) -> bool:
    item_collections = poe_client.list_collection_names()
    item_collections.remove('currencies')
    item_collections.remove('users')
    exact_requested_item = '^{item}$'.format(item=requested_item)  # regex for exact match
    stripped_requested_item = requested_item.lower().replace("'", '')  # punctuation removed and lowercase
    for collection_name in item_collections:
        specific_type_collection = poe_client.get_collection(collection_name)

        name_item_search = specific_type_collection.find_one({'name': {'$regex': exact_requested_item, '$options': 'i'}})  # search only by name
        stripped_search = specific_type_collection.find_one({'aliases': stripped_requested_item})

        if name_item_search or stripped_search:  # search by name, case insensitive
            found_item = dict(name_item_search or stripped_search)
            return found_item

    return None


def strip(input_string):
    return input_string.lower().replace("'", "")

