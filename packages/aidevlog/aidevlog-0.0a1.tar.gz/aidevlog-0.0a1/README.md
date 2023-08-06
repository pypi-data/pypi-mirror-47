![AIDevLog](https://repository-images.githubusercontent.com/191505403/6a63bc80-8d1d-11e9-8bd7-44aaa16ccdb9)

[![Build Status](https://travis-ci.org/iOSDevLog/aidevlog.svg?branch=master)](https://travis-ci.org/iOSDevLog/aidevlog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aidevlog.svg)
![PyPI](https://img.shields.io/pypi/v/aidevlog.svg)
![PyPI - License](https://img.shields.io/pypi/l/aidevlog.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/aidevlog.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aidevlog.svg)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/iOSDevLog/aidevlog.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FiOSDevLog%2Faidevlog)

# templete

templete of AIDevLog

## 需要修改

`.travis.yml`

```sh
pip3 install travis-encrypt
travis-encrypt --deploy iosdevlog <PyPI> .travis.yml
```

[https://2019.iosdevlog.com/2019/06/05/travis/](https://2019.iosdevlog.com/2019/06/05/travis/])

## 代码规范

### .vscode/settings.json

```json
{
  "python.pythonPath": "/Users/iosdevlog/.Envs/aidevlog/bin/python",
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "yapf",
  "python.linting.flake8Args": ["--max-line-length=248"],
  "python.linting.pylintEnabled": false
}
```

- 字符串使用双引号： **""**

## 安装

```sh
pip install aidevlog
```

## 开发

### 本地开发

```sh
pip3 install -e .
```

### 测试

```sh
pytest
```

### 发布

```sh
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

### 生成CHANGELOG

```sh
npm install -g conventional-changelog-cli
./version.sh
```

## 联系方式

网站: [http://2019.iosdevlog.com/](https://2019.iosdevlog.com/)

微信公众号: AI 开发日志

![AIDevLog](https://2019.iosdevlog.com/uploads/AIDevLog.jpg)

## License

AIDevLog is released under the MIT license. See [LICENSE](LICENSE) for details.
