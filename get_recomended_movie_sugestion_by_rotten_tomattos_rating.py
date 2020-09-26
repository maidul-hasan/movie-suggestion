import requests


def get_similar_movies_dct_for_a_movie(movie_name):
    bse_url = "https://tastedive.com/api/similar"
    query_params = {"q": movie_name, "type": "movies", "limit": 5}
    req_to_tastedive = requests.get(bse_url, params=query_params)
    res_dict = req_to_tastedive.json()
    return res_dict


def get_similar_titles_lst_for_a_movie(movie_name):  # takes the output of get_movies_from_tastedive() as input
    movie_titles_dct = get_similar_movies_dct_for_a_movie(movie_name)
    movie_titles_list = [itm["Name"] for itm in movie_titles_dct['Similar']['Results']]
    return movie_titles_list


def get_related_titles_list_for_a_list_of_movies(list_of_movie_titles):
    related_titles = []
    for movie_title in list_of_movie_titles:
        related_movie_titles_lst = get_similar_titles_lst_for_a_movie(movie_title)
        for movie in related_movie_titles_lst:
            if movie not in related_titles:
                related_titles.append(movie)
    return related_titles


def get_movie_data(movie_title):
    query_params = {"t": movie_title, "r": "json"}
    base_url = "http://www.omdbapi.com/"
    req_data = requests.get(base_url, query_params)
    res = req_data.json()
    return res


def get_movie_rating(res):
    rt_rating = 0
    x = [item['Value'][:2] for item in res['Ratings'] if 'Rotten Tomatoes' in item.values()]
    for item in x:
        rt_rating = int(item)
    return rt_rating


def get_sorted_recommendations(list_of_movies):
    unsorted_movie_list = get_related_titles_list_for_a_list_of_movies(list_of_movies)
    sorted_movie_list = sorted(unsorted_movie_list, key=lambda movie_title:
    get_movie_rating(get_movie_data(movie_title)), reverse=True)
    return sorted_movie_list


get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
