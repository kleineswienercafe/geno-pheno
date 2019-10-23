# Geno Pheno

python scripts that analyze the geno-pheno dataset.

## Setup
create a virtual env
```cmd
$ pip install virtualenv
$ cd python
$ virtualenv env
```

## VSCode with virtual env
`CTRL+SHIFT+P` type workspace settings, then add:
````json
"settings": {
    // python setup
    "python.pythonPath": "env\\Scripts\\python.exe",
    "python.venvPath": "${workspaceRoot}/env/"
}
````
Voilà, you're good to go

## Export excel files
- In Excel choose `Save as > Unicode Text (.txt)`
- Open exported file in Notepad++
- Replace: `;` with `,`
- Replace: `\t` with `;`
- add `#` at the beginning of the first line
- set `Encoding` to `Encode in UTF-8`

## Run Analysis

```
geno-pheno.py --file "C:/nextcloud/projects/FlowMe/geno-pheno/MM_SS_IMZ Studie_Liste 210319_excluded_040719.txt"
```