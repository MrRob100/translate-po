# Translate .PO: Translate .po files to create language packs for OJS

A python cli tool to translate existing .po locale files to create localised strings for any language for OJS

## Requirements

- Python 3

## Installation

1. Clone the repository

2. Install dependencies

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

Translate a .po file into specific locale. Creates the file /path/to/project/locale/pt_BR/locale.po:

```bash
./translate.py /path/to/project/locale/en_US/locale.po pt_BR 
```

Translate a .po file into a whole set of locales. Prompts the OJS version (3.3, 3.4 or 3.5) to be entered as the locale 
sets are different with the later versions having less country specific languages i.e `en` rather than `en_US`

```bash
./translate.py /path/to/project/locale/en_US/locale.po 
```