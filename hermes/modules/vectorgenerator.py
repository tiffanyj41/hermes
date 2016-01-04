
# vector generator == rdd generator

# ================================================================================
# Vector Factory
# ================================================================================

class VectorFactory(object):

    def create_vector(self, sqlCtx, data, support_files):
        vector = data.which_vector
        for cls in vector.__subclasses__():
            if cls.isSameDataInstance(data):
                return cls(sqlCtx, data, support_files).vector
            else:
                # cannot find class that builds the data
                raise ValueError

    def create_obj_vector(self, sqlCtx, data, support_files):
        vector = data.which_vector
        for cls in vector.__subclasses__():
            if cls.isSameDataInstance(data):
                return cls(sqlCtx, data, support_files)
            else:
                # cannot find class that builds the data
                raise ValueError

# ================================================================================
# Vector Factory Objects
# ================================================================================

class Vector(object):
    def __init__(self, sqlCtx, data, support_files):
        # TODO: remove sqlCtx because it is global?
        self.sqlCtx = sqlCtx
        self.data = data
        self.support_files = support_files
        vector_transformation = getattr(self, data.vector_transformation)
        if not vector_transformation:
            self.vector = None
        else:
            self.vector = vector_transformation()
        self.training_vector = None
        self.test_vector = None
        self.validation_vector = None
        self.prediction_vector = None

    def split_data(self, weights, seed):
        training_vector, test_vector, validation_vector = self.vector.randomSplit(weights, seed)
        self.training_vector = training_vector
        self.test_vector = test_vector
        self.validation_vector = validation_vector

# ================================================================================
# User Vector and Content Vector Factory Objects
# ================================================================================

class UserVector(Vector):
    pass

class ContentVector(Vector):
    pass

# ================================================================================
# MovieLens
# ================================================================================

# TODO: separate in its own file
# TODO: do we need isSameDataInstance()? can we eliminate it?
class MovieLens(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.vectorizer == "movielens"

class MovieLensUserVector(UserVector, MovieLens):
    def ratings(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating))

    def pos_ratings(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating)).filter(lambda (u, m, r): r > 3)

    def ratings_to_interact(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, -1 if row.rating < 3 else 1))

class MovieLensContentVector(ContentVector, MovieLens):
    def genre(self):
        def genre_vectorizer(row):
            return np.array((
                    int(row.genre_action),
                    int(row.genre_adventure),
                    int(row.genre_animation),
                    int(row.genre_childrens),
                    int(row.genre_comedy),
                    int(row.genre_crime),
                    int(row.genre_documentary),
                    int(row.genre_drama),
                    int(row.genre_fantasy),
                    int(row.genre_filmnoir),
                    int(row.genre_horror),
                    int(row.genre_musical),
                    int(row.genre_mystery),
                    int(row.genre_romance),
                    int(row.genre_scifi),
                    int(row.genre_thriller),
                    int(row.genre_war),
                    int(row.genre_western),
                ))
        return self.data.dataframe.map(lambda row: (row.movie_id, genre_vectorizer(row)))

# ================================================================================
# Wiki
# ================================================================================

# TODO: separate in its own file
class Wiki(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.vectorizer == "wiki"

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

# ================================================================================
# ADD ADDITIONAL UserVector and ContentVector based on a given data
# ================================================================================

