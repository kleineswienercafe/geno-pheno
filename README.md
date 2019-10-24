# Geno Pheno - DatenWolf™

This repository turns St. Anna's geno-pheno dataset into beautiful plots.

## Setup
create a virtual env
```cmd
$ pip install virtualenv
$ cd python
$ virtualenv env
```

## VSCode with virtual env
- `CTRL+SHIFT+P` type `python: select interpreter`
- Select the local environment (starting with `./env/...`)

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
python geno-pheno.py --file "./data/MM_SS_IMZ Studie_Liste 210319_excluded_050719 Studie 0-2.txt"
```

![mascot](https://en.wikipedia.org/wiki/Tweety#/media/File:Tweety.svg)