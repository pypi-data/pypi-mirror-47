# **maths** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 数学模块集合
[![](https://img.shields.io/badge/个人网站-jtyoui-yellow.com.svg)][1]
[![](https://img.shields.io/badge/Python-3.7-green.svg)]()
[![](https://img.shields.io/badge/BlogWeb-Tyoui-bule.svg)][1]
[![](https://img.shields.io/badge/Email-jtyoui@qq.com-red.svg)]()
[![](https://img.shields.io/badge/数学-maths-black.svg)]()


### 安装
    pip install jtyoui


## 判断一个是否为质数
```python
from jtyoui.statistics.maths import is_prime
if __name__ == '__main__':
    print(is_prime(915453))
```

## 查询1-n的质数(查询1亿耗时5秒，内存4G，i5-8500CPU，联想笔记本)
```python
from jtyoui.statistics.maths import primes
if __name__ == '__main__':
    print(len(primes(1_0000_0000)))  # 时间5.5541136264801025秒
```

***
[1]: https://blog.jtyoui.com