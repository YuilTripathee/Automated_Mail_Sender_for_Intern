# Learnings by this project

## Pointer implementation

### Necessity

Pointer seem to be necessary in this project so that a variable declared and assigned in memory block (especially the ones with large volume of data) will remain reusable that helps in memory optimization.

But, the feature was not implemented by Python developers since they would like to see their python code neater and easy to read, and the feature was yet low level since low level features for python can be extended by C which makes re-implementation of fundamental, less commonly used and counter intuitive (somehow troublesome for beginners) is no more necessary.

### Remedy

1. Use C routine within the python script.
2. Use `cast` function; this way, you can get memory reference (but can't run along different scripts).  
3. Import the **script** this time, don't try the data. So that you are able to run code from other file, remain in a program and keep accessing the data from the same memory reference.
4. Best and most out of the box approach: **Use database systems** no hastle of maintaining data in either file system or in memory.

Here's an example using `cast` function:

```py
>>> import ctypes
>>> x = (ctypes.c_ulong*5)()
>>> x
<__main__.c_ulong_Array_5 object at 0x00C2DB20>
>>> ctypes.cast(x, ctypes.POINTER(ctypes.c_ulong))
<__main__.LP_c_ulong object at 0x0119FD00>
>>>
```

## How can I ignore files that have already been committed to the repo?

Git can only ignore files that are untracked - files that haven't been committed to the repository, yet. That's why, when you create a new repository, you should also create a .gitignore file with all the file patterns you want to ignore.

However, of course, not everything goes perfect... and files slip through that you later would like to see ignored.

### Solution

Prerequirements

1. Make sure your .gitignore file is up-to-date and contains all the correct patterns you want to ignore.
2. Commit or stash any outstanding local changes you might have. Your working copy should be clean before you continue.

In three steps, you can clean up your repository and make sure your ignored items are indeed ignored:

```sh
git rm -r --cached .
git add .
git commit -m "Clean up ignored files"
```
