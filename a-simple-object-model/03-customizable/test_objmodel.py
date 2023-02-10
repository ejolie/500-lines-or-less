from objmodel import Class, Instance, TYPE, OBJECT


def test_getattr():
    # Python code
    class A(object):
        def __getattr__(self, name):
            if name == "fahrenheit":
                return self.celsius * 9.0 / 5.0 + 32
            raise AttributeError(name)

        def __setattr__(self, name, value):
            if name == "fahrenheit":
                self.celsius = (value - 32) * 5.0 / 9.0
            else:
                # call the base implementation
                object.__setattr__(self, name, value)

    obj = A()
    obj.celsius = 30
    assert obj.fahrenheit == 86  # test __getattr__
    obj.celsius = 40
    assert obj.fahrenheit == 104

    obj.fahrenheit = 86  # test __setattr__
    assert obj.celsius == 30
    assert obj.fahrenheit == 86

    # Object model code
    def __getattr__(self, name):
        if name == "fahrenheit":
            return self.read_attr("celsius") * 9.0 / 5.0 + 32
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "fahrenheit":
            self.write_attr("celsius", (value - 32) * 5.0 / 9.0)
        else:
            # call the base implementation
            OBJECT.read_attr("__setattr__")(self, name, value)

    A = Class(
        name="A",
        base_class=OBJECT,
        fields={"__getattr__": __getattr__, "__setattr__": __setattr__},
        metaclass=TYPE,
    )
    obj = Instance(A)
    obj.write_attr("celsius", 30)
    assert obj.read_attr("fahrenheit") == 86  # test __getattr__
    obj.write_attr("celsius", 40)
    assert obj.read_attr("fahrenheit") == 104
    obj.write_attr("fahrenheit", 86)  # test __setattr__
    assert obj.read_attr("celsius") == 30
    assert obj.read_attr("fahrenheit") == 86


def test_get():
    # Python code
    class FahrenheitGetter(object):
        def __get__(self, inst, cls):
            return inst.celsius * 9.0 / 5.0 + 32

    class A(object):
        fahrenheit = FahrenheitGetter()

    obj = A()
    obj.celsius = 30
    assert obj.fahrenheit == 86

    # Object model code
    class FahrenheitGetter(object):
        def __get__(self, inst, cls):
            return inst.read_attr("celsius") * 9.0 / 5.0 + 32

    A = Class(
        name="A",
        base_class=OBJECT,
        fields={"fahrenheit": FahrenheitGetter()},
        metaclass=TYPE,
    )
    obj = Instance(A)
    obj.write_attr("celsius", 30)
    assert obj.read_attr("fahrenheit") == 86
