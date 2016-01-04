# Hermes's Configuration Files Explained

* [List of Files Standard](#list-of-files-standard)
  * [Dataname](#dataname)
  * [JSON Paths](#json-paths)
* [Configuration File Standard](#configuration-file-standard)
  * [Datasets](#datasets)
    * [Dataname](#dataname)
    * [Vectors](#vectors)    
    * [Optional Variables: Schemas & Support Files](#optional-variables)
* [Recommenders](#recommenders)
* [Metrics](#metrics)

Hermes requires at least two configuration files:
* **list_of_files_config**: A configuration file that lists all the json paths referenced by configs.
* **configs**: Users can provide an unlimited amount of configuration files that list what datasets to use and which recommender algorithms and metrics to apply to each dataset.

Each configuration file requires it to follow a certain standard. These standards will be further explained below.

Saved configuration files can be found in hermes/hermes/configs in case you want to run a previously saved configuration.

Before continuing, it might be beneficial if you understand the Hermes's framework by reading this [guide](https://github.com/Lab41/hermes/tree/master/docs/framework.md) first.

## List of Files Standard

Let's take a look at an example file called list_of_files.ini.

```bash
[movielens] 
# 20M data
movielens_20m_ratings = /path/to/your/movielens/20m/ratings.json.gz
movielens_20m_tags = /path/to/your/movielens/20m/tags.json.gz
movielens_20m_movies = /path/to/your/movielens/20m/movies.json.gz

# 10M data
movielens_10m_ratings = /path/to/your/movielens/10m/ratings.json.gz
movielens_10m_tags = /path/to/your/movielens/10m/tags.json.gz
movielens_10m_movies = /path/to/your/movielens/10m/movies.json.gz

# 1M data
movielens_1m_ratings = /path/to/your/movielens/1m/ratings.json.gz
movielens_1m_tags = /path/to/your/movielens/1m/tags.json.gz
movielens_1m_movies = /path/to/your/movielens/1m/movies.json.gz

# 20M schema
movielens_20m_ratings_schema = /path/to/your/movielens/20m/ratings_schema.json.gz
movielens_20m_tags_schema = /path/to/your/movielens/20m/tags_schema.json.gz
movielens_20m_movies_schema = /path/to/your/movielens/20m/movies_schema.json.gz

# 10M schema
movielens_10m_ratings_schema = /path/to/your/movielens/10m/ratings_schema.json.gz
movielens_10m_tags_schema = /path/to/your/movielens/10m/tags_schema.json.gz
movielens_10m_movies_schema = /path/to/your/movielens/10m/movies_schema.json.gz

# 1M schema
movielens_1m_ratings_schema = /path/to/your/movielens/1m/ratings_schema.json.gz
movielens_1m_tags_schema = /path/to/your/movielens/1m/tags.json_schema.gz
movielens_1m_movies_schema = /path/to/your/movielens/1m/movies_schema.json.gz
```

### Dataname

A single data can be split into multiple JSON files. In this case, [movielens] is a data that is split into multiple JSON files. For lack of a better term, we call [movielens] a "dataname" variable. There can be multiple datanames in a list of files (ie. list_of_files.ini), but there can only be one dataname in a configuration file (ie. config.ini). 

Dataname plays an important role in that we know which data each JSON file is coming from. This check can be found in hermes/hermes/modules/vectorgenerator.py under a class function called isSameDataInstance() for each data instantiated class. What is checked in isSameDataInstance() has to match the dataname exactly. If it did not, Hermes will throw an error message. 

For example, in the case of the Movie Lens data, its dataname is "movielens". The check in the class MovieLens's isSameDataInstance() function will check that dataname is equal to "movielens". If you passed [MovieLens] to list_of_files.ini, for example, and the check in isSameDataInstance() is "movielens", it will fail. However, if you passed [movielens] to list_of_files.ini and the check in isSameDataInstance() is "movielens", it will pass.  

### JSON Paths

Underneath the dataname heading, each variable (ie. movielens_20m_ratings, movielens_20m_tags, etc.) is a shorthand name for a specific JSON file. These variables will store the path to their individual JSON file. They will be used in the configuration file (ie. config.ini) as input to user_vector_data and content_vector_data variable. 

## Configuration File Standard

**If you wanted to know what data is currently supported by Hermes and the different ways you can parse the data (and how you can add your own data not yet supported), please checkout [List of Data Supported](https://github.com/Lab41/hermes/tree/master/docs/data_supported.md) guide.**

**If you wanted to know what types of recommender system algorithms currently supported by Hermes (and how you can add different algorithms not yet supported), please check out [List of Recommender Systems Supported](https://github.com/Lab41/hermes/tree/master/docs/recommenders_supported.md) guide.**

**If you wanted to know what types of metrics currently supported by Hermes (and how you can add different metrics not yet supported), please check out [List of Metrics Supported](https://github.com/Lab41/hermes/tree/master/docs/metrics_supported.md) guide.** 

Let's take a look at an example file called config.ini.

```bash
[datasets]
dataname = movielens

# user vector
user_vector_data = ["movielens_10m_ratings", "movielens_20m_ratings"]
user_vector_schemas = ["movielens_10m_ratings_schema", "movielens_20m_ratings_schema"]
user_vector_transformations = ["ratings", "ratings_to_interact"]

# content vector
content_vector_data = ["movielens_10m_movies"]
content_vector_schema = ["movielens_10m_movies_schema"]
content_vector_transformations = ["genre"]

[recommenders]
user_recommenders = ["ALS"]
content_recommenders = ["CBWithKMeans"]

[metrics]
metrics = ["RMSE", "MAE"]
```

### Datasets

Datasets specify which data we are going to use. It contains dataname, user or content vectors, and support files.

#### Dataname  

One configuration file can specify only one dataname. Dataname is the name of the data where each JSON file is derived from. 

#### Vectors

Vector is the transformed data that will be subjected to the recommender system algorithms and metrics. 

Understanding how a vector is created will provide an understanding of what a vector is. To create a vector, the steps are as follow:

1. Read the configuration files to know what type of vectors we are creating.
2. Read each JSON file to obtain the data. The output of this step is the creation of a dataframe.
3. Once you have this dataframe, you can subject it to a transformation specified by the vector transformation. For example: if we wanted to create a user vector from the JSON file "movielens_10m_ratings" of vector tranformation "ratings" as specified by config.ini above, the data from the JSON file "movielens_10m_ratings" is transformed into a RDD of [(user_id, movie_id, rating)] because vector transformation "rating" converts MovieLens data into [(user_id, movie_id, rating)]. Different vector transformation will implement different transformation of the data. For vector transformation "ratings_to_interact", it will convert MovieLens data into [(user_id, movie_id, just_rating_greater_than_3)].

To wrap it up, vector refers to a dataframe that has been converted to a RDD after a transformation occurs. This transformation is specified by the vector tranformation.

There are two types of vectors currently implemented: User Vector and Content Vector. User Vector refers to the vector describing users in the data. Content Vector refers to the vector describing the content in the data.

Each vector requires the following to be specified in the configuration file:
* **user_vector_data** / **content_vector_data**: Vector data takes in a list of JSON names that reference the JSON path as specified in the list of files config (ie. list_of_files.ini). user_vector_data will create a User Vector; content_vector_data will create a Content Vector.
* **user_vector_transformations** / **content_vector_transformations**: user_vector_transformations and content_vector_transformations will take in a list of transformations to apply to user_vector_data and content_vector_data respectively. Note that user_vector_data and user_vector_transformations (as well as content_vector_data and content_vector_transformations) have a one-on-one relationship, meaning vector transformation at index 0 will be applied to vector data at index 0, vector transformation at index 1 will be applied to vector data at index 1, and vector transformation at index n will be applied to vector data at index n. Currently, Hermes does not have the ability to apply multiple transformations onto one vector data unless the vector data is specified multiple times in user_vector_data / content_vector_data with its respective vector transformation. 

#### Optional Variables: Schemas & Support Files

Each vector can specify optional variables that can assist in process speed or vector transformation:
* **user_vector_schemas** / **content_vector_schemas**: Specifying a schema for each data can speed up the reading process of the JSON file. Again, user_vector_schemas and content_vector_schemas have a one-to-one relationship with user_vector_data and content_vector_data respectively, meaning user_vector_schemas at index 0 applies to user_vector_data at index 0; content_vector_schemas at index 0 applies to content_vector_data at index 0. 
* **support_files**: Additional variables listed in the [datasets] section will be treated as support files. During the creation of a Vector, these support files will be passed in as a dictionary with the key as a variable and the value as the value received. Currently, it cannot take a list of values as its value. For example: if glove_model = /data/glove/glove.txt is an additional line listed under the [datasets] section, it will be passed in as a dictionary with glove_model as key and /data/glove/glove.txt as its value.

### Recommenders

user_recommenders take in a list of recommender algorithms that will be applied to all user_vector_data.

content_recommenders take in a list of recommender algorithms that will be applied to all content_vector_data.

### Metrics

metrics take in a list of metrics that will be applied to all data, including both user_vector_data and content_vector_data, after recommender algorithms have been applied to them.





































































































