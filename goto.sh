if [ -z $1 ] ; then
    if [ -e ~/.workspaces ] ; then
        ls -dl ~/.workspaces | sed 's/.*\///'
    else
        echo '(no current workspace)'
    fi
    ls -1d ~/.workspaces.*
else
    rm -f ~/.workspaces
    ln -s ~/.workspaces.$1 ~/.workspaces
fi
