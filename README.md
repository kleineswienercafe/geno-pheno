# Geno Pheno - DatenWolf™

This repository turns St. Anna's geno-pheno dataset into beautiful plots.

## Setup
create a virtual env
```cmd
$ pip install virtualenv
$ cd THIS_REPOSITORY
$ virtualenv env
```

## VSCode with virtual env
- `CTRL+SHIFT+P` type `python: select interpreter`
- Select the local environment (starting with `./env/...`)

Voilà, you're good to go:
```
python geno-pheno.py --file "./data/MM_SS_IMZ Studie_Liste 210319_excluded_050719 Studie 0-2.txt"
```

## Export excel files

we have now scripted the conversion from excel files (because there were more updates than expected). You can turn the excel file into a valid csv using:
````cmd
python convert-excel.py --file ./data/Geno_Pheno AML 291019.xlsx
````

### Manually export excel files
- In Excel choose `Save as > Unicode Text (.txt)`
- Open exported file in Notepad++
- Replace: `;` with `,`
- Replace: `\t` with `;`
- add `#` at the beginning of the first line
- set `Encoding` to `Encode in UTF-8`

## Launch configuration
here is a ``launch.json`` configuration that renders umaps for AML 0-2:
````json
{
    "name": "AML 0-2",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/geno-pheno.py",
    "args": [
        "--file",
        "${workspaceFolder}/data/Geno_Pheno AML 231019 Studie 0-2.txt",
        "--plot-mode", "umap"
    ]
},
````
I also like the batch computation:
````json
{
    "name": "Batch AML",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/geno-pheno.py",
    "args": [
        "--aml"
    ]

},
````

![mascot](https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Tweety.svg/133px-Tweety.svg.png)
