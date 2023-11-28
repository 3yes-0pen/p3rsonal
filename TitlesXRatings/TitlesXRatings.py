import pandas as pd
import matplotlib.pyplot as plt


na_values = ['\\N']
movie_titles = pd.read_csv('/Users/modelnic/Python/input/title.basics.tsv.imdb', sep = '\t', na_values=na_values)
dropped_cols = ['isAdult', 'startYear', 'endYear', 'originalTitle']
movie_titles = movie_titles.drop(columns=dropped_cols)
movie_titles = movie_titles.assign(genres=movie_titles.genres.str.split(',')).explode('genres')
movie_titles = movie_titles[pd.to_numeric(movie_titles['runtimeMinutes'], errors='coerce').notnull()]
movie_titles.dropna(how='all', inplace=True)
movie_titles = movie_titles.astype({
    'jtconst': str,
    'titleType': 'category',
    'primaryTitle': str,
    'runtimeMinutes': float,
    'genres': 'category'
})
movie_titles.rename(columns={'jtconst': 'tconst'}, inplace=True)
movie_ratings = pd.read_csv('/Users/modelnic/Python/input/title.ratings.tsv.imdb', sep='\t', na_values = na_values)
movie_ratings = movie_ratings.astype({
    'tconst': str,
    'averageRating': float,
    'numVotes': int
})
Moviess = pd.merge(movie_titles, movie_ratings, on='tconst', how='inner')
Moviess['averageRating']=Moviess['averageRating'].round().astype(int)
print(Moviess.head(10))

topFifty = Moviess.sort_values(by=['numVotes','averageRating'], ascending=False)
topFifty = topFifty[topFifty['titleType'] == 'movie'].head(2000)
print(topFifty.head(9))
genre_count = topFifty['genres'].value_counts()
print(genre_count.head(11))
genre_count.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Genres')
plt.ylabel('Count')
plt.title("The popular genres of highly rated films")
plt.show()