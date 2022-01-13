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

  <h3 align="center">Dianshao</h3>

  <p align="center">
    An Embedded Linux Project Build and Compile Tool
  </p>

  <p align="center">
    <a href="https://github.com/croakexciting/dianshao/blob/main/README-CN.md">中文说明</a>
  </p>
</div>

<br/>
<br/>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![product-screenshot]

The Dianshao is an embedded linux project build and compile tool, it is developed based on [Bitbake](https://github.com/openembedded/bitbake) and [Yocto](https://www.yoctoproject.org/) project. It can lower the threshold of using Bitbake and provide an interactive web UI to enhance the experience of using Bitbake

Here is why:

+ Many developers are not interested in embedded bottom-level porting and development, and hope to focus on application development

+ Embedded projects are too scattered, and there is no good management tool to help developers manage their projects in a elegant way

+ Bitbake is an awesome project, but his learning curve is steep and not easy to use. So I developed **dianshao** to help developers use bitbake more easily
<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

Dianshao is mainly developed based on Django framework, it operates bitbake through asynchronous task queue supported by Celery + Redis and uses Postgresql as database.

For reliable and rapid deployment, Dianshao and related dependencies run in the docker containers

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
## Getting Started

Since the program runs in a docker container, installation is pretty easy

### Prerequisites

Currently, the Dinashao has been tested on windows (Win10 & Win11) and linux (Ubuntu & Fedora & centos) host. You can choose you preferred operating system as the docker host

Please Install docker & docker-compose on your host according to the official documentation

[docker install doc](https://docs.docker.com/engine/install/)

[docker-compose install doc](https://docs.docker.com/compose/install/)


### Installation

1. Clone the repo
    
    *Using on Linux*
   ```sh
   $ git clone https://github.com/croakexciting/dianshao.git && cd ./dianshao
   ```
    *Using on Windows*

    ```sh
    $ git clone https://github.com/croakexciting/dianshao.git -c core.autocrlf=false

    $ cd ./dianshao
    ```

2. Set Your Yocto Project Path
   ```sh
   $ export DIANSHAO_YOCTO_PROJECT_PATH="your yocto project path"
   ```

    *notes：If using on Linux, please don't use dianshao in root and make sure the folder permissions is 1000:1000*

    ```sh
    $ sudo chown -R 1000:1000 $DIANSHAO_YOCTO_PROJECT_PATH
    ```

    *notes：If using on windows, please enable the folder case sensitive option*

    ```sh
    $ fsutil.exe file setCaseSensitiveInfo $DIANSHAO_YOCTO_PROJECT_PATH enable
    ```

2. Docker Image build
   ```sh
   $ sudo docker-compose build
   ```
3. Docker Container up
   ```sh
   $ sudo docker-compose up
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

In general, the dianshao is an extension of Bitbake, which aims to help developers to develop yocto projects more conveniently.

If you are familiar with yocto, you will master dianshao quickly. If you are a beginner, it doesn’t matter, Dianshao will help you quickly understand and learn to develop yocto projects

### Quick Start

1. Create a new yocto project

    Enter your project name and version, then click button

    ![create-project-screenshot]


    Wait for the project initialization to complete, it may take some time

    ![project-initial-screenshot]


    If the initialization is successful, the page is as follow
      ![success-initial-screenshot]

2. Add other layers you need

    The initialized project only contains the core layer, if you need to add other layers, please click *Add Therd-Party MetaLayer* button

    Enter the layer name and choose the import method, the remote means that the git repo does not exist in the main directory, and the local means the opposite. If you choose *remote*, you need to input layer url. the *sub* means that the layer you want to import is located in a subdirectory of a git repo, such as **meta-openembedded/meta-oe/**.


    ![addlayer-screenshot]

    
    Wait for the process to complete,  and you will find the layer now is in the list

    ![after-addlayer-screenshot]


3. Test bitbake

    You can bitbake anything in *bitbake command* page, you can use this page to test how to operate bitbake. The current UI is not good enough, I will continue to optimize it

    ![bitbake-test-screenshot]


### Develop MyMeta

Danshao provides a range of tools to help you develop your own embedded projects, including customizing your device, your images, and packages that you develop yourself or want to introduce additionally

Danshao achieves the above functions by helping you to automatically generate yocto bbfiles, machine, distro and imagefiles. See the documentation (coming soon) for specific instructions



### Open your yocto project in IDE

The yocto project generate by dianshao is located at ./yocto_project, you can open the yocto project in IDE as normal


### Development in the command line

If you want to execute the bitbake command directly using the command line, Please use the following command to enter inside the container, and then use the command line

  ```sh
  $ docker exec -it dianshao-yocto bash
  $ cd ../yocto
  ```

<!-- TODO: doc!!!! _For more examples, please refer to the [Documentation](https://example.com)_ -->
 
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap


- [ ] Bitbake progress ui optimization
- [ ] Git clone task restart after failed
- [ ] MyImage 
    - [ ] Image build tools
    - [ ] Image OTA support
- [ ] MyPakcage
    - [ ] System-V support

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

croakexciting - croakexciting@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The dianshao is mainly used to help you use yocto, so you need to know the basics of yocto

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
[readme-chinese]:README-CN.md