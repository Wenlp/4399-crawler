## 4399爬虫项目

###### 输入：

​	种子URL  http://www.4399.com/flash/1.htm

###### 输出：

​	4399.xlsx(请根据自己的文件系统设置目标路径)

###### 工作内容：

1. 从种子页面解析游戏信息，存入自己的DataFrame。
2. 从当前页面解析url信息作为候选队列。
3. 对候选队列进行BFS(循环1.2.)，第一次到达队列容量后不再进行2.

###### 可变参数：

1. max_size = 1000
2. 停止搜索的策略：可以增加Nround参数来调整：多少次塞满候选队列之后，才停止程序。

###### 说明：

1. 4399的游戏页面主要有3种：普通FLASH游戏的封面页、普通FLASH游戏的播放页、网页游戏页面。
2. 网页游戏没有固定的解析格式，只能有效提取名称信息，对于数据分析意义不大，所以没有采集。
3. 得到的xlsx数据包括名称、分类、文件大小、专题、上线时间、简介等。
4. 进一步可以区分中英文名，调整专题、文件大小、上线时间的格式，增加URL属性。建立数据库、进行数据分析等。这些都没有完成。

