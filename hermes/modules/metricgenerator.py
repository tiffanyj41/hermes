
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
import algorithms.performance_metrics as pm

"""

eggsecutor = MetricExecutor(RMSE())
print eggsecutor.execute(vector)
eggsecutor.change_metric(PRFS())
print eggsecutor.execute(vector)

"""

# ================================================================================
# Metric Strategy
# ================================================================================

class MetricExecutor:
    def __init__(self, metric):
        self.metric = metric

    def execute(self, vector):
        return self.metric.calculate_metric(vector)

    def change_metric(self, new_metric):
        print "changing metric to %s" % new_metric
        self.metric = new_metric

# ================================================================================
# List of metrics
# ================================================================================

class MetricFactory(object):
    def create_obj_metric(self, metric_str):
        which_metric = getattr(sys.modules[__name__], metric_str)
        print "which_metric: ", which_metric
        if not which_metric:
            # cannot find class
            raise ValueError
        else:
            print "calling on which_metric()"
            return which_metric()

class Metric:
    def calculate_metric(self, vector=None) : 
        raise NotImplemented

class RMSE(Metric):
    def calculate_metric(self, vector):
        print "executing RMSE"
        print vector.test_vector.take(5)
        print vector.prediction_vector.take(5)
        return pm.calculate_rmse(vector.test_vector, vector.prediction_vector)

class MAE(Metric):
    def calculate_metric(self, vector):
        print "executing MAE"
        print vector.test_vector.take(5)
        print vector.prediction_vector.take(5)
        return pm.calculate_mae(vector.test_vector, vector.prediction_vector)
        
class PRFS(Metric):
    pass




