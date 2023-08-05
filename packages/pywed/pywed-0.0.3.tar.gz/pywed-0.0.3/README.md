# WEather Database client

## Install

### Pypi

Requires the eccodes library
```bash
pip install pywed
```

## Develop

### Conda

```bash
conda create -n wed --file packages.txt
conda activate wed
```

### Pypi

Requires the eccodes library
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
import wed
import datetime

db = wed.Database()
dataset = db.open_dataset(wed.DataType.WIND)
t = datetime.datetime(2017, 5, 12, 20, 4)  # 12/05/2017 at 20:04
print(dataset.read(t, wed.Coordinate(12, 48)))
```


## Packaging

This package is built out of some very simple code that queries `d-ice` weather
database using `s3`. If the user does not have credentials to access it, this
package becomes useless. We can therefore release the package publicly

### Pypi

```bash
bash upload.sh
```
