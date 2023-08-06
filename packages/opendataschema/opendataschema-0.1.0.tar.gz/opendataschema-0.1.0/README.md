# Open Data Schema Python client

## Install

```bash
pip install opendataschema
```

## Usage

Note: the `schema.json` file can be given as a file path or an URL.

```bash
opendataschema schema.json list
opendataschema schema.json show
opendataschema schema.json show --name <schema_name>
opendataschema schema.json show --versions
```

## Python API

TODO
Example:

```python
tsc = SchemaCatalog("https://opendataschema.frama.io/catalog/schema-catalog.json")
for tsr in tsc.get_schema_references():
    if tsr.has_git_nature():
        version_list =
        for ver in tsr.get_git_versions():
            url = tsr.get_schema_url(version)
            ts = TableSchema(url)
            print(ts.get_properties())
    else:
        url = tsr.get_schema_url()
        ts = TableSchema(url)
        print(ts.get_properties())

```

