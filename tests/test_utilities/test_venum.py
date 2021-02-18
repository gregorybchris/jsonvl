from jsonvl._utilities.venum import Venum


class MockVenum(Venum):

    AAA = 'a'
    BBB = 'b'
    CCC = 'c'


class TestVenum:
    def test_has(self):
        assert MockVenum.AAA.value == 'a'
        assert MockVenum.BBB.value == 'b'
        assert MockVenum.CCC.value == 'c'

        assert MockVenum.has('a')
        assert MockVenum.has('b')
        assert MockVenum.has('c')

        assert not MockVenum.has('d')

    def test_get_all(self):
        assert MockVenum.get_all() == ['a', 'b', 'c']
