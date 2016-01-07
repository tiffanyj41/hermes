from hermes.modules.vectorgenerator import UserVector, ContentVector

# ================================================================================
# Wiki
# ================================================================================

class Wiki(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.dataname == "wiki"

class WikiUserVector(UserVector, Wiki):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.filtered = self.sqlCtx.sql("select * from ratings where redirect_target is null and article_namespace=0 and user_id is not null")
        self.filtered.registerTempTable("wiki_ratings")

    def num_edits(self):
        return self.sqlCtx.sql("select user_id as user, article_id as item, count(1) as rating from wiki_ratings group by user_id, article_id")

    def any_interact(self):
        return self.sqlCtx.sql("select user_id as user, article_id as item, 1 as rating from wiki_ratings group by user_id, article_id")

    def num_edits_ceil(self):
        return self.sqlCtx.sql("select user_id as user, article_id as item, count(1) as rating from wiki_ratings group by user_id, article_id")\
             .map(lambda (user, article, rating): (user, article, max(rating, 5)))

class WikiContentVector(ContentVector, Wiki):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.filtered_content = sqlCtx.sqlCtx.sql("select * from content where redirect_target is null and article_namespace=0 and full_text is not null")
        self.filtered_content.registerTempTable("wiki_content")

    def glove(self):
        raise NotImplemented

    def category_map(self):
        raise NotImplemented