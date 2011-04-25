li the workspace manager
========================

li is a script for managing sets of interesting files in codebases.

A workspace is defined in a text file in which the first line is a path. The
rest of the file is free-form plain text, but any filenames relative to the
first path can be followed by making use of vim's "gf" shortcut.

li can list your available workspaces, or it can open one. Opening a workspace
means creating a new tmux session with a vim session editing the workspace
file. From there new terminals can be spawned through tmux, and any file in the
workspace can be accessed easily through vim.

Usage
=====

Invoking li by itself will list the workspaces it knows about. A * next to a
workspace indicates that the workspace is already open (ie: there is a tmux
session for it already).

    % li
    > 1: refactor-something
    > 2: add-update-name-rpc
    > 3: li-the-workspace-manager
    % li 2
    <opens the workspace 'add-update-name-rpc'>

The nw shortcut can be used to create a new workspace with a set of files
already in it.

    % cd my-project
    % nw my-project src/*.py
    % li
    > 1: my-project
