# Assumptions

* [Assumptions on Execution](#assumptions-on-execution)
* [Assumptions on Vector Creation](#assumptions-on-vector-creation)

## Assumptions on Execution

Here is an example file called config.ini.

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

When you specify the following configuration, the assumption that we make during execution is as follows:
* each transformation is applied in sequential order to the data, meaning
  * user_vector_transformation "ratings" is applied to "movielens_10m_ratings" and "movielens_10m_ratings_schema"
  * user_vector_transformation "ratings_to_interact" is applied to "movielens_20m_ratings" and "movielens_20m_ratings_schema"
  * content_vector_transformation "genre" is applied to "movielens_10m_movies" and "movielens10m_movies_schema"
* user_recommenders take in a list of recommender algorithms that will be applied to all user_vector_data, meaning
  * apply ALS to a User Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings"
  * apply ALS to a User Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings_to_interact"
* content_recommenders take in a list of recommender algorithms that will be applied to all content_vector_data, meaning
  * apply CBWithKMeans to a Content Vector of movielens_10m_movies that have been transformed by vector transformation "genre"
* metrics take in a list of metrics that will be applied to all data, including both user_vector_data and content_vector_data, after recommender algorithms have been applied to them, meaning
  * apply RMSE to a User Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings" and recommendation system algorithm ALS
  * apply RMSE to a USer Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings_to_interact" and recommedation systme algorithm ALS
  * apply RMSE to a Content Vector of movielens_10m_movies that have been transformed by vector transformation "genre" and recommendationi system algorithm CBWithKMeans
  * apply MAE to a User Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings" and recommendation system algorithm ALS
  * apply MAE to a USer Vector of movielens_10m_ratings that have been transformed by vector transformation "ratings_to_interact" and recommedation systme algorithm ALS
  * apply MAE to a Content Vector of movielens_10m_movies that have been transformed by vector transformation "genre" and recommendationi system algorithm CBWithKMeans

## Assumptions on Vector Creation

Each dataset is unique in that transforming JSON to RDD is different for each dataset. This step is implemented in vectorgenerator.py. When we separate the implementation of vector generation of each dataset into individual files in the hermes/hermes/modules/vectors directory, each of these files need to import vectorgenerator.py in this specific manner: 

```bash
from hermes.modules.vectorgenerator import UserVector, ContentVector
```

The reason for this is during the instantiation of the vector object in the VectorFactory class. When we specify which vector to create, it is either a UserVector or a ContentVector class; both of which are instantiated in vectorgenerator.py, and vectorgenerator.py as a module is hermes.modules.vectorgenerator. 

Since we can no longer use the __subclasses__() function to iterate through all children of UserVector class or all children of ContentVector class in order to instantiate the right vector because the children are now defined in a separate module in hermes/hermes/modules/vectors directory, we have to load all modules and go through each class in each module to know all children of a UserVector or ContentVector class. Unfortunately, if you defined the import statement as "from modules.vectorgenerator" instead of "from hermes.modules.vectorgenerator", it does not think the two modules are the same even though they are. 

We have yet to determine why this is the case. 

When users add a new dataset, we cannot always assume that they will import exactly as "from hermes.modules.vectorgenerator import UserVector, ContentVector" because they can import it as "from modules.vectorgenerator import UserVector, ContentVector" since it is valid. For this reason, we have made an assumption that if the parent class of the MovieLensUserVector, for example, has the __name__ UserVector, MovieLensUserVector is the child of UserVector. The problem of this assummption is that if MovieLensUserVector inherits multiple parents from different module with the same class name, it can become a problem as it will treat both parents with the same class name as the same. 



