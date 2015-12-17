# Recommender Algorithms Supported

* [ALS](#als)
  * [Use Cases Supported](#use-cases-supported)
* [Content Base with K-Means](#content-base-with-k-means)
  * [Use Cases Supported](#use-cases-supported-1)
* [Adding New Recommender System Algorithms](#adding-new-recommender-system-algorithms)

This excerpt is taken out from [Understanding Hermes's Framework](https://github.com/Lab41/hermes/tree/master/docs/framework.md#recommendergeneratorpy). It will be helpful if you read this guide first.

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

## ALS

Explanation of what ALS does will be provided in the future. (TODO)

### Use Cases Supported

* Normal Use Case

## Content Base with K-Means 

Explanation of what Content Base with K-Means will be provided in the future. (TODO)

### Use Cases Supported

* Normal Use Case

#### Adding New Recommender System Algorithms

This excerpt is taken out from [Understanding Hermes's Framework](https://github.com/Lab41/hermes/tree/master/docs/framework.md#adding-new-recommender-system-algorithms).

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