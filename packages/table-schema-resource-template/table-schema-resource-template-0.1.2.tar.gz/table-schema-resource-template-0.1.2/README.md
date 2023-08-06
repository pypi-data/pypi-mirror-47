# Table Schema resource template

Generate an empty resource file template from a [Table Schema](https://frictionlessdata.io/specs/table-schema/) JSON file.

Supported output formats:

- Microsoft Excel XLSX

## Install

```bash
pip install table-schema-resource-template
```

## Usage

Table Schema JSON can be given as file or URL:

```bash
table-schema-resource-template --format xlsx schema.json template.xlsx
table-schema-resource-template --format xlsx https://git.opendatafrance.net/scdl/subventions/raw/master/schema.json template.xlsx
```
