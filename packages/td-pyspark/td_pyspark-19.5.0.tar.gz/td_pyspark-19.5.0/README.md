td_pyspark
== 

Treasure Data extension of pyspark.


## Usage

```python
import td_pyspark
from pyspark.sql import SparkSession

spark = SparkSession\
    .builder\
    .appName("td-pyspark-app")\
    .getOrCreate()

td = td_pyspark.TDSparkContext(spark)

# Read the table data within -1d (yesterday) range as DataFrame
df = td.table("sample_datasets.www_access")\
    .within("-1d")\
    .df()
df.show()

# Submit a Presto query
q = td.presto("select 1")
q.show()
```

## For Developers

Running pyspark with td_pyspark:

```bash
$ ./bin/spark-submit --master "local[4]"  --driver-class-path td-spark-assemblyd.jar  --properties-file=td-spark.conf --py-files ~/work/git/td-spark/td_pyspark/td_pyspark/td_pyspark.py ~/work/git/td-spark/td_pyspark/td_pyspark/tests/test_pyspark.py
```

## How to publish

### Prerequisites 

[Twine](https://pypi.org/project/twine/) is a secure utility to publish the python package. It's commonly used to publish Python package to PyPI.
First you need to install the package in advance.

```bash
$ pip install twine
```

Having the configuration file for PyPI credential may be useful.

```
$ cat << 'EOF' > ~/.pypirc 
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://upload.pypi.org/legacy/
username=<your_username>
password=<your_password>

[pypitest]
repository=https://test.pypi.org/legacy/
username=<your_username>
password=<your_password>
EOF
```

### Build Package

Build the package in the raw source code and wheel format.

```
$ python setup.py sdist bdist_wheel
```

### Publish Package

Upload the package to the test repository first.

```
$ twine upload \
  --repository pypitest \
  dist/*
```

If you do not find anything wrong in the test repository, then it's time to publish the package.

```
$ twine upload \
  --repository pypi \
  dist/*
```
