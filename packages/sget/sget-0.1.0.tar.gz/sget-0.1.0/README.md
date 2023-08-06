# SGET

[![asciicast](https://asciinema.org/a/iNJJ60m6C21RM0DlGXlgz4EAM.png)](https://asciinema.org/a/iNJJ60m6C21RM0DlGXlgz4EAM?speed=3)
## INSTALL WITH AND PIP
```bash
pip install sget
```


## INSTALL WITH GIT AND PIP
```bash
git clone git@github.com:ONordander/sget.git
cd sget
pip install .
```

## QUICKSTART
```bash
# Add a snippet
sget add "grep -r sget"

# Add a snippet template with <$>, will prompt for a value at <$>.
sget add "scp sget@192.168.0.10:<$> ."

# Add many snippets from a .toml file
curl https://raw.githubusercontent.com/ONordander/snippets/master/unix.toml -o unix.toml
sget install unix.toml

# Run a snippet from search prompt
sget

# Run a snippet by name
sget run grep_sget

# Remove snippet by name (leaving the name blank will start a search prompt)
sget rm grep_sget

# List all snippets (with optional group)
sget list -g unix

# Clear all snippets
sget clear
```

## Vim integration
```bash
nnoremap <expr> <Leader>s ":!sget cp<Space>" . input("Snippet name (leave blank to search): ") . "<CR>"
```
