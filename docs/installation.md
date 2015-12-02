## Hermes Installation Guide

### Dependencies: 
* Spark 1.5.1 
* Scala 2.11.7
* Pyspark 0.8.2.1
* Hadoop 2.7.1
* virtualenv

### How to Install Dependencies on Mac OS X: 
#### Installing Spark, Scala, and PySpark 
1. Install Java
  1. Download 
  2. Double click on .dmg file to install.
  3. In a terminal, type java -version. You should see the following: 
`
java version "1.8.0_65"
Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
`
2. Set JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home)

3. Install Homebrew
`
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
`

4. Install Scala
`
brew install scala
`

5. Download Spark from https://spark.apache.org/downloads.html. 

6. Set SCALA_HOME and SPARK_HOME and export it to path in your .bash_profile.
`
export SPARK_HOME=/path/to/your/spark
export PATH=$PATH:$SPARK_HOME/bin
export SCALA_HOME=/path/to/your/scala
export PATH=$PATH:$SCALA_HOME/bin
`

7. Export PySpark classes to the Python path after you have installed Python.
`
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
`

8. Build and install Apache Spark
`
brew install sbt
cd $SPARK_HOME
sbt/sbt clean assembly
`

#### Installing Hadoop  
Please follow this [guide](http://zhongyaonan.com/hadoop-tutorial/setting-up-hadoop-2-6-on-mac-osx-yosemite.html).

#### Installing virtualenv 
Please read this [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for more details.
`
pip install virtualenv
`

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

This will create a binary called hermes in /usr/local/bin/hermes. Instead of running the binary with the entire path (ie. ./usr/local/bin/hermes), you can install it so that you can run hermes automatically on the command line. 
```bash
$ pip install --editable .
```

Now, you can just run hermes the binary and it will prompt you with what you want to do with the data that you have. 
```bash 
$ hermes
```