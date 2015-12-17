# Metrics Supported

* [RMSE](#rmse)
* [MAE](#mae)
* [PRFS](#prfs)
* [Adding New Metric](#adding-new-metric)

This excerpt is taken out from [Understanding Hermes's Framework](https://github.com/Lab41/hermes/tree/master/docs/framework.md#metricgeneratorpy). It will be helpful if you read this guide first.

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

## RMSE

Explanation of what RMSE does will be provided in the future. (TODO)

## MAE

Explanation of what MAE does will be provided in the future. (TODO)

## PRFS

Explanation of what PRFS does will be provided in the future. (TODO)


#### Adding New Metric

This excerpt is taken out from [Understanding Hermes's Framework](https://github.com/Lab41/hermes/tree/master/docs/framework.md#adding-new-metric).

To add a new metric, create a class that inherits from the Metric class and define a calculate_metric function in the class.

```bash
class MyCoolNewMetric(Metric):
    def calculate_metric(self, vector):
        # calculate your cool new metric here
        # or
        # define your cool new metric in hermes/metrics/performance_metrics.py
        return metrics.performance_metrics.calculate_my_cool_new_metric(vector.test_vector, vector.prediction_vector)
```