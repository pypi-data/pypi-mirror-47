# Eloope
事件循环引擎, 主要功能:

    1. 异步执行, 解决io密集型任务
    2. 支持搭建多进程, 分布式运行
    3. 支持断点续爬
    4. 提供日志系统

目录:
- [安装](#安装)
- [使用](#使用)
    - [单进程](#单进程)
    - [多进程](#多进程)
    - [分布式](#分布式)
    - [命令式](#命令式)
    - [日志](#日志)
    - [setting](#setting)
- [API](#API)
    - [Engine](#Engine)
    - [Manager](#Manager)
- [下次更新内容](#下次更新内容)

## 安装
```
pip install eloope -upgrade
```

## 使用
- 首行导入 `eloope` 模块

### 单进程
```
from eloope import engine, get_current_engine, logger

def task(code):
    logger.info(f'{get_current_engine().name} --- {code}')

engine.add_tasks(fn=task, param_groups=[[code] for code in range(100)])
engine.run()
```
- 单进程 demo: [spider_dili.py](https://github.com/Czw96/Eloope/blob/master/demo/spider_dili.py)
- 通过 `get_current_engine` 函数获得当前运行engine

### 多进程
#### 开启服务
```
from eloope import run_server

run_server(load_file=None, dump_path='.', log_path=None, host='localhost', port=6991)
```
- load_file: 加载任务文件
- dump_path: 任务文件保存路径
- log_path: 日志保存路径, 为 `None` 时将不保存日志文件

#### 运行客户端
```
from eloope import Manager, get_current_engine, logger

def task(code):
    logger.info(f'{get_current_engine().name} --- {code}')

if __name__ == '__main__':
    # Manager 创建多进程
    manager = Manager(engine_names=['engine1', 'engine2'], host='localhost', port=6991)
    manager.add_tasks(fn=task, param_groups=[[code] for code in range(100)])
    manager.run()
```
- 多进程客户端需要在 `if __name__ == '__main__':` 语句中启动
- 多进程 demo: [multi_progress.py](https://github.com/Czw96/Eloope/blob/master/demo/multi_progress.py)

### 分布式
- 部署项目, 连接同一服务

### 命令式
```
>>> eloope <command> <args> -h <host> -p <port>
```
| command | 说明 |
|---------|:-----|
| stop | 停止向客户端发送任务 |
| start | 开始向客户端发送任务 |
| save | 保存当前服务器上的任务 |
| quit | 强制退出服务和所有客户端 |
| task_total | 任务总数量 |
| task_count | 任务当前数量 |
| start_time | 服务开始时间 |
| connect | 连接服务 |
| run_server <load_file> <dump_path> <log_path> | 启动服务 |
- `host` 默认值: 'localhost', `port` 默认值: 6991

### 日志
```
from eloope import logger

logger.info('hello world!')
logger.debug('hello world!')
logger.result('hello world!')
logger.warning('hello world!')
logger.error('hello world!')
logger.system('hello world!')
```
- 导入 `eloope` 模块将会屏蔽掉其他模块的日志系统

### setting
```
from eloope import setting

# 客户端运行中连接失败回调函数
# 参数: engine(Engine 实例), repeat_count(重复连接次数)
# 返回: True(重新连接), False(断开连接退出程序)
setting.connection_interrupt_callback = connection_interrupt_callback

setting.send_interval = 1  # 客户端连接服务器间隔
setting.log_path = None  # 本地日志保存路径

# 日志级别过滤
setting.log_filter = ('info', 'debug', 'result', 'warning', 'error', 'system')
```

## API
### Engine(name='engine', size=50)
- name: 名称标识
- size: 任务池大小

| Attribute | 说明 |
|-----------|:-----|
| name | 名称 |
| is_run | 运行状态 |
| task_count | 任务数量 |
| free_count | 任务池剩余空间 |
| task_pool | 任务池 |
| run() | 运行 |
| add_task(fn, *params) | 添加单个任务 |
| add_tasks(fn, param_groups) | 添加多个任务, 同一个函数不同参数 |

### Manager(engine_names, host='localhost', port=6991)
- engine_names: engine 名称标识列表
- host: 服务器地址
- post: 服务器端口

| Attribute | 说明 |
|-----------|:-----|
| create_engines(engine_names, size=50) | 创建多个 engine |
| add_task(fn, *params) | 添加单个任务 |
| add_tasks(fn, param_groups) | 添加多个任务, 同一个函数不同参数 |
| run() | 运行 |



## 下次更新内容
```
1. 添加 Task 类, 可以选择任务执行的优先级; 可以指定 enigne 执行任务; 添加任务执行失败回调函数
2. 重新设计日志系统
3. 添加 UI 控制面板
```
