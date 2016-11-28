Arista IPython Magics
=====================


IPython/Notebook Config
-----------------------

```bash
$ more jupyter_notebook_config.py | grep -v "^#" | grep -v "^$"
c.NotebookApp.ip = '*'

$ cat ipython_config.py | grep -v "^#" | grep -v "^$"
c.InteractiveShellApp.exec_lines = ['%autoreload 2']
c.InteractiveShellApp.extensions = ['autoreload'] #, 'shakedown.magics']
```
