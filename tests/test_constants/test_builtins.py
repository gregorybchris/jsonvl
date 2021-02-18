import re

from jsonvl.constants.builtins import Collection, Primitive


class TestBuiltins:
    def test_primitives(self):
        primitives = Primitive.get_all()
        assert len(primitives) == 4
        for primitive in primitives:
            assert re.match(r'[a-z]{2,15}', primitive)

    def test_collections(self):
        collections = Collection.get_all()
        assert len(collections) == 2
        for collection in collections:
            assert re.match(r'[a-z]{2,15}', collection)
