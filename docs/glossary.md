# Glossary

This is a glossary of common terms used in Hermes and their specified meaning.

## A

## B

## C
**Content Vector**: Content Vector refers to the vector describing the content in the data.

## D
**Dataframe**: A DataFrame is a distributed collection of data organized into named columns. It is conceptually equivalent to a table in a relational database or a data frame in R/Python, but with richer optimizations under the hood. (Excerpt taken from Spark's SQL Programming Guide). In Hermes, the dataframe variable defined in the Data class refers to the dataframe created after reading in the JSON file.

## E

## F

## G

## H

## I

## J

## K

##L

## M

**Metrics**: See "Performance Metrics".

## N

## O

## P

**Performance Metrics**: Performance Metrics allows user to evaluate a recommender and how much a recommender adds value to the end user. 

## Q

## R
**RDD**: Resilient Distributed Dataset or RDD is the basic abstraction in Spark that represents an immutable, partitioned collection of elements that can be operated on in parallel. (Excerpt taken from Spark's man page about RDD).

**Recommender**: See "Recommender System Algorithms".

**Recommender System Algorithms**: Hermes use Recommender System Algorithms to build a model based on the train data and make a prediction based on the test data.

## S

## T
**Tradespace**: It is the space spanned by completely enumerated design variables, which means given a set of design variables, the tradespace is the space of possible design options. (Excerpt taken from Adam M. Ross & Daniel E. Hasting's "The Tradespace Exploration Program")

**Test Data**: Data is usually split into train data, test data, and validation data. After you have used the train data to build a model and validation data to select the best performing model out of all the models, you use test data to estimate the accuracy of the selected approach. In other words, you want to estimate how well your model has been trained. 

**Train Data**: Data is usually split into train data, test data, and validation data. Train data is used by a recommender to build a model by pairing the input with the expected output.


## U
**User Vector**: User Vector refers to the vector describing users in the data. 

## V
**Validation Data**: Data is usually split into train data, test data, and validation data. Validation data is used to select which is the best performing model out of all the models you trained with the train data. Sometimes validation data is optional.

**Vector**: In Hermes, when we referenced a vector, it refers to a dataframe that has been converted to a RDD after a transformation occurs. This transformation is specified by the vector transformation. For example, in the case of a user vector, if the vector transformation is "ratings" for Movie Lens data, the data from the JSON file is transformed into a RDD of [(user_id, item_id, rating)]. The output of this transformation is a vector of [(user_id, item_id, rating)].

**Vector Transformation**: In Hermes, vector transformation refers to the transformation needed to convert data from a JSON file to a specified vector. Please see **Vector** for more details. 

**Vector Type**: Hermes separates vectors into two distinct types: User Vector and Content Vector. User Vector refers to the vector describing users in the data. Content Vector refers to the vector describing content in the data. Users can implement other vector types as needed if User Vector and Content Vector does not describe the vector they are building.

**Vectorizer**: Vectorizer is a variable used in configuration file to refer to the data where each JSON file is coming from. 

## W

## X

## Y

## Z