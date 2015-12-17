# Understanding Hermes's Framework

* [Command Line Utilities](#command-line-utilities)
* [General Framework Concepts](#general-framework-concepts)
* [Main Components](#main-components)
  * [hermesctl.py](#hermesctlpy)
    * [Revising Hermes's Version Number](#revising-hermess-version-number)
    * [Revising What to Log](#revising-what-to-log)
    * [Understanding Spark Context](#understanding-spark-context)
    * [Adding New Global Variables](#adding-new-global-variables)
    * [Adding New States in State Machine](#adding-new-states-in-state-machine)
    * [Adding New Variables in Cargo](#adding-new-variables-in-cargo)
    * [Adding and Extracting New Configuration Variables](#adding-and-extracting-new-configuration-variables)
      * [Adding New Configuration Variables](#adding-new-configuration-variables)
      * [Extracting New Configuration Variables](#extracting-new-configuraiton-variables)
  * [hermes.py](#hermespy)
    * [Currently Defined States](#currently-defined-states)
      * [start_state](#start_state)
      * [json_to_rdd_state](#json_to_rdd_state)
      * [split_data_state](#split_data_state)
      * [make_prediction_state](#make_prediction_state)
      * [calculate_metrics_state](#calculate_metrics_state)
      * [error_state](#error_state)    
    * [Handling Multiple Next States](#handling-multiple-next-states)  
    * [Defining a New State](#defining-a-new-state)
  * [hermesui.py](#hermesuipy)
    * [Adding Additional UI](#adding-additional-ui)
* [Helper Components](#helper-components)
  * [singleton.py](#singletonpy)
  * [globals.py](#globalspy)
  * [helper.py](#helperpy)
    * [Adding New Global Helper Function](#adding-new-global-helper-functions)
  * [cargo.py](#cargopy)
  * [config.py](#configpy)
  * [data.py](#datapy)
    * [Adding New Vector Type](#adding-new-vector-type)
  * [vectorgenerator.py](#vectorgeneratorpy)
    * [Understanding What Vectors Are](#understanding-what-vectors-are)
    * [Adding New Vector Type](#adding-new-vector-type-1)
    * [Adding New Dataset](#adding-new-dataset)
    * [Adding New Vector Transformation](#adding-new-vector-transformation)
  * [recommendergenerator.py](#recommendergeneratorpy)
    * [Adding New Recommender System Algorithms](#adding-new-recommender-system-algorithms)
    * [Implementing a Different Use Case for a Specific Recommender System Algorithm](#implementing-a-different-use-case-for-a-specific-recommender-system-algorithm)
  * [metricgenerator.py](#metricgeneratorpy)
    * [Adding New Metric](#adding-new-metric)
  * [statemachine.py](#statemachinepy)
  * [timer.py](#timerpy)

## Command Line Utilities

Hermes uses Click as its command line utilities. To learn what parameters Hermes take for the command line, please read the guide [How to Run Hermes]
(https://github.com/lab41/hermes/tree/master/docs/run.md).

## General Framework Concepts

The goal of Hermes is to give user the ability to run multiple recommender system algorithms and metrics on a particular dataset to determine which recommender system works best for this dataset. For this reason, we want to make the framework as modular as possible so that user can implement his/her own recommender system algorithms or performance metrics as needed if they were not yet implemented by default, asssuming that the target user is a data scientist.

Hermes relies on a state machine as its framework. The beauty of the state machine is that state machine allows modularity. Each state represents a particular functionality, and states do not have to follow a singular path. This means that each state has the option to go to multiple different states for its next state depending on the context it was placed. 

Currently, Hermes has 5 states defined; they are start_state, json_to_rdd_state, split_data_state, make_prediction_state, and calculate_metrics_state. These states make up a state machine that follows this particular path (which can be subjected to change):

```bash
start_state -> json_to_rdd_state -> split_data_state -> make_prediction_state -> calculate_metrics_state 
```

Details of what each state does is explained in [hermes.py](#hermespy).

Reading this entire article will give you the complete understanding of what the framework does. But if you wanted a TL;DR version, please check out the following:
* If you do not know a particular term used in Hermes, please check out the glossary:
  * [Glossary](https://github.com/Lab41/hermes/tree/master/docs/glossary.md)
* If you are planning to change the flow of the state machine, please read:
  * [Adding New States in State Machine](#adding-new-states-in-state-machine)
  * [Defining a New State](#defining-a-new-state)
  * [Handling Multiple Next States](#handling-multiple-next-states)  
* If you are planning to use your own dataset not yet supported by Hermes, please read:
  * [Understanding What Vectors Are](#understanding-what-vectors-are) 
  * [Datasets Supported](https://github.com/Lab41/hermes/tree/master/docs/data_supported.md), in particular Adding New Datasets section.
* If you are planning to use your own recommender system algorithms not yet supported by Hermes, please read:
  * [Recommender System Algorithms Supported](https://github.com/Lab41/hermes/tree/master/docs/recommenders_supported.md), in particular Adding New Recommender System Algorithm section.
* If you are planning to use your own metrics not yet supported by Hermes, please read:
  * [Metrics Supported](https://github.com/Lab41/hermes/tree/master/docs/metrics_supported.md), in particular Adding New Metric section.

## Main Components

Hermes has three main components: hermesctl.py, hermes.py, and hermesui.py. 
* hermesctl.py is the entry point; it also handles instantiation. 
* hermes.py defines every state in the state machine. 
* hermesui.py defines the command line UI used in hermes.py.

### hermesctl.py

**Path: hermes/hermes/hermesctl.py**

When you run the hermes binary, it will call on the main() function found in hermesctl.py. 

hermesctl.py is responsible for
* printing Hermes's version number 
* initializing global varibles
* instantiating state machines
* creating cargo used in state machines
* parsing the configuration files
* running state machine 

#### Revising Hermes's Version Number

You can check Hermes's version number by running
```bash
$ hermes --version
```

Team members revise the version number found in `hermes/hermes/__init__.py.`

#### Revising What to Log

We employ the logging library to log INFO, DEBUG, and ERROR messages. The logger is a global variable with the name "hermes".

All INFO messages are outputted to the command line.

ALL DEBUG messages are outputted to the command line and a log file called hermes.log. hermes.log is created wherever the hermes binary is run. Debug messages will only print when the --verbose option is passed.

ALL ERROR messages are outputted to the command line and stderr.

#### Understanding Spark Context

Spark Context will not be instantiated if you run the framework in an iPython notebook (TODO: in development). 

Otherwise, it is wrapped in a singleton pattern to avoid multiple instantiation with the app name of "hermes". The singleton wrapper is defined in [singleton.py](#singletonpy)

#### Adding New Global Variables

Global variables are defined in [globals.py](#globalspy) and instantiated in hermesctl's main(). 

To add a new global variable, please define it in the Globals class in [globals.py](#globalspy). 

A list of what global variables are currently defined can be found in [globals.py](#globalspy).

#### Adding New States in State Machine

You can add a new state to Hermes in hermesctl's add_states() function, but you need to define what the state does (including where it needs to go next) in [hermes.py](#hermespy). If the new state is an end state, meaning there is no other state to go to next, you have to specify that it is an end state.

To add a state, add the following line in hermesctl's add_states():
```bash
state_machine.add_state(hermes.new_state)
```

To add an end state, add the following line in hermesctl's add_states():
```bash
state_machine.add_state(hermes.new_state, isEndState=True)
```

#### Adding New Variables in Cargo

Cargo is the object passed around in the state machine. Since we can never know until runtime where each state has derived from and where it will go next, we do not know what parameters to pass into each state. Cargo encapsulates all the parameters needed for each state in one object. It is defined in [cargo.py](#cargopy) and instantiated in hermesctl's main(). Future implementation will clean up Cargo so that one state does not know what another state's parameter needs are unless necessary (TODO: in development).

To add a new variable in cargo for use in your newly defined state, please define it in the constructor of the Cargo class in [cargo.py](#cargopy). 

A list of what variables are currently defined in cargo can be found in [cargo.py](#cargopy).

#### Adding and Extracting New Configuration Variables

Configuration Files are currently extracted via the ConfigParser library. In the future, we might use ConfigObj as it supports subsections, which ConfigParser does not support (TODO: in development).

Listed below are recognized sections and their respective items:
* datasets
  * vectorizer
  * user_vector_data
  * user_vector_transformations
  * user_vector_schemas
  * content_vector_data
  * content_vector_transformations
  * content_vector_schemas
* recommenders
  * recommenders
* metrics
  * metrics

What Hermes will do when it encounters unrecognized section or section's item:
* If it does not recognize the section, it will skip the entire section.
* In datasets section, if vectorizer is not specified, it will quit the program.
* In datasets section, if User Vector (user_vector_data, user_vector_transformation) or Content Vector (content_vector_data, content_vector_transformation) or both are not specified, it will quit the program. In the future, it will also quit the program if it does not have User Vector and Content Vector specified when Content Vector is already specified (TODO: in development).
* Any other items in datasets that are not recognized are treated as a support_file item, meaning the variable is placed as a key and its value is placed as a value in a dictionary called support_files to be used later when generating the vector.
* In recommenders section, any items that are not recognized will be skipped. In the future, extra parameter variables needed for recommender system algorithms will be recognized (TODO: in development).
* In metrics section, any items that are not recognized will be skipped. In the future, extra parameter variables needed for calculating the metrics will be recognized (TODO: in development).

Note that in datasets section, if user_vector_data and user_vector_transformations are defined in the configuration file, hermesctl.py will store these values inside a UserVector Data object. Similarly, if content_vector_data and content_vector_transformations are defined in the configuration file, hermesctl.py will store these values inside a ContentVector Data object. All Data objects are then placed inside Cargo's data list. 

##### Adding New Configuration Variables

Add any [new_section] in the configuration file. Add any new section's items underneath the [new_section] in the configuration file as needed.

##### Extracting New Configuration Variables

To make your new section and its items recognizable, add them in [configs.py](#configspy)'s HEADINGS variable.

Handle its extractions in hermesctl's extract_configs() function. For handling the pecularities of the section, follow the example of the datasets section. For handling the recognized and unrecognized section items, handle it in extract_configs()'s helper function handle_recognized_section_item() and handle_unrecognized_section_item() respectively.

### hermes.py

**Path: hermes/hermes/hermes.py**

hermes.py defines all functions for all states in the state machine.

#### Currently Defined States
 
##### start_state

start_state creates the HDFS directory specified by the user (if the user does not specify it, the default is datasets) and loads all JSON files into this HDFS directory.

##### json_to_rdd_state

json_to_rdd_state converts the JSON file into its respective RDD or Vectors.

##### split_data_state

split_data_state splits the data in Vector into train data, test data, and validation data depending on the input given by the user at runtime.

##### make_prediction_state

make_prediction_state takes the train data from each Vector, develop model based on the train data and the recommender in configuration file, and make prediction based on this model.

##### calculate_metrics_state

calculate_metrics test the metrics specified in the configuration file. This is an end state.

##### error_state

error_state is where states go when they encounter an error. This is an end state.

#### Handling Multiple Next States

If you wanted a state to go to multiple next states, define the switch in the state of interest and make sure you return newState and cargo with the correct next state (name of the state function) and necessary parameters initialized or added to cargo.

#### Defining a New State

Defining a new state is the same as defining a function in hermes.py. Make sure you add the new state into the state machine by following the instructions in [Adding New States in State Machine](#adding-new-states-in-state-machine).

### hermesui.py

**Path: hermes/hermes/hermesui.py**

hermesui.py defines all the command line user interface used in hermes.py.

#### Adding Additonal UI 

Most configuration can be addressed using the configuration file. However, if you needed to ask the user for a configuration at runtime, define the UI function in hermes.py and call it as needed in the required state.

## Helper Components

### singleton.py

**Path: hermes/modules/singleton.py**

SCSingleton is a singleton pattern object that wraps the Spark Context to avoid multiple instantiation of the Spark Context.

### globals.py

**Path: hermes/modules/globals.py**

Listed below are the currently defined global variables:
* verbose: a boolean variable that prints out debug log messages
* logger: logging object that logs messages
* scsingleton: singleton object that defines the Spark Context

To add a new global variable, please see [Adding New Global Variables](#adding-new-global-variables).

### helper.py

**Path: hermes/modules/helper.py**

helper.py defines all global helper functions used in multiple places throughout the framework. 

#### Adding New Global Helper Function

To add a new global helper function, create the function in helper.py and import helper.py to the necessary file.

### cargo.py

**Path: hermes/modules/cargo.py**

Cargo is the object passed around in the state machine. Since we can never know until runtime where each state has derived from and where it will go next, we do not know what parameters to pass into each state. Cargo encapsulates all the parameters needed for each state in one object.

Listed below are the currently defined cargo variables:
* hdfs_dir: Name of HDFS directory to store input data. One of the option passed in when running hermes binary. Default = datasets.
* fs_default_ip_addr: IP address of fs.default.name used in HDFS. One of the arguments passed in when running hermes binary. Default = localhost:9000.
* datas: List of Data objects initialized when extracting the configuration file. 
* vectors: List of Vector objects initialized during one of the states in the state machine, json_to_rdd_state.
* support_files: Unrecognized items in [datasets] section of the configuration file that is presumed to be support files for the creation of a Vector.
* recommenders: List of recommender system algorithms initialized when extracting the configuration file.
* metrics: List of metrics initialized when extracting the configuration file.
* error_msg: It starts out as an empty string that will be initialized as an error message to the error state.

To add a new variable in cargo, please see [Adding New Variables in Cargo](#adding-new-variables-in-cargo).

### config.py

**Path: hermes/modules/config.py**

config.py has a list of recognized section and section's items used in the parsing of the configuration file. It also has functions defined to assist in the parsing of the configuration file. 

### data.py

**Path: hermes/modules/data.py**

Class Data is defined in data.py to store the configurations specified in the configuration file. We have not decided whether or not this is the best way to store configurations from the configuration file. (TODO: in development)

Currently, it has a subclass called UserVectorData nad ContentVectorData to differentiate the two different Vector Types that Hermes supports.

#### Adding New Vector Type

Hermes has two vector types: UserVector and ContentVector. If you wanted to add a new vector type, you will need to follow the instructions in [Adding New Vector Type](#adding-new-vector-type-1) under the vectorgenerator.py as well as add its respective Data object for storing its configuration. 

### vectorgenerator.py

**Path: hermes/modules/vectorgenerator.py**

#### Understanding What Vectors Are

In Hermes, when we referenced a vector, it refers to a dataframe that has been converted to a RDD after a transformation occurs. This transformation is specified by the vector transformation. For example, if you have Movie Lens data and you wanted to build a user vector from this data, if you specified the vector transformation to be "ratings" in the configuration file, the data from the JSON file is transformed into a dataframe and then a RDD of [(user_id, item_id, rating)]. In other words, the output of this transformation is a vector of [(user_id, item_id, rating)].

There are two types of vectors: User Vector and Content Vector. User Vector refers to the vector describing users in the data. Content Vector refers to the vector describing content in the data. Collaborative Filtering Recommender System typically uses only User Vector, and Content Based Recommender System typically uses both User Vector and Content Vector, but this does not have to be the case.

Every vector type inherits from the Vector class, meaning all User Vector and Content Vector will have the following variables:
* data: a Data object containing the configuration for this particular vector from the configuration file
* support_files: list of unrecognized variables in [datasets] section of the configuration file that we assume is a support file for the creation of a Vector
* vector_transformation: transformation needed to convert data from a JSON file to a specified vector
* training_vector: part of the vector that is split for training
* test_vector: part of the vector that is split for test
* validation_vector: part of the vector that is split for validation
* prediction_vector: part of the vector that is predicted based on test_vector and the model that is created from training_vector 

Since each data requires its own specific vector transformation, every data has its own class as well as its own UserVector and ContentVector. The data's UserVector and ContentVector inherit from both the data's own class as well as UserVector or ContentVector respectively. The data's UserVector and ContentVector have functions defined in their class to execute vector transformation. The name of these functions has to match the name of the vector transformation passed in via the configuration file in order for the vector transformation to occur. 

Vectorizer is a variable used in configuration file to refer to the data where each JSON file is coming from. The data's own class has a check function called isSameDataInstance() to verify that the vectorizer passed in via the configuration file is describing about the same data as data's own class.

To automatically create a vector (ie. which vector type and from which data), VectorFactory is there to the rescue! It can either return a Vector object or the RDD / vector itself by calling VectorFactory().create_obj_vector(...) or VectorFactory().create_vector(...) respectively.

#### Adding New Vector Type

UserVector and ContentVector are two vector types supported in Hermes. If you wanted to add a new vector type, create a class for your new vector type that inherits the Vector class. Add additional variables and functions as needed to the class.

```bash
class MyNewVectorType(Vector):
    pass
```

#### Adding New Dataset

Please read [Datasets Supported's section on Adding New Datasets](https://github.com/Lab41/hermes/tree/master/docs/data_supported.md#adding-new-datasets).

#### Adding New Vector Transformation

To add a new vector transformation, go to the data class itself and decide which vector type it is. Under the class of the vector type, define the new vector transformation as a class function.

For example: if you wanted to create a vector transformation for MovieLens data's UserVector, do the following:
```bash
class MovieLens(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.vectorizer == "movielens"

class MovieLensUserVector(UserVector, MovieLens):
    def ratings(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating))

    def new_vector_transformation:
        # your defined vector transformation
        ...
        return vector_after_the_transformation

```
Except instead of naming the new function as new_vector_trasnformation, name it according to what you want to use in the configuration file.

### recommendergenerator.py

**Path: hermes/modules/recommendergenerator.py**

recommendergenerator.py is built to allow clearer execution of code using the bridge pattern. For example, let's try to create a model using ALS. To do so, we can execute the following:

```bash
import recommendergenerator as rg

recommender = rg.ALS(vector)
```

We can then make a prediction because the Recommender object already knows about the recommender system algorithm to use as well as the training and test data from the parameter vector that we passed in.

```bash
prediction_vector = recommender.make_prediction()
```

If we have a specific use case that is different than the normal ALS use case, we can define that abnormal use case for ALS and call it as follows:

```bash
abnormal_usecase = AbnormalUseCase()
recommender = ALS(abnormal_usecase)
prediction_vector = recommender.make_prediction()
```

We do not have to call the make_prediction() function differently. We just call make_prediction() because it will call make_prediction() specifically for the abnormal use case.

Also, when you change the recommender system algorithm, say for example CBWithKMeans, all you need to do is create this Recommender object and when you are ready to make your prediction, call make_prediction() because it will make sure that behind the scene, it will call CBWithKMeans's make_prediction().

```bash
recommender = CBWithKMeans()
prediction_vector = recommender.make_prediction()
```

#### Adding New Recommender System Algorithms

To add a new recommender system algorithm, instantiate a class that inherits from Recommender class and defines the make_prediction() function that calls on the recommender system algorithm's own make prediction function. 

```bash
class NewRecommenderSystemAlgorithm(Recommender):
    def make_prediction(self)
        return self.implementation.make_prediction_with_new_recommender_system_algorithm(self.vector)
```

self.implementation is the use case that you want to use. The default use case is the Normal class. If you have another use case, for example: an abnormal use case, you want to instantiate a class called Abnormal, for example, that inherits from ImplementationInterface. 

So let's do that, let's define an abnormal use case.
```bash
class Abnormal(ImplementationInterface):
    pass
```

Let's say we want to define the make_prediction() function for both normal and abnormal use case. Therefore, the first thing we need to do is define the make_prediction() function for our new recommender system algorithm in the ImplementationInterface so that in case there is another use case that does not implement our new recommender system algorithm's make_prediction() function, it will fail by raising a NotImplemented error.

```bash
class ImplementationInterface(object):
    def make_prediciton_with_als(self):
        raise NotImplemented

    def make_prediction_with_cbwithkmeans(self):
        raise NotImplemented

    def make_prediction_with_new_recommender_system_algorithm(self):
        raise NotImplemented
```

After you defined in the ImplementationInterface class, you also want to define it in Normal class.

```bash
class Normal(ImplementationInterface):
    def make_prediction_with_als(self):
        ...
        return prediciton_vector

    def make_prediction_with_cbwithkmeans(self):
        ...
        return prediction_vector

    def make_prediction_with_new_recommender_system_algorithm(self):
        # implement your make_prediction() for the normal use case
        return prediciton_vector
```

Now begin implementing it in your Abnormal class too.
```bash
class Abnormal(ImplementationInterface):
    def make_prediction_with_new_recommender_system_algorithm(self):
    # implement your make_prediction() for the abnormal use case
    return prediction_vector
```

You are done. :)

#### Implementing a Different Use Case for a Specific Recommender System Algorithm

Let's do this with the ALS recommender system algorithm. We want to create an abnormal use case. To do so, we need to instantiate the Abnormal class that inherits from ImplementationInterface.

```bash
class Abnormal(ImplementationInterface):
    pass

```

Since ALS's make_prediction() function is already defined in the normal use case, we just need to define it also in the abnormal use case with the abnormal use case's implementation.

```bash
class Abnormal(ImplementationInterface):
    def make_prediction_with_new_recommender_system_algorithm(self):
    # implement your make_prediction() for the abnormal use case
    return prediction_vector
```

You are done. :)

### metricgenerator.py

**Path: hermes/modules/metricgenerator.py**

metricgenerator.py is also built to allow clearer execution of code using the strategy pattern. You have MetricExceutor that executes different types of metrics and change the metrics during runtime.

For example: we want to execute RMSE and then execute PRFS with different vectors.

```bash
exeggutor = MetricExecutor(RMSE())
print exeggutor.execute(vector1)
print exeggutor.execute(vector2)
exeggutor = MetricExecutor(PRFS)
print exeggutor.execute(vector1)
print exeggutor.execute(vector2)
```

MetricFactory() is a class that will automatically instantiate which metric dependent on what is specified in the configuration file.

#### Adding New Metric

To add a new metric, create a class that inherits from the Metric class and define a calculate_metric function in the class.

```bash
class MyCoolNewMetric(Metric):
    def calculate_metric(self, vector):
        # calculate your cool new metric here
        # or
        # define your cool new metric in hermes/metrics/performance_metrics.py
        return metrics.performance_metrics.calculate_my_cool_new_metric(vector.test_vector, vector.prediction_vector)
```

### statemachine.py

**Path: hermes/modules/statemachine.py**

statemachine.py defines the concrete implementation of the state machine. 

Here is how you can use a state machine:
```bash
# state1 -> state2 -> state3a
#                  -> state3b
# where state1, state2, state3a, and state3b are defined functions.

import StateMachine

sm = StateMachine()
sm.add_state(state1)
sm.add_state(state2)
sm.add_state(state3a, isEndState=True)
sm.add_state(state3b, isEndState=True)
sm.set_start(state1)
sm.run()

# or if you have cargo defined, instead of sm.run(), you can do the following:
# sm.run(Cargo())
```

### timer.py

**Path: hermes/modules/timer.py**

timer.py defines a Timer Class where you can use anywhere in the code to time how long a particular function runs.

For example: if you wanted to time how long somefunction() runs, do the following:
```bash
import Timer

with Timer() as t:
    somefunction()
print("somefunction() takes %s seconds or %s milliseconds" % (t.secs, t.msecs))
```
