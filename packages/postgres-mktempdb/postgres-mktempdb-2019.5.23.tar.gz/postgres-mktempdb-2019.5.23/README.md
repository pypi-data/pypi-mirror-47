<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install postgres-mktempdb
```

#### Scripts usage
command|`usage`
-|-
`mktempdb` |`usage: mktempdb [OPTION]...`

#### Examples
```bash
$ mktempdb
tmp_LH8LqXy8UGlfMR8zfB3todrc4mwC9Sns
```

delete temp databases:
```bash
$ psql -At -c "SELECT datname FROM pg_database WHERE datname LIKE 'tmp_%'" | xargs -L 1 dropdb
```

delete temp databases created more than 5 minutes ago:
```bash
$ psql -At -c "SELECT datname FROM pg_database
WHERE datname LIKE 'tmp_%' AND (pg_stat_file('base/'||oid||'/PG_VERSION')).modification<now()+interval '5 minutes'" | xargs -L 1 dropdb
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>