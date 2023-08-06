# WEather Database client

## Install

### Conda

Requires the eccodes library
```bash
conda config --add channels https://conda.anaconda.org/t/D--8990a90f-fff0-45a4-8ceb-66f63faedcb9/d-ice
conda install pywed
```

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

### Conda

```bash
conda install conda-build anaconda-client  # optional
conda build pywed --output-folder conda-build
anaconda -t D--d373f51c-281d-4003-b206-2d2a205c7fb5 upload conda-build/linux-64/pywed*
```
