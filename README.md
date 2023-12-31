
# Test Automation repository for creating quick selenium based tests and to generate code for automation

This repo is the collection of automated UI tests mainly used to create quick automation tests and to expand on the code generation utility "Scripter" in the utils folder

##  Setup

Please note that these tests and this setup instruction has been written using Python 3.9.2
To ensure that you have the same experience please ensure that you are running the same version.


### Setup your virtual environment


```shell
python3 -m venv ./venv
```

### Activate your virtual environment

```shell
source venv/bin/activate
```

### Install Project Dependencies

please install the following dependencies
```shell
pip install --upgrade pip
pip install selenium
pip install webdriver-manager
pip install pytest
pip install lxml
pip install sqlalchemy
pip install pandas
```



## Executing Test Cases


To execute all tests you can run the following command
```shell
pytest
```

