### TODO:

-------------

+ MyPackage
    1. 去除文件内容数据库存储 - 完成
    2. Install 任务智能增加 (提供文件名和安装目的地) - 挂起
    1. System-V 支持 - 挂起

--------------

+  MyMachine - 完成
    1. board 及芯片选取
    1. u-boot 选取 (根据board或者芯片型号，也可以自定义)
    2. 内核选取 (根据board或者芯片型号)
    3. 文件系统格式及相关格式参数
    4. systemd or system-V
    5. machine include file
    6. distro include file
    7. extra macro define
    8. imx6ull 最小可启动 u-boot 及 kernel
----------

+  MyImage
    1. 包构建选取功能 - 挂起
    2. 镜像构建功能 (分区设置及自动dd工具) - 挂起
    3. 固件升级方式设计 (基于overlay方式实现) - 挂起

-----------

+ 项目部署
    1. python 项目打包
    2. docker 镜像制作

--------------

+ 可靠性
    1. bitbake 错误信息处理 - 完成基础功能
    2. bitbake 锁及后台运行，刷新可恢复 - 挂起
    3. bitbake 任务心跳包 - 心跳包超时未完成
    3. 项目完整性检查
    4. Git 任务失败重新开始 - 完成
    5. Git 任务锁及后台运行 - 挂起
    1. 重启一切，包括重启任务

--------------


+ Meta-Layer
    1. 本地 meta layer 增加
    2. meta-layer 子文件夹添加
    3. meta-layer 增加错误处理
    4. 本地项目导入

TODO: add mirror docker file using instruction
Windows 上使用需要打开 区分大小写属性
fsutil.exe file setCaseSensitiveInfo .\.dianshao\ enable
使用时需要创建文件夹，linux需要设置权限，windows上需要打开大小写属性区分