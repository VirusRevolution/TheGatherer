class DotDict(dict):
    """A dict subclass that provides dot.notation access to dictionary attributes.

    This allows you to access dictionary values using attribute-style syntax
    (obj.key) in addition to the traditional bracket syntax (obj["key"]).

    Nested dictionaries are automatically wrapped in DotDict instances when
    accessed via dot notation.

    Examples:
        >>> from Backend.model.dotdict import DotDict
        >>>
        >>> data = DotDict({"name": "Alice", "age": 30, "city": "Berlin"})
        >>> data.name
        'Alice'
        >>> data["age"]
        30
        >>>
        >>> # Setting and deleting values
        >>> data.country = "Germany"
        >>> del data.age
        >>>
        >>> # Nested dictionary access
        >>> config = DotDict({
        ...     "database": {
        ...         "host": "localhost",
        ...         "port": 5432,
        ...         "credentials": {
        ...             "username": "admin",
        ...             "password": "secret"
        ...         }
        ...     }
        ... })
        >>> config.database.host
        'localhost'
        >>> config.database.credentials.username
        'admin'
        >>> type(config.database)  # Nested dicts are also DotDict instances
        <class 'Backend.model.dotdict.DotDict'>
        >>>
        >>> # Standard dict methods still work
        >>> len(data)
        3
        >>> data.keys()
        dict_keys(['name', 'city', 'country'])

    Note:
        - If a key shares a name with a built-in dict method (e.g. "keys",
          "get", "items"), use bracket notation to access it.
        - Accessing a missing key via dot notation returns None, since it
          delegates to dict.get().
        - Bracket access on nested values returns raw dicts; only dot
          access wraps them in DotDict.
    """
    def __getattr__(*args):
        """Return the value for a given key using dot notation.

        If the value is itself a dict, it is wrapped in a DotDict instance
        for chained dot access. Returns None if the key does not exist.

        Examples:
            >>> d = DotDict({"user": {"name": "Bob"}})
            >>> d.user.name
            'Bob'
            >>> d.missing  # Missing keys return None, not KeyError
        """
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val


    __setattr__ = dict.__setitem__
    """Enable attribute-style assignment (obj.key = value).

    Examples:
        >>> d = DotDict()
        >>> d.name = "Alice"
        >>> d["name"]
        'Alice'
    """


    __delattr__ = dict.__delitem__
    """Enable attribute-style deletion (del obj.key).

    Examples:
        >>> d = DotDict({"name": "Alice", "age": 30})
        >>> del d.age
        >>> "age" in d
        False
    """