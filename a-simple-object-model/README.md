# A Simple Object Model
> by Carl Friedrich Bolz

http://aosabook.org/en/500L/a-simple-object-model.html

- 키워드
  - Metaclass in OOP
  - Descriptor protocol and description in Python
  - The relation of `type` and `object` in Python
  - Bound method
  - maps
  - JIT Compiler

## Introduction
- 객체 지향 언어들의 공통점
	- 객체가 존재한다.
	- 상속 메커니즘이 존재한다.
- 클래스는 모든 언어가 직접적으로 제공하는 기능은 아니다.
	- Self나 JavaScript와 같은 프로토타입 베이스 언어에서 클래스 개념은 존재하지 않고, 대신에 객체들은 서로 직접적으로 상속받는다.
- 아주 단순한 객체 모델을 구현해본다.
	- 단순한 인스턴스와 클래스, 인스턴스에 대한 메서드 호출 기능...
	- -> Simula 67이나 Smalltalk과 같은 초기 OO 언어에서 성립된 "고전적인" 객체 지향 접근법
	- 이후에 모델을 점점 더 확장해나가고, 효율성을 개선해본다.
	- 최종적인 모델은 파이썬 객체 모델의 이상화된, 단순화된 버전이다.

## 1. Method-Based Model
- 우선, 스몰톡 객체 모델의 엄청 단순화된 버전으로 객체 모델을 구현해보겠다.
- 1970년대 개발됨
- 객체 지향 프로그래밍을 대중화시켰고 오늘날 프로그래밍 언어의 많은 기능들의 근간
- 스몰톡의 핵심 기조 "모든 것은 객체다."
	- 오늘날 사용되는 언어 중 가장 직접적인 후손은 Ruby다. C와 비슷한 문법을 가지면서 스몰톡의 객체 모델을 갖고 있다.
- 용어 정리
	- 인스턴스: 클래스가 아닌 한 객체
- 객체 모델을 구현하는 코드와 객체에 사용되는 메서드를 작성하는 코드를 명확하게 구분하지 않았다. 실제 시스템에서 이 둘은 서로 다른 프로그래밍 언어로 구현되는 경우가 많다.

- `Class`: 클래스
- `Instance`: 인스턴스
- 두 개의 특별한 클래스 인스턴스
  - `OBJECT`: 상속 계층에서 가장 베이스가 되는 클래스, 파이썬에서 `object`
  - `TYPE`: 모든 클래스의 타입, 파이썬에서 `type`
- `Class`와 `Instance`는 `Base`라는 베이스 클래스를 상속받아 공통 인터페이스를 구현한다.
- `Base` 클래스는 객체의 클래스와 객체의 필드 값을 담고 있는 딕셔너리를 저장한다.

- [?] Since classes are also a kind of object, they (indirectly) inherit from Base. Thus, the class needs to be an instance of another class: its metaclass.

- 상당히 복잡한 메타클래스 시스템을 갖춘 Smalltalk 모델 대신, 파이썬이 채택한 ObjVlisp에 소개된 모델을 사용하도록 하겠다.
- ObjVlisp 모델에서 `OBJECT`와 `TYPE`은 얽혀있다.
  - `OBJECT`는 모든 클래스의 베이스 클래스다. 즉, `OBJECT`는 베이스 클래스를 갖지 않는다.
  - `TYPE`은 `OBJECT`의 서브클래스다.
  - 기본적으로 모든 클래스는 `TYPE`의 인스턴스다.
  - `TYPE`과 `OBJECT` 모두 `TYPE`의 인스턴스다.
  - [?] 하지만, 프로그래머는 새로운 메타클래스를 만들기 위해 `TYPE`을 서브클래싱(상속)할 수 있다.

- 새로운 메타클래스를 만들기 위해 `TYPE`을 상속받는 것으로 충분하다. 하지만, 이 챕터에서 그런 식으로 안 하고 단순히 모든 클래스의 메타클래스로 `TYPE`을 사용할거다.
- [?] metaclass vs baseclass
- [?] 파이썬 다이어그램 궁금

  ![Figure 14.1 - Inheritance](http://aosabook.org/en/500L/objmodel-images/inheritance.png)

### `isinstance` Checking
- `obj` 객체가 `cls` 클래스의 인스턴스인지 확인하는 방법
  -  `cls`가 `obj` 클래스의 상위 클래스(superclass)인지 또는 클래스 자체인지 확인하면 된다.
- 어떤 클래스가 상위 클래스인지 확인하는 방법
  - 상위 클래스 체인(그 클래스 자체도 포함)에 존재하는지 확인하면 된다.
  - 클래스의 상위 클래스 체인은 그 클래스의 "method resolution order"라고 부른다.
  - 재귀적으로 쉽게 계산할 수 있다.

### Calling Methods
- 객체에 호출되니 메서드의 구현을 찾기 위해서는 그 객체 클래스의 MRO를 거슬러 올라가 찾아야 한다. MRO에 있는 클래스 중 하나의 딕셔너리에서 찾아진 첫번째 메서드가 호출된다.

## 2. Attribute-Based Model
- method-based model과 attribute-based model의 구분을 하겠다.
  - Smalltalk, Ruby, JavaScript와 Python, Lua의 차이 중 하나다.
- method-based model은 프로그램 실행의 기본 요소인 메서드 호출이 있다.
  ```python
      result = obj.f(arg1, arg2)
  ```
- attribute-based model은 메서드 호출을 두 단계로 쪼갠다. 1) attribute 조회, 2) 결과 호출
  ```python
      method = obj.f
	  result = method(arg1, arg2)
  ```

- 메서드 호출 방식이 다르다.
  - 1) 객체에서 메서드명의 속성 조회 -> 결과는 bound method: 해당 객체와 클래스에서 찾은 함수를 캡슐화
  - 2) bound method 호출

- bound method 구현: 속성을 딕셔너리에서 찾지 못하면 클래스에서 찾도록 코드를 수정해야 한다.
  - 클로저 사용해서 구현하면 된다.

## 3. Meta-Object Protocols
- 프로그램에서 직접 호출되는 normal 메서드와 더불어, 많은 동적 언어는 special 메서드를 지원한다.
  - 직접 호출되는게 아니라 객체 시스템에 의해 호출되는 메서드
- 파이썬에서는 `__xxx__`
  - 오버라이드 가능
  - Python's object model has [dozens of special methods](https://docs.python.org/2/reference/datamodel.html#special-method-names).
- Meta-object protocol
  - 스몰톡에서 도입

- 메타 훅을 추가하겠다.
  - 속성을 읽고 쓸 때 발생하는 일을 미세하게 조정하는데 사용한다.
  - `__getattr__` and `__setattr__`

### Customizing Reading and Writing and Attribute
- `__getattr__`: 조회하는 속성을 일반적인 방법으로(인스턴스 or 클래스에서) 찾을 수 없을 때 호출된다.
- `__setattr__`: 속성 값 셋팅할 때마다 호출된다. 

### Descriptor Protocol
- `__getattr__`와 `__setattr__`이 속성을 읽고 있는 객체에 대해 호출될 때, 디스크립터 프로토콜은 객체에서 속성을 가져온 결과에 대해 특수 메서드를 호출한다.
- -> 메서드를 객체에 바인딩하는 일반화 + 실제로 메서드를 객체에 바인딩하는 건 디스크립터 프로토콜을 사용해 수행된다.
- 파이썬에서의 유스케이스
  - `staticmethod`
  - `classmethod`
  - `property`

## 4. Instance Optimization
- maps
  - Self 언어의 VM에서 도입됨. 중요한 객체 모델 최적화 방법 중 하나.
  - PyPy, V8과 같은 모던 JS VM(여기서는 hidden classes라고 부름)에서 사용됨

- 모든 인스턴스들이 속성을 저장하기 위해 딕셔너리를 사용한다.
  - 같은 클래스의 인스턴스들은 같은 키를 가진 딕셔너리를 갖고 있다.
- 모든 인스턴스의 딕셔너리를 두 파트로 쪼갠다.
  - 1) 같은 속성명을 가진 모든 인스턴스 사이에 공유하는 keys(map)를 저장하는 부분
    - 그러면 인스턴스는 map에 대한 레퍼런스만 갖고 있고, 값은 list에 담아둘 수 있다. 
  - 2) 