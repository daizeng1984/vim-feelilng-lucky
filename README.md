## Introduction
I feel I need a quick keyword linking tools in Vim so that I could keep writing while providing reflink. But I'm too lazy to grab link by myself and I trust Google most of the time. Therefore, this plugin is written to feed my need! It just does the job for me.

## Install
```
Plug 'daizeng1984/vim-feeling-lucky', {'do': 'pip3 install --upgrade google-api-python-client' }
```
As all Python remote plugins, after you `PlugInstall`, you need to run `:UpdateRemotePlugins`.

## How
Put your cursor on the word and make command `:FeelingLuckyReflink` and you're done.

```
Jekyll --> [Jekyll](https://jekyllrb.com/)
```

# TODO
