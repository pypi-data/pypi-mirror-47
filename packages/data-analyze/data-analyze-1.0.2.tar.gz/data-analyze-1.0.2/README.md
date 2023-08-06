# 概述
data analysis

# 一、rules 规则
系统会根据配置的规则，对原数据进行分析

## 数据结构
```json
{
  "type":"system",
  "rules":[
      {
          "id":1,
          "type":"log",
          "condition":"xxxx" 
      },
      {
          "id":2,
          "type":"assert",
          "condition":"xxxx" 
      },
      {
          "id":3,
          "type":"data",
          "condition":"xxxx"
      }
  ],
  "relation":"id1|id2|id3",
  "result":{ 
      "type":"system",
      "module":"bluetooth",
      "desc":"蓝牙没打开"
  },
  "weights":1
```

### type 规则类型
支持 coredump、system、test
1. coredump 数据分析
2. system 系统级别日志分析
3. test 测试业务数据分析
### rules 规则 
1. id 唯一标识
2. type 匹配内容类型，log-行日志、assert-断言、data-直接数据
3. condition 匹配条件，支持正则表达式，可配置多个条件
### relation 匹配条件关系
多个条件id匹配关系，支持 与&、或|、非not、优先级()
### result 匹配结果
1. type 结果类型：cloud云端问题，system系统端问题
2. module 问题模块：bluetooth蓝牙模块，alarm闹钟模块等。。
3. desc 问题描述

### weights 权重
同时匹配多个规则时，权重越大概率越高

### 打包上传
1.pip install twine 
2.python setup.py sdist bdist_wheel  --打包
3.twine upload --repository-url https://upload.pypi.org/legacy/ dist/*   --上传 