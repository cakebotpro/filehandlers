# Changelog

## v3.0.0

```diff
+ Added tests and code coverage
+ Added abs() override to AbstractFile
* Fixed certain resource leaks
```

## v2.12.1

```diff
+ Add autodoc-working docstrings to OpenModes
```

## v2.12.0

```diff
+ Optimized some internal logic.
```

## v2.11.1

```diff
* Continuation of v2.11.0 work
```

## v2.11.0

```diff
* Refactored documentation
```

## v2.10.0

```diff
+ Added FileManipulator.load_from_json method
Lots of documentation fixes
```

## v2.9.0

```diff
+ Added FileManipulator.delete method
- Removed AbstractFile.change_file_name
```

## v2.8.0

```diff
* We are now using Semver
+ Added AbstractFile.exists method
```

## v2.7

```diff
+ Added FileManipulator.get_file_contents_singlestring method
```

## v2.6

```diff
+ Added contributing guidelines.
+ Added OpenModes enum.
* Made files that remained open close themselves (prevents memory leaks).
+ Added FileManipulator.write_to_file method.
```

## v2.5

```diff
* Refactored documentation.
- Removed AbstractFile.__abs__() - It wasn't needed.
+ Added doreturn parameter to AbstractFile.wrap() - Just keep it as True, it is for other code inside the package.
+ Added AbstractFile.touch() method.
```

## v2.4

```diff
+ Added keywords to package
+ Added flake8 task and package builder task for every commit
* Enhanced documentation
```

## v2.3

```diff
* Fixed long description
```

## v2.2

```diff
+ Added new documentation, refactored existing ones.
+ Added code of conduct
+ Added proper license
+ Added AbstractFile.change_file_name()
* Changed result of abs(AbstractFile) - now returns instance of the class
+ Added project URLs
```

## v2.1

```diff
* Fixed a bug where FileManipulator.clear_file() would raise an AttributeError
```

## v2.0

```diff
* Made sure all classes inherit object
* Changed __str__() calls to use str() instead
* Changed FileHandler's name to FileManipulator
+ Added functionality to translate strings to AbstractFile (as a parameter to FileManipulator)
+ Added FileManipulator.clear_file() method to clear a AbstractFile's contents
* Updated some values in setup.py
```
