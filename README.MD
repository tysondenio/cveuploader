# Overview
A simple CLI program to manage upload a CSV file of CVE vulnerabilities to Clubhouse

# Authentication
This tool requires a Clubhouse API token in order to create the new stories.  An API token may be retrieved from https://app.clubhouse.io/onnahq/settings/account/api-tokens.
Once aquired the token may either be passed in as an environemnt variable named `CLUBHOUSE TOKEN` or via a .env file.

Environment variable
```
CLUBHOUSE_TOKEN=token cveuploader ...
```

Environment File
```
// local.env //
CLUBHOUSE_TOKEN=token
```
```
cveuploader --env-file ./env.local ...
```

# Usage
```
cveuploader --env-file [path] upload-csv [csv-path] [epic id] [project id] -n [name field] -d [description field]
```

See `cveuploader upload-csv --help` for all options

# Helpers
List all projects
```
cveuploader --env-file [path] list-projects
```

List all epics
```
cveuploader --env-file [path] list-epics
```
