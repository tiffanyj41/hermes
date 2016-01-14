# ================================================================================
# Background implementation interface
# ================================================================================

class ImplementationInterface(object):
    def make_prediction_with_als(self):
        raise NotImplemented

    def make_prediction_with_cbkmeans(self):
        raise NotImplemented

    def make_prediction_with_useruser(self):
        raise NotImplemented
        
    def make_prediction_with_itemitem(self):
        raise NotImplemented