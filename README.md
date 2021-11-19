# Attack Graph Generator for Microsservice Architectures

This attack graph generator is an upgrade to an old generator made by Tum Informatik Chair 4, updated in order to use Clair4.

Given the rise of Microsservices, due to their various benefits, such as elasticity and managenability, it is important to keep security up to date on the various deployments.
One way to do it is by analysing possible attack paths that adversaries can take.
This can be done looking at attack graphs and protecting the various services based on these.
The portability aquired by docker images, allows the developers to compress the whole service into a single image, which then enables us to verify what vulnerabilities exist inside a certain service.

# Academic Citation 
You can cite the following paper with the original work:

Ibrahim, Amjad, Stevica Bozhinoski, and Alexander Pretschner. "Attack graph generation for microservice architecture." Proceedings of the 34th ACM/SIGAPP Symposium on Applied Computing. ACM, 2019.

@inproceedings{ibrahim2019attack,
  title={Attack graph generation for microservice architecture},
  author={Ibrahim, Amjad and Bozhinoski, Stevica and Pretschner, Alexander},
  booktitle={Proceedings of the 34th ACM/SIGAPP Symposium on Applied Computing},
  pages={1235--1242},
  year={2019},
  organization={ACM}
}

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project works currently only on Ubuntu 16.04.4 LTS. Executing the program for the first time will download all of the needed libraries/components including:

* [Python 3.6](https://www.python.org/downloads/) - a programming language.
* [Pip](https://pypi.org/project/pip/) - a tool for installing Python packages.
* [Docker Community Edition (CE)](https://docs.docker.com/install/linux/docker-ce/ubuntu/) - a computer program that performs operating-system-level virtualization, also known as "containerization".
* [Docker Compose](https://docs.docker.com/compose/) - a tool for defining and running multi-container Docker applications.
* [Go](https://github.com/golang/go) - an open source programming language that makes it easy to build simple, reliable, and efficient software.
* [Clairctl](https://github.com/jgsqware/clairctl) - a lightweight command-line tool doing the bridge between Registries as Docker Hub, Docker Registry or Quay.io, and the CoreOS vulnerability tracker, Clair.
* [Graphviz](https://www.graphviz.org/) - an open source graph visualization software.
* [Yaml](http://yaml.org/) - a human-readable data serialization language.
* [Networkx](https://networkx.github.io/) - a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* [Numpy](http://www.numpy.org/) - a fundamental package for scientific computing with Python.

### Installing

All of the libraries/components indicated above are automatically installed during the first running of the program. For how to run the program, please refer to the commands bellow.

### Running

In order to run the program, the user needs to enter the home directory of the project and the following command on the terminal should be run:

```
$ sudo ./attack-graph-generator.sh ./examples/atsea

```

The above command starts the attack-graph-generator.sh script and generates an attack graph for the system ./examples/atsea. This command will download and install the required libraries and set up environment variables when run for the first time. Afterward, it performs the attack graph analysis.

Other examples are
```
$ sudo ./attack-graph-generator.sh ./examples/javaee
$ sudo ./attack-graph-generator.sh ./examples/example
$ sudo ./attack-graph-generator.sh ./examples/netflix-oss-example

```

* Please note that on the first try, Clair populates the database, so that is why the attack graph will be empty. Furthermore, building the images in the vulnerability-parser for the first time takes longer. The code is tested on a virtual machine running on the above-mentioned operating system.

### Customizing the attack graph generation

The config file is the main point where the attack graphs can be customized. The attack graph generation can be conducted in either online or offline mode. Online mode uses Clair for vulnerabilities detection and takes more time. Offline mode uses already created vulnerability files (by Clair) and performs the attack graph analysis. Therefore, the offline mode does not require an internet connection. Because the edges can have many vulnerabilities, there is an option if we want to display the attack graph with separate edges with different vulnerabilities or combine all of them in one edge. Another option is to display only one vulnerability per edge in the attack graph. Finally, the user has to possibility to modify the pre- and postcondition rules from which the attack graphs are created. For additional details on how to use the config file, please refer to the comments in the config.yml file.

## Authors

* Paulo Gonçalves pgoncalves@student.dei.uc.pt

Original Authors:
* Stevica Bozhinoski stevica.bozhinoski@tum.de
* Amjad Ibrahim, M.Sc. amjad.ibrahim@tum.de

## License

## Acknowledgments

We would like to thank the teams of [Clair](https://github.com/coreos/clair) and [Clairctl](https://github.com/jgsqware/clairctl) for their vulnerabilities generator, which is an integral part of our system. Additional thanks to the contributors of all of the third-party tools used in this project.
