<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/cook_pan.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">颠勺</h3>

  <p align="center">
    一个嵌入式 Linux 项目构建管理工具 -- Bitbake UI 扩展功能
  </p>
</div>

<br/>
<br/>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>内容列表</summary>
  <ol>
    <li>
      <a href="#about-the-project">关于颠勺</a>
      <ul>
        <li><a href="#built-with">依赖</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">安装颠勺</a>
      <ul>
        <li><a href="#prerequisites">安装准备</a></li>
        <li><a href="#installation">安装</a></li>
      </ul>
    </li>
    <li><a href="#usage">使用颠勺</a></li>
    <li><a href="#roadmap">开发计划</a></li>
    <li><a href="#contributing">贡献代码</a></li>
    <li><a href="#license">许可说明</a></li>
    <li><a href="#contact">联系方式</a></li>
    <li><a href="#acknowledgments">相关知识</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 关于颠勺

![product-screenshot]

颠勺是一个嵌入式 Linux 项目构建管理工具，它主要基于 [Bitbake](https://github.com/openembedded/bitbake) 和 [Yocto](https://www.yoctoproject.org/) 项目使用。目的是降低 Bitbake 的使用门槛，提高 Yocto 项目的开发体验。

我为什么开发颠勺:

+ 许多开发者对于嵌入式 Linux 底层移植与开发并不感兴趣，也不想关心，希望专注于上层应用程序的开发以满足其业务需求。

+ 一个嵌入式 Linux 项目过于零散，由许多小的软件项目组成，如何使用优雅的方式管理项目是一个挑战

+ Bitbake 和 Yocto 是非常棒的项目，但是其学习曲线十分陡峭，对新手不友好。因此我希望通过颠勺去帮助初学者更快的学会开发 Yocto 项目

<p align="right">(<a href="#top">back to top</a>)</p>


### 开发依赖

颠勺主要是基于 Django 开发， 它通过由 Celery + Redis 支持的异步队列发送 bitbake 命令进行编译等操作，另外它使用 Postgresql 作为数据库


为了快速可靠的安装部署，颠勺和相关依赖均运行于 Docker 容器之中

* [Bitbake](https://github.com/openembedded/bitbake)
* [Yocto](https://www.yoctoproject.org/)
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)
* [Postgresql](https://www.postgresql.org/)
* [Celery](https://docs.celeryproject.org/en/stable/)
* [Redis](https://redis.io)
* [Skeleton](http://getskeleton.com/)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## 安装颠勺

由于颠勺运行于容器中，因此安装非常简便

### 安装准备

目前，颠勺已经在 Windows (Win10 & Win11) 和 Linux (Ubuntu & Fedora) 环境下完成测试。你可以选择你习惯的操作系统环境作为 Docker 主机， 请根据如下官方文档安装 Docker & Docker-Compose

[docker 安装说明](https://docs.docker.com/engine/install/)

[docker-compose 安装说明](https://docs.docker.com/compose/install/)


### 安装

1. Clone 仓库
    
    *在 Linux 环境中使用*
   ```sh
   $ git clone https://github.com/croakexciting/dianshao.git && cd ./dianshao
   ```

   *注意：由于 Bitbake 无法被 root 用户使用，因此请确保项目文件夹权限为 1000：1000*

    *在 Windows 环境中使用*

    ```sh
    $ git clone https://github.com/croakexciting/dianshao.git -c core.autocrlf=false
    
    $ cd ./dianshao

    $ rm .\yocto_projects\.gitkeep
    
    $ fsutil.exe file setCaseSensitiveInfo .\yocto_projects\ enable
    ```

2. Docker 镜像编译
   ```sh
   $ sudo docker-compose build
   ```

   *注意：如果使用国内网络编译速度过慢，可使用如下命令使用国内镜像源*

    ```sh
    $ cp ./docker/docker-compose-with-mirror.yml docker-compose.yml

   $ sudo docker-compose build
   ```

3. Docker 容器启动
   ```sh
   $ sudo docker-compose up
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## 使用颠勺

In general, the dianshao is an extension of Bitbake, which aims to help developers to develop yocto projects more conveniently.

总的来说，颠勺是 Bitbake 的拓展，目的是帮助开发者更方便的开发 Yocto 项目

If you are familiar with yocto, you will master dianshao quickly. If you are a beginner, it doesn’t matter, Dianshao will help you quickly understand and learn to develop yocto projects

如果你对 Yocto 很熟悉，那你会很快掌握颠勺。如果你是一个初学者，颠勺将帮助你快速理解和学会开发 Yocto 项目。但是建议你最好有一定的嵌入式 Linux 开发经验。

### 快速开始

1. 创建新项目


    输入项目名称并选择 Yocto 版本号，然后点击创建

    ![create-project-screenshot]


    等待项目初始化完成，初始化时间根据你的网络情况，可能会很长，请耐心等待

    ![project-initial-screenshot]



    如果初始化成功，页面如下所示

      ![success-initial-screenshot]

2. 增加你需要的元数据层

    初始化完成的 Yocto 项目中只包含核心层，如果你需要增加其他元数据层，请点击 *Add Therd-Party MetaLayer* 按钮

    输入元数据层名称并且选择导入方式，*remote* 方式意味这你想导入的层目前不在该 Yocto 项目主目录中，*local* 意思则相反。如果你选择 *remote*, 你需要输入 *Url*. 
    
    *sub* 意义为：如果你想导入的层是某个 Git 仓库的子目录， 例如 **meta-openembedded/meta-oe/**，那你需要在 *sub* 中填写 meta-oe


    ![addlayer-screenshot]

    
    等待进程结束，你会发现新添加的元数据层已经在列表中了

    ![after-addlayer-screenshot]


3. 测试 bitbake

    你可以在 *bitbake command* 界面中操作 bitbake，可以在该界面中感受颠勺如何操作 bitbake. 但是目前的 UI 还不够好，我会持续优化它。

    *注意：Bitbake 需要从零构建，对网络环境和计算资源要求很高，如果你使用普通个人电脑和国内网络，第一次编译的时间可能很长，请耐心*

    ![bitbake-test-screenshot]


### 开发 MyMeta

颠勺提供一系列工具帮助你开发自己的 Yocto 项目，包括定制你的设备，你的镜像和你自己开发或者想额外引入的软件包

颠勺通过自动生成 Yocto bbfiles, machine, distro 和 imagefiles 来实现上述功能，具体请见文档说明（即将上线）


### 在 IDE 或者编辑器中打开你的项目

通过颠勺自动生成的 Yocto 项目位于 ./yocto_project 中，按照打开正常文件的方式打开即可

### 使用命令行操作 Bitbake

如果你想按照传统的方式，在命令行中执行 Bitbake 命令， 请使用下面命令进入命令行，即可使用命令行

  ```sh
  $ docker exec -it dianshao-yocto bash
  $ cd ../yocto
  ```

<!-- TODO: doc!!!! _For more examples, please refer to the [Documentation](https://example.com)_ -->
 
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## 开发计划


- [ ] Bitbake progress ui optimization
- [ ] Git clone task restart after failed
- [ ] MyImage 
    - [ ] Image build tools
    - [ ] Image OTA support
- [ ] MyPakcage
    - [ ] System-V support

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## 贡献代码

如果你对该项目很感兴趣，非常欢迎贡献代码，并且请不要忘记 Star

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## 许可证

本项目基于 MIT 许可. 详情请见 `LICENSE`.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## 联系我

croakexciting - croakexciting@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## 相关知识

颠勺主要的目的是帮助你开发 Yocto 项目，所以你最好学习一些 Yocto 的基础知识

* [yocto official documentation](https://docs.yoctoproject.org/current/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/mainpage.PNG
[create-project-screenshot]: images/create_project.png
[project-initial-screenshot]: images/project_initial.png
[success-initial-screenshot]: images/success_init.png
[addlayer-screenshot]: images/addlayer.png
[after-addlayer-screenshot]: images/after_addlayer.png
[bitbake-test-screenshot]: images/bitbake_test.png