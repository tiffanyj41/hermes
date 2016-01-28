# How to use iPython Notebook

1. Install Anaconda
2. Launch Anaconda launcher
3. Launch ipython-notebook 
4. Create an iPython profile for use with PySpark
  1. Make sure you have exported PySpark classes to your python path and build Apache Spark. 
     To export PySpark classes, add the following to your ~/.bash_profile:

     ```bash
     # export spark to path
     export SPARK_HOME=/path/to/your/spark
     export PATH=$PATH:$SPARK_HOME/bin
     # export pyspark classes to the python path
     export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
     # export py4j to the python path
     export PYTHONPATH=$SPARK_HOME/python/lib/py4j-<version_number>-src.zip:$PYTHONPATH
     ```
     
  2. Build Apache Spark
  
     ```bash
    $ cd $SPARK_HOME
    $ sbt/sbt clean assembly
     ```
     
 ```bash
ipython profile create pyspark
 ```
5. Create a iPython notebook configuration

 ```bash
vim ~/.ipython/profile_pyspark/ipython_notebook_config.py
 ```
 ```bash
 c = get_config()
 
 # kernel configuration
 c.IPKernelApp.pylab = 'inline'  # set %matplotlib inline always
 
 # notebook configuration
 c.NotebookApp.ip = '*' # '*' == to bind on all IPs
 # do not open the browser at start of ipython notebook
 # so that we can point the ipython notebook address
 # in an active web browser
 c.NotebookApp.open_browser = False 
 
 # (optional) you can add password to your notebook if desired
 
 # set a fixed port number that does not conflict with other iPython profiles
 c.NotebookApp.port = 8880 
 ```
6. Create PySpark Setup configuration
 ```bash
 vim ~/.ipython/profile_pyspark/startup/00-pyspark-setup.py
 ```
 ```bash
 import os
 import sys
 import findspark
 
 # setup spark home
 findspark.init()
 spark_home = findspark.find()
 
 # setup spark home approach #2
 # make sure you have already set $SPARK_HOME in $PATH
 # spark_home = os.environ.get('SPARK_HOME', None)

 # add spark's home directory to path
 sys.path.insert(0, os.path.join(spark_home, "python")) 
 
 # add py4j to path
 sys.path.insert(0, os.path.join(spark_home, "python/lib/py4j-0.8.2.1-src.zip"))
 
 # initialize pyspark to predefine the SparkContext variable "sc"
 execfile(os.path.join(spark_home, "python/pyspark/shell.py"))
 ```
 
7. Run iPython notebook in your desired directory
 ```bash
 ipython notebook --profile=pyspark
 ```

8. Test to see if sc is defined. If not, setup the SparkContext and SQLContext by doing the following in your iPython notebook
 ```bash
 from pyspark import SparkContext
 from pyspark.sql import SQLContext 
 
 # setup SparkContext
 try:
     sc = SparkContext()
 except:
     sc = SparkContext._active_spark_context

 # setup SQLContext
 sqlCtx = SQLContext(sc)
 ```

9. When you are reading your JSON, you need to determine your fs.default.name or fs.defaultFS. You can figure this out by checking out the core-site.xml file. This can be found in Mac OS at /usr/local/Cellar/hadoop/<hadoop_version_number>/libexec/etc/hadoop/core-site.xml. To read JSON using SQLContext, you have to add this ip address when calling the function. 

For example: your fs.default.name or fs.defaultFS is hdfs://localhost:9000. To use one of the JSON files that you have put into the datasets directory in HDFS, you have to call as follows:
 ```bash
 dataframe = sqlCtx.read.json("hdfs://localhost:9000/datasets/movielens_1m_movies.json.gz")
 ```
