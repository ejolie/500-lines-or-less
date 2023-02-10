from objmodel import Class, Instance, TYPE, OBJECT


def test_bound_method():
    # Python code
    class A(object):
        def f(self, a):
            return self.x + a + 1

    obj = A()
    obj.x = 2
    m = obj.f
    assert m(4) == 7

    class B(A):
        pass

    obj = B()
    obj.x = 1
    m = obj.f
    assert m(10) == 12  # works on subclass too

    # Object model code
    def f_A(self, a):
        return self.read_attr("x") + a + 1

    A = Class(name="A", base_class=OBJECT, fields={"f": f_A}, metaclass=TYPE)
    obj = Instance(A)
    obj.write_attr("x", 2)
    m = obj.read_attr("f")
    assert m(4) == 7

    B = Class(name="B", base_class=A, fields={}, metaclass=TYPE)
    obj = Instance(B)
    obj.write_attr("x", 1)
    m = obj.read_attr("f")
    assert m(10) == 12
