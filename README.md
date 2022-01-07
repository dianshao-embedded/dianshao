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
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



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

![Product Name Screen Shot][product-screenshot]

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

Since the program runs in a docker container, installation is very easy

### Prerequisites

Currently, the Dinashao has been tested on windows (Win11) and linux (Ubuntu & Fedora & centos) host. You can choose you preferred operating system as the docker host

Please Install docker & docker-compose according to the official documentation

[docker install doc](https://docs.docker.com/engine/install/)

[docker-compose install doc](dochttps://docs.docker.com/compose/install/)

***notes:*** If you use dianshao on windows, please create a "/.dianshao" folder in your home path (C:\Users\username) and turn on folder **case sensitive** properity using the following command before installation

```sh
fsutil.exe file setCaseSensitiveInfo .\.dianshao\ enable
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/croakexciting/dianshao.git
   ```
2. Docker Image build
   ```sh
   sudo docker-compose build
   ```
3. Docker Container up
   ```sh
   sudo docker-compose up
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

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
[product-screenshot]: images/mainpage.png
