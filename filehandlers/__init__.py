"""The main module."""

import io
import os
import enum
from json import loads
from typing import Optional, Dict, Any, List


class AbstractFile:
    """A file in instance form."""

    def __init__(self, name: str):
        """
        Creates the class.

        Args:
            name: The file name.

        Returns:
            Nothing.
        """
        self.name = name

    def __str__(self) -> str:
        """
        Override of `str()` and `__str__`.

        Returns:
            The name of the file.
        """
        return self.name

    def __abs__(self) -> str:
        """
        Override of `abs()` and `__abs__`.

        Provides the absolute path to the file.

        Returns:
            The absolute path to the file.
        """
        return os.path.abspath(self.name)

    def wrap(self):
        """
        Wrap the file in a `TextIOWrapper` (part of the Python standard library,
        return type of `open()`). The wrapper will be in read mode.

        Returns:
            The wrapper.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
            FileNotFoundError: If the file doesn't exist.
        """
        return open(str(self), mode="r")

    def touch(self):
        """
        Create the file if it doesn't already exist.

        In case you are wondering, the name for this function comes from the Unix command
        `touch`, which creates a new file with the name as a parameter.

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        open(str(self), mode="a").close()

    def exists(self, touch_if_false: Optional[bool] = False) -> bool:
        """
        Get if this file exists or not (boolean value).

        Returns:
            If the file exists.

        Arguments:
            touch_if_false: If the file should be created if it doesn't exist.

        Raises:
            PermissionError: If you don't have the required permissions to access the file.
        """
        e = False
        if os.path.exists(self.name):
            e = True
            if touch_if_false:
                self.touch()
        return e


class FileManipulator:
    """Class used for managing an assigned file."""

    cache: List[str]
    _linked_abstractfile: AbstractFile

    def __init__(self, abstract_file: AbstractFile):
        """
        Create class instance.

        Arguments:
            abstract_file: The AbstractFile instance.

        Returns:
            Nothing.

        Raises:
            TypeError: If the argument isn't an AbstractFile.
        """
        self.cache = []
        if type(abstract_file) == AbstractFile:
            self._linked_abstractfile = abstract_file
        else:
            raise TypeError("Wrong type! Please pass AbstractFile or string")
        self.refresh()

    def get_file(self) -> AbstractFile:
        """
        Get the AbstractFile instance.

        Returns:
            The AbstractFile instance.
        """
        return self._linked_abstractfile

    def get_file_name(self) -> str:
        """
        Get the file's name.

        Returns:
            The file's name.
        """
        return str(self.get_file())

    def refresh(self, slim: Optional[bool] = False):
        """
        Update the cache.

        Arguments:
            slim: If empty lines should be removed.

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        if not self.get_file().exists():
            # file doesn't exist, exit early
            return

        with open(self.get_file_name(), mode="r") as fh:
            self.cache = fh.readlines()
            # strip newlines
            for h, g in enumerate(self.cache):
                if slim and self.cache[h] == "":
                    self.cache.pop(h)
                else:
                    self.cache[h] = self.cache[h].replace("\n", "")
            fh.close()

    def get_cache(self) -> List[str]:
        """
        Get the cache.

        The cache will be a list of the file's lines at the time of the
        last refresh.

        Refreshes are called when this class is created,
        or when manually triggered by [refresh].

        Returns:
            The cache.
        """
        return self.cache

    def write_to_file(self, string: str):
        """
        Write to the file.

        !!! warning "Types"
            Please ensure that what you are writing to the file
            is a string.

        Arguments:
            string: What to write to the file.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
            TypeError: If you pass an unsupported type to be written.
            FileNotFoundError: If the file doesn't exist.

        Returns:
            Nothing.
        """
        e = open(str(self.get_file()), mode="w")
        e.write(string)
        e.close()

    def wrap_file(self) -> io.TextIOWrapper:
        """
        Shortcut for `self.get_file().wrap()`.

        Returns:
            The wrapped file.
        """
        return self._linked_abstractfile.wrap()

    def clear_file(self):
        """
        Clear the file.

        Warning: You will not be able to recover the old contents!

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
            FileNotFoundError: If the file doesn't exist.
        """
        open(str(self.get_file()), mode="w").close()

    def get_file_contents_singlestring(self) -> str:
        """
        Get the file's contents, but as one multi-line string.

        !!! warning
            This function does not use the cache.

        Returns:
            The file's contents.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
            FileNotFoundError: If the file doesn't exist.
        """
        o = open(str(self.get_file()), mode="r")
        string = o.read()
        o.close()
        return string

    def delete(self):
        """
        Delete the file if it exists.

        Returns:
            If it got deleted or not (can be ignored by just calling the method).

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        if self.get_file().exists():
            os.remove(str(self.get_file()))
            return True
        return False

    def load_from_json(self) -> Dict[str, Any]:
        """
        Loads the file, and returns the dictionary containing the data.

        Returns:
            The dictionary with the data.

        Raises:
            JSONDecodeError: If it isn't valid JSON.
            PermissionError: If you don't have needed permission to access the file.
            FileNotFoundError: If the file doesn't exist.
        """
        return loads(self.get_file_contents_singlestring())


class OpenModes(enum.Enum):
    """
    Enum for the different options you can pass to the
    keyword argument `mode` in Python's `open` function.

    It can be used like this:

    ```python
    from filehandlers import OpenModes
    open("myfile.txt", mode=OpenModes.READ.value)
    ```

    This can help so you don't need to remember all the different
    `mode` options.

    !!! danger "Using `WRITE`"
        For the `write` option, the file will be cleared and
        then written to. To avoid this, use `append` instead!

    !!! tip "Binary mode vs Text mode"
        Text mode should be used when writing text files
        (whether using plain text or a text-based format like TXT),
        while binary mode must be used when writing non-text files like images.
    """

    """Read only access to the file."""
    READ = "r"
    """Read only access to the file (binary enabled)."""
    READ_BINARY = "rb"
    """Write only access to the file - ***see warning above***."""
    WRITE = "w"
    """Write only access to the file - ***see warning above*** (binary enabled)."""
    WRITE_BINARY = "wb"
    """Clear the file."""
    CLEAR = WRITE
    """Append to the end of the file (also gives read!)."""
    APPEND = "a"
    """Create the file - ***raises error if file exists***."""
    CREATE = "x"
    """Create the file and ready it to be written to."""
    CREATE_AND_WRITE = "w+"
    """The default option for the built-in `open` function."""
    TEXT = "t"
    """Open in binary mode."""
    BINARY = "b"
    """This will open a file for reading and writing (updating)."""
    UPDATING = "+"
