# Hermes 

Hermes is Lab41's foray into recommender systems. It explores how to choose a recommender system for a new application by analyzing the performance of multiple recommender system algorithms on a variety of datasets.

It also explores how recommender systems may assist a software developer or a data scientist to find new data, tools, and computer programs.

This readme will be updated as the project progresses so stay tuned!


## Documentation 

[Hermes Documentation](https://github.com/Lab41/hermes/tree/master/docs)


## Basic Installation Guide 

For a detailed installation guide, please read on [Hermes Installation Guide](https://github.com/Lab41/hermes/tree/master/docs/installation.txt).

### Dependencies: 
* Spark 1.5.1 
* Scala 2.11.7
* Pyspark 0.8.2.1
* Hadoop 2.7.1
* virtualenv

### How to Install Hermes: 

(Optional) After you have installed the dependencies, if you have different projects that require different Python environment, you can use a Virtual Environment. As listed in the Virtual Environment's [site](http://docs.python-guide.org/en/latest/dev/virtualenvs/), "a Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them."

```bash
$ virtualenv name_of_your_virtualenv
$ . name_of_your_virtualenv/bin/activate
```

To install Hermes, run 
```bash
$ python setup.py install
```

This will create a binary called hermes in /usr/local/bin/hermes. Instead of running the binary with the entire path (ie. ./usr/local/bin/hermes), you can install it so that you can run hermes without calling the entire path on the command line. 
```bash
$ pip install --editable .
```

Now, you can just run hermes the binary and it will prompt you with what you want to do with the data that you have. 
```bash 
$ hermes
```


## State of Build 

It is currently in progress. We will show the progress of the build using TravisCI once it is established.
