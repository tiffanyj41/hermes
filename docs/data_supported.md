# Datasets Supported

* [Movie Lens](#movielens)
  * [Configuration Files](#movielens-configuration-files)
  * [Vector Transformation for User Vector](#movielens-vector-transformation-for-user-vector)
  * [Vector Transformation for Content Vector](#movielens-vector-transformation-for-content-vector)
* [Wikipedia](#wiki)
  * [Configuration Files](#wiki-configuration-files)
  * [Vector Transformation for User Vector](#wiki-vector-transformation-for-user-vector)
  * [Vector Transformation for Content Vector](#wiki-vector-transformation-for-content-vector)
* [Adding New Datasets](#adding-new-datasets)


Hermes currently supports the following dataset: 

Dataset       | Location
------------- | -------------
MovieLens     | http://grouplens.org/datasets/movielens/
Wikipedia     | https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia

Additional datasets will be added in the future.

If you have datasets not currently supported by Hermes, please follow the instructions in [Adding Additional Datasets](#adding-additional-datasets) section below. 

Before continuing, it might be beneficial if you understand the Hermes's framework by reading this [guide](https://github.com/Lab41/hermes/tree/master/docs/framework.md) first.

## Movie Lens

### Configuration Files
For JSON files derived from Movie Lens data, you need to specify the following:
* In configuration file, specify dataname = movielens
* In configuraiton file that lists all JSON files, specify section as [movielens]

As long as the dataname check matches with the dataname given in the configuration files, Hermes will recognize it as a Movie Lens data. This check can be found in hermes/hermes/modules/vectorgenerator.py under a class function called isSameDataInstance(). What is checked in isSameDataInstance() has to match the dataname exactly. If it did not, Hermes will throw an error message. In this case, dataname has to match "movielens" exactly to recognize that this is a Movie Lens data.

### Vector Transformation for User Vector

You can specify the vector transformation on a user vector by specifying user_vector_transformations as one of the followings:

* *ratings*: This vector transformation transforms the data into the format of [(user_id, movie_id, rating)].
* *pos_ratings*: This vector transformation transforms the data into the format of [(user_id, movie_id, rating)] and filters out only ratings that are greater than 3. Meaning, this vector transformation will list all positive ratings where we assume a rating of 4 or 5 is a positive one.
* *ratings_to_interact*: This vector transformation transforms the data into the format of [(user_id, movie_id, binary_rating)] where binary_rating will return a value of -1 if it has a rating 2 or less and a value of 1 if it has a rating 3 or more. 

### Vector Transformation for Content Vector

You can specify the vector transformation on a content vector by specifying content_vector_transformations as one of the followings:

* *genre*: This vector transformation transforms the data into the format of [(movie_id, [genre_1, genre_2, ..., genre_n])]. Meaning, this vector transformation will list the genres of the movie.

## Wikipedia

### Configuration Files
For JSON files derived from Wikipedia data, you need to specify the following:
* In configuration file, specify dataname = wiki
* In configuration file that lists all JSON files, specify section as [wiki]

As long as the dataname check matches with the dataname given in the configuration files, Hermes will recognize it as a Wikipedia data. This check can be found in hermes/hermes/modules/vectorgenerator.py under a class function called isSameDataInstance(). What is checked in isSameDataInstance() has to match the dataname exactly. If it did not, Hermes will throw an error message. In this case, dataname has to match "wiki" exactly to recognize that this is a Wikipedia data.

#### Vector Transformation for User Vector

You can specify the vector transformation on a user vector by specifying user_vector_transformations as one of the followings:

* *num_edits*: This vector transformation transforms the data into the format of [(user_id, article_id, num_edits)] where num_edits counts the number of items a user modify an article. 
* *any_interact*: This vector transformation transforms the data into the format of [(user_id, article_id, num_interact)] where num_interact shows the interaction the user has with an article. Even if the user edits the article more than once, this vector transformation considers the interaction the user has with the article as one.
* *num_edits_ceil*: This vector trasnformation transforms the data into the format of [(user_id, article_id, num_edits_with_ceiling)] where num_edits counts the number of items a user modify an article and selects the max between num_edits and 5.

#### Vector Transformation for Content Vector 

You can specify the vector transformation on a content vector by specifying content_vector_transformations as one of the followings:

* *glove*: Explanation will be provided once implemented. (TODO: in development)
* *category_map*: Explanation will be provided once implemented. (TODO: in development)


## Adding New Datasets

Currently, adding new dataset will require you to append the logic (see template below) in hermes/hermes/modules/vectorgenerator.py. To make it easier for the user, in the future, every time you add a new dataset, you will need to create a new file. The template for supporting an additional dataset is shown below.

Template: 

```bash
class NewDataset(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.dataname == "new_dataset_dataname_name"

class NewDatasetUserVector(UserVector, NewDataset):
    def user_vector_transformation_1(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating))

    def user_vector_transformation_2(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating)).filter(lambda (u, m, r): r > 3)

    def user_vector_transformation_n(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, -1 if row.rating < 3 else 1))

class NewDatasetContentVector(ContentVector, NewDataset):
    def content_vector_transformation_1(self):
        def internal_helper_function(row):
            return np.array((
                int(row.genre_action),
                int(row.genre_adventure),
                int(row.genre_animation),
            ))
        return self.data.dataframe.map(lambda row: (row.movie_id, internal_helper_function(row)))

```

1. Instantiate a class for your dataset. In this case, it is specified as class NewDataset.
2. Instantiate a User Vector and a Content Vector class for your dataset that inherits from your dataset class and UserVector or Content Vector respectively. In this case, the UserVector for NewDataset is called NewDataSetUserVector, and the ContentVector for NewDataset is called NewDataContentVector. 
3. Provide the dataname name for the check in isSameDataInstance(). In this case, dataname is checked if it's equal to "new_dataset_dataname_name".
4. Provide the vector transformation logic for each type of vectors. For User Vector transformations, define the function in the class NewDatasetUserVector. In this case, these vector transformations are user_vector_transformation_1, user_vector_transformation_2, and user_vector_transformation_n. For Content Vector transformations, define the function in the class NewDatasetContentVector. In this case, the vector transformation is content_vector_trasnformation_1. 
5. Additional support files needed for the vector transformation is passed down from the configuration file as self.support_files. self.support_files is a dictionary with the key as a variable and the value as the value received in the configuration file. Please read on the [configuration file guide](https://github.com/Lab41/hermes/tree/master/docs/configs.md#optional-variables) for more details.

After you have defined the concrete implementation of the new dataset, you can now use the dataset and apply multiple recommender system algorithms and metrics.

In list_of_files.ini:
```bash
[new_dataset_dataname_name]
new_dataset_10m_ratings = /path/to/your/new/dataset/10m/ratings.json.gz
new_dataset_20m_ratings = /path/to/your/new/dataset/20m/ratings.json.gz
new_dataset_10m_ratings_schema = /path/to/your/new/dataset/10m/ratings_schema.json.gz
new_dataset_20m_ratings_schema = /path/to/your/new/dataset/20m/ratings_schema.json.gz

new_dataset_10m_movies = /path/to/your/new/dataset/10m/movies.json.gz
new_dataset_10m_movies_schema = /path/to/your/new/dataset/10m/movies_schema.json.gz
```

In new_dataset_config.ini:
```bash
[datasets]
dataname = new_dataset_dataname_name

# user vector
user_vector_data = ["new_dataset_10m_ratings", "new_dataset_20m_ratings"]
user_vector_schemas = ["new_dataset_10m_ratings_schema", "new_dataset_20m_ratings_schema"]
user_vector_transformations = ["user_vector_transformation_1", "user_vector_transformation_2"]

# content vector
content_vector_data = ["new_dataset_10m_movies"]
content_vector_schema = ["new_dataset_10m_movies_schema"]
content_vector_transformations = ["content_vector_trasnformation_1"]

[recommenders]
user_recommenders = ["ALS"]
content_recommenders = ["CBWithKMeans"]

[metrics]
metrics = ["RMSE", "MAE"]
```

When you run hermes with the above configuration, the following will happen:
* user_vector_transformation_1 will be applied to new_dataset_10m_ratings.
* user_vector_transformation_2 will be applied to new_dataset_20m_ratings.
* content_vector_transformation_1 will be applied to new_dataset_10m_movies.
* ALS will be applied to UserVector of new_dataset_10m_ratings.
* ALS will be applied to UserVector of new_dataset_20m_ratings.
* CBWithKMeans will be applied to ContentVector of new_dataset_10m_movies.
* RMSE will be applied to UserVector of new_dataset_10m_ratings after ALS has been subjected to it.
* RMSE will be applied to UserVector of new_dataset_20m_ratings after ALS has been subjected to it.
* RMSE will be applied to ContentVector of new_dataset_10m_ratings after CBWithKMeans has been subjected to it.
* MAE will be applied to UserVector of new_dataset_10m_ratings after ALS has been subjected to it.
* MAE will be applied to UserVector of new_dataset_20m_ratings after ALS has been subjected to it.
* MAE will be applied to ContentVector of new_dataset_10m_ratings after CBWithKMeans has been subjected to it.
