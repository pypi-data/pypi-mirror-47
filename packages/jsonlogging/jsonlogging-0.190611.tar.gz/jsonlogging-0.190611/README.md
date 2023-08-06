# jsonlogging

json 格式的日志。

### 安装

```
pip install jsonlogging
```

### 基本用法

```python
from jsonlogging import create_logger_simple

logger = create_logger_simple()
logger.setLevel("INFO")
```

#### 示例1

```python
logger.info({"name": "小明", "age": 11, "logTag": "TestTag"})
```

输出日志 (格式化后):

```json
{
    "logTime":"2019-05-23 17:38:04",
    "logName":"root",
    "logLevel":"INFO",
    "logPath":"/Users/myp/code/py36/0523/main.py",
    "logFile":"main.py",
    "logModule":"main",
    "logLine":12,
    "logFunc":"<module>",
    "logTag":"TestTag",
    "logIp":"spiderman-OptiPlex-3020",
    "ext_info":"",
    "name":"小明",
    "age":11
}
```

⚠️注意：推荐每条日志都带上 `logTag` 键，该键几乎是让使用者在浩如烟海的日志中找到所要日志的唯一线索；

#### 示例2

```
logger.info("执行成功")
```

输出日志 (格式化后):

```json
{
    "logTime":"2019-05-23 17:41:32",
    "logName":"root",
    "logLevel":"INFO",
    "logPath":"/Users/myp/code/py36/0523/main.py",
    "logFile":"main.py",
    "logModule":"main",
    "logLine":13,
    "logFunc":"<module>",
    "logTag":"",
    "logIp":"spiderman-OptiPlex-3020",
    "ext_info":"",
    "logMsg":"执行成功"
}
```

### logger 类型

目前支持如下类型

| 获得方式             | 说明                         |
| -------------------- | ---------------------------- |
| create_logger_simple | 输出 日志 到控制台           |
| create_logger_tofile | 输出 日志 到文件             |
| create_logger_daily  | 输出 日志 到文件，且按天分割 |

### 上传至 PyPI 步骤

1. 更新 `setup.py` 中的 `version`

2. cd 到 setup.py 所在目录下，执行：

```
python3 setup.py sdist bdist_wheel
```

3. 推送最新包到 PyPi 官方，执行：

```
twine upload dist/*
```

4. 登录 <https://pypi.org/manage/projects/>，查看新上传的包，在本地测试新包没问题后删除旧的版本（因为 pip install jsonlogging 时仍会优先安装 旧版本）。