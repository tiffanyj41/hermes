
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
        self.metric = new_metric

# ================================================================================
# List of metrics
# ================================================================================

class MetricFactory(object):
    def create_obj_metric(self, metric_str):
        which_metric = getattr(sys.modules[__name__], metric_str)
        if not which_metric:
            # cannot find class
            raise ValueError
        else:
            return which_metric()

class Metric:
    def calculate_metric(self, vector=None) : 
        raise NotImplemented

class RMSE(Metric):
    def calculate_metric(self, vector):
        return pm.calculate_rmse(vector.test_vector, vector.prediction_vector)

class MAE(Metric):
    def calculate_metric(self, vector):
        return pm.calculate_mae(vector.test_vector, vector.prediction_vector)
        
class PRFS(Metric):
    pass




