# Open Data Schema Python client

## Install

```bash
pip install opendataschema
```

## Usage

Note: the `schema_catalog.toml` file can be given as a file path or an URL.

```bash
opendataschema schema_catalog.toml list
opendataschema schema_catalog.toml show
opendataschema schema_catalog.toml show --name <schema_name>
opendataschema schema_catalog.toml show --versions
```

## Python API

Example:

```python
tsc = TableSchemaCatalog("https://git.opendatafrance.net/scdl/schema-catalog/raw/master/schema_catalog.toml")
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

- a `TableSchema` instance can contain multiple `TableSchemaReference`
- a `TableSchemaReference` can be a Git (GitLab, GitHub) reference or an url reference
  - in case of Git reference, multiple versions of tableschema can coexist
- a `TableSchema` is created from a schema.json URL. It provides info on the schema (spec and properties)
