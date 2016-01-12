from modules.vectorgenerator import UserVector, ContentVector
from modules.hermesglobals import Globals

# ================================================================================
# MovieLens
# ================================================================================

# TODO: do we need isSameDataInstance()? can we eliminate it?
class MovieLens(object):
    @classmethod
    def isSameDataInstance(cls, comparisonData):
        return comparisonData.dataname == "movielens"

class MovieLensUserVector(UserVector, MovieLens):
    def ratings(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating))

    def pos_ratings(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, row.rating)).filter(lambda (u, m, r): r > 3)

    def ratings_to_interact(self):
        return self.data.dataframe.map(lambda row: (row.user_id, row.movie_id, -1 if row.rating < 3 else 1))

class MovieLensContentVector(ContentVector, MovieLens):
    def genre(self):
        def get_genre(row):
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
        return self.data.dataframe.map(lambda row: (row.movie_id, get_genre(row)))
