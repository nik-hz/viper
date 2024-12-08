# Viper to Python sample pairs
Our code generator should convert the AST into correct python code. We check for compile time type consistency in the Viper code and then turn it to python. 

### 1) 
**Viper input**
``` python 
NoneType :: def say_hello_world():{ 
    string :: text = 'hello world'; 
    print(text);
    }
```

**Python output**
```python 
def say_hello_world(){
    text = 'hello world'
    assert isinstance(text, str)
    print(text)
}
```
### 2) 
**Viper input**
``` python 
str :: def say_hello_world():{ 
    string :: text = 'hello world'; 
    return text;
    }

output = say_hello_world()
```

**Python output**
```python 
def say_hello_world(){
    text = 'hello world'
    assert isinstance(text, str)
    return text
}

output = say_hello_world()
assert isinstance(output, str)
```

### 3) 
**Viper input**
``` python 
int :: def func(int :: a, int :: b):{ 
    assert isinstance(a, int)
    assert isinstance(b, int)
    int :: c = a + b; 
    assert isinstance(c, int)
    return c;
}
```

**Python output**
```python 
def func(a, b):{ 
    c = a + b; 
    return c;
}
```

### 4) 
**Viper input**
``` python 
int :: x_a = 10; 
list :: y = range(0,x_a); 
for i in y: { print(i); }
```
**Python output**
``` python 
x_a = 10
assert isinstance(x_a, int)
y = range(0,x_a) 
assert isinstance(y, list)
for i in y: 
    print(i)
```

### 5) 
**Viper input**
``` python 
NoneType :: def nthFib(int :: n):{
    int :: res = (((1+sqrt(5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5));
    print(res,'is',str(n)+'th fibonacci number');
};
nthFib(12);
```
**Python output**
``` python 
def nthFib(n){
    assert isinstance(n, int)
    res = (((1+sqrt(5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5));
    assert isinstance(res, int)
    print(res,'is',str(n)+'th fibonacci number')
}
nthFib(12)
```