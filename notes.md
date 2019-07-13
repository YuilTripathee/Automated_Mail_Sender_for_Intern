# Learnings by this project

## Pointer implementation (since not supported by Python)

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

## How to ignore files (remove from the repository) that have already been committed to the repo

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

## Autopilot using cron job

Cron is a task scheduler for UNIX-like systems which allow running **only background** process is a specific timed schedule. This can be implemented in personal computers, servers and cloud machines.

### Our solution : for Linux systems (hope it may work for Macs)

Here's the solution from GitHub by `@pa4080`. This allows starting up GUI applications using cron jobs.

The link: <https://github.com/pa4080/cron-gui-launcher>

> **Warning:** Its better to to things on hand than leaving on autopilot so that you won't get messed up sending wrong content. Better to use a reminder.

## Graphical User Interface (GUI) solution in Python

In most of the cases, we prefer using Graphical User Interfaces in our software due to its advantages although this system is less preferable to self operating tasks (without need of physical user) such as backend or bot.

For this, we have mainly two reasonable soulutions to implement GUI bindings.

### Heavy apps in client side (Adobe Softwares, AutoCADs)

We prefer using PySide or PyQt5, which is Python binding for Qt library to create native modern applications in real time.

### Very lightweight apps in client side (Small utility features)

For advanced users, use of terminal may not bother at all. But, still if GUI solutions arises to be necessary, we prefer using Tkinter; but for nowadays reliable solution could be using Electron desktop app. This is a JavaScript based implement allowing cross platform compilation between Windows, macOS and Linux systems (most of them may be compatible to all distros).

Since electron heavily relies on node.js runtime environment, there's a node module called `python-shell` that allows running python scipts within the installation region.

This might come handy for that purpose: <https://www.youtube.com/watch?v=CJi6hDOIxR0>

### Modern apps (uses RESTful APIs, Automation, Beautiful Design like Slack, Visual Studio Code)

Electron will be the most suitable for this application. Since heavy python usage is in demand of the project, running lightweight RESTful solution within the localhost (maybe using `Flask`) and the electron based client software can communicate using some interfaces (here API looks the most viable one).

This might come handy for that purpose: <https://www.youtube.com/watch?v=627VBkAhKTc>

## Make your Python project compatible to cross platform (as many as possible)

To make the python almost compatible for almost all existing platform, we can get it clear by the following steps:

1. Firstly, let's make the code completely executable in linux (I mean Ubuntu especially), since most of the machines, servers and clouds are at our first priority.

2. Then, we have to make sure the code works on mac machine and finally check in Windows machine.

Here are the important points to consider while enchancing cross platform support:

* Make sure you are using SHELL codes as less as possible since different machines have different types of shell and your project may not work as you desire to function.

* If you must use SHELL, use those that are compatible with most of the systems (example include `cd`, `mv`).

* Consider for hardware target you wish your code is expected to work, range include from fairly multipurpose microcontrollers to cloud clusters up to supercomputers. The consideration include multithreading, multiprocessing, using clusters, GPU utilization and many more.

* If it is still hard to completely make python based software compatible with all target platforms, branch your project repository. Make sure your changes within the branches created will be for cross platform support only, not for implementing program logic. Version control sytem can be handy enough to bring changes on main system logic (can be managed when merging branches), keeping cross platform support unchanged.

## Storing data in JSON gets larger over time and become memory intensive (for no vital reasons)

When it comes to storing data, JSON is much handy and readable form and is supported in majority of codebases. But for data intensive application where data grows in time, the time when JSON data reaches higher up to being bottleneck for smooth running of the program (either API or bot), optimization much be applied for healthier operation of the program desired.

### Optimization

The situation has been arised by growth of JSON data. The following remedies seems helpful enough:

1. **For large solution**, it is understood that now it is time to use database systems in your
project.

2. **For small solution**, where data volume is much smaller and situation is still in control and you desire to maintain scalability of the project, using CSV *(Comma Separated Values)* or DSV *(Delimeter Separated Values)* and appending data (rather than loading whole file into memory and rewriting) will save a lot of time and resource. For this, you've to optimize your existing JSON data into almost relational paradigm of data storage and manipulation (i.e. in tables).
