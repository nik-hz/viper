class Scope:
    """
    Keeps track of variables in the current scope.
    Inherits variables from the parent scope when cloned.
    Allows redefinition of variables, which overrides parent scope definitions.
    """

    def __init__(self, parent=None):
        """
        Initialize a new scope.
        :param parent: The parent scope (optional). If provided, this scope inherits variables from the parent.
        """
        self.variables = {}  # Dictionary to store variable names and their types
        self.parent = parent  # Reference to the parent scope
        self.function_return = None

    def define(self, name, var_type):
        """
        Define a new variable or overwrite an existing variable in the current scope.
        :param name: Name of the variable
        :param var_type: Type of the variable
        """
        self.variables[name] = var_type

    def define_func_val(self, name, var_type):
        self.function_return = var_type

    def lookup(self, name):
        """
        Look up the type of a variable.
        Searches the current scope first, then parent scopes if necessary.
        :param name: Name of the variable
        :return: The type of the variable, or None if it is not defined.
        """
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            return None

    def clone(self):
        """
        Create a new child scope that inherits from the current scope.
        :return: A new Scope instance with the current scope as its parent.
        """
        return Scope(parent=self)

    def __repr__(self):
        parent_info = f", parent={repr(self.parent)}" if self.parent else ""
        return f"<Scope variables={self.variables}{parent_info}>"
