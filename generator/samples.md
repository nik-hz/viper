# Viper to Python sample pairs
Our code generator should convert the AST into correct python code. We check for compile time type consistency in the Viper code and then turn it to python. 
We only support arithmetic and boolean operations NoneType function and do not support print, return, and function calls in this version.

### 1) 
**Viper input**
``` python 
int :: num = 1; 
```

**Python output**
```python 
num = 1
assert isinstance(num, int)
```

### 2) 
**Viper input**
``` python 
NoneType :: def print_one():{ 
    int :: num = 1; 
};
```

**Python output**
```python 
def print_one():
    num = 1
    assert isinstance(num, int)
```
### 3) 
**Viper input**
``` python 
NoneType :: def calculation1():{ 
    float :: num = 1.5; 
    float :: num
    return num;
};

float :: output = return_float();
```

**Python output**
```python 
def return_float(){
    num = 1.5
    assert isinstance(num, float)
    return num
}

output = return_float()
assert isinstance(output, float)
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
};
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
for i in y: { print(i); };
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