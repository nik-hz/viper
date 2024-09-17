# Proposal for Viper programming language project for COMS 4115

## Team Member
- Angel Leyi Cui
- Nikolaus Holzer

### Work division
- Adding static types
- Adding brackets

### Weekly meeting
- Tuesday after class

## Introduction
The goal of *Viper* is to enhance Python by addressing two key issues that many developers from C and Java backgrounds encounter: dynamic typing and whitespace-based syntax. Our aim is to achieve for Python what TypeScript accomplishes for JavaScript. *Viper* will offer a Python-like experience, maintain compatibility with all Python libraries, but introduce static typing and a syntax structure based on brackets and semicolons.

We strive to ensure a smooth learning curve for experienced Python users. *Viper* retains Python's overall user-friendliness while incorporating features that are beneficial for larger-scale applications. To preserve Python's familiarity, *Viper* is designed as a superset of Python, meaning all valid Python code is also valid *Viper* code, facilitating seamless integration into existing projects.

## Motivation
The motivation behind *Viper* stems from addressing key limitations in Python that are often cited by developers coming from languages like C, C++, and Java—particularly dynamic typing and reliance on whitespace-based syntax. These limitations can create challenges when building large-scale or complex applications. *Viper* is designed to maintain the ease and flexibility of Python while introducing more structured syntax and static typing, making it a valuable tool for developers looking to scale their Python projects or work on more robust systems.

### Why *Viper* Will Be Useful

1. **Improved Error Detection**: One of the primary benefits of *Viper* is the introduction of static typing, which catches many errors at compile time rather than runtime. This is a significant advantage in large applications where runtime errors can be difficult to trace and costly to fix. By detecting type-related issues during development, *Viper* helps developers produce more reliable and maintainable code.

2. **Familiar Python Feel with Enhanced Structure**: *Viper* retains the familiar syntax, data types, and overall feel of Python, making it easy for experienced Python developers to adopt without a steep learning curve. The addition of brackets and semicolons introduces a clearer and more structured syntax that developers from C-like languages will find more intuitive and less error-prone, especially when dealing with nested structures.

3. **Seamless Integration with Python Libraries**: By maintaining compatibility with existing Python libraries, *Viper* allows developers to continue using their preferred libraries without sacrificing the advantages of static typing. This eliminates the need to rewrite or reformat code for library use, making *Viper* an attractive option for Python projects of any size.

### Why the Design Choices Make *Viper* Useful

1. **Static Typing with Python's Flexibility**: While static typing is not a feature in standard Python, it is crucial for reducing runtime errors in larger applications. However, many existing Python typing libraries and conventions, such as type hints, can feel cumbersome to use. *Viper* streamlines this by incorporating a more intuitive and concise static typing system, while still allowing the dynamic nature of Python when necessary. This flexibility makes *Viper* suitable for a wide range of projects, from small scripts to enterprise-level software.

2. **IDE Support for Write-Time Errors**: *Viper*’s static typing and structured syntax enable better integration with modern IDEs, offering features like autocompletion, linting, and immediate error feedback. This reduces debugging time and enhances the developer experience by catching potential issues during the development phase rather than at runtime. By providing write-time error detection, *Viper* ensures that code quality is improved from the start.

3. **Brackets and Semicolons for Consistency**: By introducing brackets and semicolons, *Viper* eliminates common whitespace-related issues in Python, such as accidental indentation errors or ambiguities in block definitions. This consistency is especially beneficial when working on collaborative or multi-developer projects, where code readability and maintainability are crucial. The familiar syntax also makes it easier for developers with experience in C-like languages to transition to *Viper*.

### Use Cases and Program Types for *Viper*

1. **Enterprise Applications**: *Viper* is ideal for large-scale enterprise applications that require a balance between Python’s flexibility and the structural advantages of statically typed languages. Its static typing and compile-time error checking will make it easier to build, maintain, and scale such applications.

2. **Systems Programming**: *Viper*’s ability to compile to Python, C, or even machine code directly makes it highly versatile for systems-level programming, where performance and low-level memory management are key concerns. Its structured syntax and static typing make it a strong alternative for developers familiar with systems programming languages like C or Rust.

3. **Data Science and Machine Learning**: Many Python-based data science and machine learning libraries could benefit from *Viper*’s static typing, allowing for better debugging and optimization. *Viper* provides the best of both worlds—Python’s powerful scientific libraries and the added safety and performance benefits of a statically typed language.

In summary, *Viper* combines the best aspects of Python with enhanced structure and type safety, making it particularly useful for developers who require a more robust and scalable language without sacrificing Python's ease of use.

## Creativity/Novelty
*Viper* introduces a novel approach to enhancing Python’s usability. While several languages have aimed to build on Python’s strengths, *Viper* is unique in its goal to serve as a direct superset of Python, combining the best elements of both dynamic and static typing without fundamentally changing the Python experience. This balance between familiarity and structure represents the core of *Viper*’s innovation.

### Novel Features

1. **Superset of Python with Full Compatibility**: While other languages like TypeScript have enhanced JavaScript by adding static typing, *Viper* is unique in that it is a full superset of Python, ensuring that all valid Python code is also valid *Viper* code. This is a novel concept in the Python ecosystem, as it allows developers to transition to *Viper* without the need for extensive rewriting of existing codebases. The ability to compile *Viper* code to Python, C, or machine code offers flexibility that few Python extensions provide.

2. **Seamless Integration with Python Libraries**: One of *Viper*’s most creative and unique features is the ability to use existing Python libraries seamlessly, even with the introduction of static typing. By allowing *Viper* to either dynamically fetch types from libraries at compile time or bypass type checks with a keyword, the language ensures that it remains highly flexible. This novel solution to working with Python’s dynamic nature sets *Viper* apart from other statically typed Python-like languages, which often require extensive manual type annotations or rewrite libraries for compatibility.

3. **Multiple Compilation Targets**: Few languages provide the ability to compile to Python, C, or machine code directly, and *Viper*’s support for these compilation targets is a novel feature. This flexibility allows *Viper* to cater to a wide range of use cases, from high-level scripting to low-level systems programming, making it a truly versatile language.

4. **Python-Friendly Static Typing**: While Python has introduced type hinting, the implementation remains optional and clunky for many developers. *Viper* innovates by fully embracing static typing while maintaining a Python-like experience. The novel design choice of adopting static typing without introducing new data types or syntax complexities keeps *Viper* simple yet powerful, making it an attractive option for developers who value type safety but don’t want to lose the flexibility of Python.

### Novelty in the Python Ecosystem
While Python is highly popular, its growth has revealed limitations in large-scale applications, especially around dynamic typing and debugging runtime errors. Other languages, such as Pyright (a static type checker for Python), and mypy (a type checker for Python) attempt to mitigate these issues but lack the full static typing and structured syntax that *Viper* provides. *Viper* distinguishes itself as the first language to fully embrace Python’s strengths while innovatively addressing its weaknesses, offering a novel and creative solution that appeals to both Python developers and those from more statically typed backgrounds.

## Language and compiler description
*Viper* is a superset of Python, meaning *Viper* projects can be compiled to Python code, similar to how TypeScript compiles to JavaScript. *Viper* retains Python’s data types while introducing new syntax and static typing, preserving the familiar feel of Python by not adding new types. This allows developers to easily transition existing Python projects into *Viper* without sacrificing compatibility or needing to rewrite code.

### Compilation Targets:
Our compiler will support compiling *Viper* code to multiple targets: Python, C, or machine code. The compilation process will allow *Viper* to be seamlessly integrated into a wide variety of software environments, whether developers are working with high-level scripts or low-level system programming. By providing multiple target languages, *Viper* ensures flexibility for developers who want to write efficient, statically-typed code while leveraging Python’s ecosystem.

### Type Handling for Python Libraries:
To ensure *Viper* users can continue utilizing their favorite Python libraries, we propose two possible approaches for handling types. The first option is to provide type declaration files for the libraries in use, similar to how TypeScript provides `.d.ts` files. These declaration files would allow *Viper* to verify the types of library functions without requiring the libraries themselves to be rewritten.

The second option is to enable the *Viper* compiler to dynamically fetch type information from libraries at compile-time, inferring and verifying types against the *Viper* code automatically. This approach would require the compiler to inspect the libraries’ internal structure and ensure compatibility.

Alternatively, we might introduce a special keyword in *Viper* that allows users to bypass type checking for specific library functions when static typing information is either unavailable or unnecessary. This would allow flexibility without sacrificing the benefits of strong typing elsewhere in the project.

### Optimizations:
The *Viper* compiler should also include optimization steps tailored to the target language. For Python, the focus will be on minimizing overhead and ensuring that the compiled code retains full interoperability with Python’s runtime. For C and machine code, more aggressive optimizations may be applied, such as memory management enhancements, loop unrolling, and function inlining, to improve performance in critical applications.

## Example simple program written in Viper
This example demonstrates a recursive function that calculates the factorial of a number in *Viper*. 

``` python
# very similar syntax with only minimal changes
def int factorial(int n) {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}

int n = 5;
print(f"factorial of {n} is {factorial(n)}")
```
