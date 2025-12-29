import pytest

from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.repository import RepositoryException
from tests.conftest import in_memory_repo
import unittest


def test_repository_can_set_podcasts(in_memory_repo):
    # checking we have same amount as test csv file
    podcasts = in_memory_repo.get_podcasts()
    assert len(podcasts) == 11

    # initialise some author object to create podcast for testing
    author = Author(1, "Audioboom")
    podcast1 = Podcast(101, author, "Zebra Podcast", "image_url", "Description", "website", 111111, "English")
    podcast2 = Podcast(102, author, "Apple Podcast", "image_url", "Description", "website", 222222, "English")
    podcast3 = Podcast(103, author, "Banana Podcast", "image_url", "Description", "website", 333333, "English")
    in_memory_repo.set_podcasts([podcast1, podcast2, podcast3])
    podcasts = in_memory_repo.get_podcasts()

    #  check that the podcast is in repo
    assert len(podcasts) == 3
    assert podcasts == [podcast1, podcast2, podcast3]


def test_repository_can_add_podcast(in_memory_repo):
    author = Author(1, "Audioboom")  # initialise author object for podcast
    podcast = Podcast(100, author, "AHDB",
                      "http://is4.mzstatic.com/image/thumb/Music128/v4/90/67/ac/9067ac95-5513-7f85-8089-0928976e4fae/source/600x600bb.jpg",
                      "Our purpose is to inspire our farmers, growers and industry to succeed in a rapidly changing world. We equip the"
                      " industry with easy to use, practical know-how which they can apply straight away to make better decisions and improve their"
                      " performance. AHDB is a statutory levy board and is funded by farmers, growers and others in the supply chain.",
                      "https://audioboom.com/channels/4937761",
                      1324104670, "English")
    c1 = Category(0, 'Government & Organizations')
    c2 = Category(1, 'Natural Sciences')
    c3 = Category(2, 'Science & Medicine')
    c4 = Category(3, 'National')
    c5 = Category(4, 'Business')
    podcast.add_category(c1)
    podcast.add_category(c2)
    podcast.add_category(c3)
    podcast.add_category(c4)
    podcast.add_category(c5)
    # Above is all to create an identical podcast with all info as the one in test csv

    # Added and Check that it is that podcast
    in_memory_repo.add_podcast(podcast)
    assert in_memory_repo.get_podcast(100) is podcast


def test_repository_can_get_podcast(in_memory_repo):
    author = Author(1, "Audioboom")  # initialise author for podcast object
    podcast = Podcast(100, author, "AHDB",
                      "http://is4.mzstatic.com/image/thumb/Music128/v4/90/67/ac/9067ac95-5513-7f85-8089-0928976e4fae/source/600x600bb.jpg",
                      "Description", "https://audioboom.com/channels/4937761", 1324104670, "English")
    in_memory_repo.add_podcast(podcast)

    podcast = in_memory_repo.get_podcast(100)
    # check that the podcast exist and can retrieve info on the podcast
    assert podcast is not None
    assert podcast.id == 100
    assert podcast.title == "AHDB"


def test_can_get_all_podcasts(in_memory_repo):
    # starts with 11 podcast
    podcast = in_memory_repo.get_podcasts()
    assert len(podcast) == 11

    # initialise all appropriate objects
    author = Author(1, "Animals")
    podcast1 = Podcast(101, author, "Zebra Podcast", "image_url", "Description", "website", 111111, "English")
    podcast2 = Podcast(102, author, "Apple Podcast", "image_url", "Description", "website", 222222, "English")
    podcast3 = Podcast(103, author, "Banana Podcast", "image_url", "Description", "website", 333333, "English")
    in_memory_repo.add_podcast(podcast1)
    in_memory_repo.add_podcast(podcast2)
    in_memory_repo.add_podcast(podcast3)

    # added 3 podcast so should be 14 total podcast
    assert len(podcast) == 14

    # check that can retrieve title in repo of those podcast
    assert in_memory_repo.get_podcast(101).title == "Zebra Podcast"
    assert in_memory_repo.get_podcast(102).title == "Apple Podcast"
    assert in_memory_repo.get_podcast(103).title == "Banana Podcast"


def test_repository_can_get_podcasts_by_alphabet(in_memory_repo):
    # initialise all appropriate objects
    author = Author(1, "Audioboom")
    podcast1 = Podcast(101, author, "Zebra Podcast", "image_url", "Description", "website", 111111, "English")
    podcast2 = Podcast(102, author, "Apple Podcast", "image_url", "Description", "website", 222222, "English")
    podcast3 = Podcast(103, author, "Banana Podcast", "image_url", "Description", "website", 333333, "English")

    # set the 3 podcast as all the podcasts in mem repo
    in_memory_repo.set_podcasts([podcast1, podcast2, podcast3])

    # sorted them alphabetically
    sorted_podcasts = in_memory_repo.get_podcasts_by_alphabet(in_memory_repo.get_list_of_podcasts_titles())

    # Check the list sequentially, seeing that it is in the expected order
    assert sorted_podcasts[0].title == "Apple Podcast"
    assert sorted_podcasts[1].title == "Banana Podcast"
    assert sorted_podcasts[2].title == "Zebra Podcast"


def test_repository_can_get_random_podcasts(in_memory_repo):
    # initialise all appropriate objects
    author = Author(1, "Audioboom")
    for i in range(15):
        podcast = Podcast(i, author, f"Podcast {i}", "image_url", "Description", "website", 100000 + i, "English")
        in_memory_repo.add_podcast(podcast)

    random_podcasts = in_memory_repo.get_random_podcasts()
    # check that the limit of podcast is 10
    assert len(random_podcasts) == 10


def test_repository_can_get_episodes_by_date(in_memory_repo):
    # initialise all appropriate objects
    episode1 = Episode(1, 1, "Episode 1", pub_date="2023-08-19 10:00:00+0000")  # 2nd
    episode2 = Episode(2, 2, "Episode 2", pub_date="2023-08-18 09:00:00+0000")  # 1st
    episode3 = Episode(3, 3, "Episode 3", pub_date="2023-08-20 11:00:00+0000")  # 3rd

    # sort the episodes
    sorted_episodes = in_memory_repo.get_episodes_by_date([episode1, episode2, episode3])

    # check that it is sorted by date
    assert sorted_episodes[0].id == 2
    assert sorted_episodes[1].id == 1
    assert sorted_episodes[2].id == 3


def test_get_list_of_podcasts_titles(in_memory_repo):
    list_of_titles = in_memory_repo.get_list_of_podcasts_titles()
    podcasts = in_memory_repo.get_podcasts()
    # 11 podcasts in test csv file
    assert len(list_of_titles) == 11
    # should be in ascending ID order
    assert podcasts[0].title == "D-Hour Radio Network"  # id 1
    assert list_of_titles[0] == "D-Hour Radio Network"
    assert podcasts[1].title == "Brian Denny Radio"  # id 2
    assert list_of_titles[1] == "Brian Denny Radio"


# Method currently not in used so test left incomplete
# def test_update_podcast(in_memory_repo):
#     # get all podcast (11 in total)
#     podcasts = in_memory_repo.get_podcasts()
#     # showing it has these info
#     assert podcasts[0].title == "D-Hour Radio Network"
#     assert podcasts[0].description == ("The D-Hour Radio Network is the home of real entertainment radio and \"THE\" "
#                                       "premiere online radio network. We showcase dynamically dynamite radio shows for "
#                                       "the sole purpose of entertaining your listening ear. Here on the D-hour Show "
#                                       "Radio network we take pride in providing an outlet for Celebrity Artists, "
#                                       "Underground Artists, Indie Artists, Producers, Entertainers, Entrepreneurs, "
#                                       "Internet Stars and future business owners. We discuss topics of all forms and "
#                                       "have a great time while doing so. We play all your favorite hits in the forms "
#                                       "of Celebrity, Indie, Hip Hop, Soul/R&B, Pop, and everything else you want and "
#                                       "consider popular. If you would like yourself and or your music to be showcased "
#                                       "on our radio network submit email requests for music airplay, interviews and "
#                                       "etc.. to:  dhourshow@gmail.com and we will get back to you promptly. Here at "
#                                       "the D-Hour Radio Network we are Family and all of our guests, listeners and "
#                                       "loyal fans are family too.  So tune into the D-Hour Radio Network and join the "
#                                       "Family! ")


# Methods not in use (Not made properly so give wrong results) |  test will be made when method is needed or fixed
# def test_get_podcasts_by_author(in_memory_repo):
#     # initialise author object
#     author = Author(1, "Audioboom")
#     podcasts_by_author = in_memory_repo.get_podcasts_by_author(author)
#     assert len(podcasts_by_author) == 1
#
#
# def test_get_podcasts_by_category(in_memory_repo):
#     # initialise category object
#     category = Category(1, "Technology")
#     podcasts_by_category = in_memory_repo.get_podcasts_by_category(category)
#     # Check that there are only podcast of that category
#     assert len(podcasts_by_category) == 2
#
#
# def test_get_number_of_podcasts_by_author(in_memory_repo):
#     # initialise author object
#     author = Author(1, "Audioboom")
#     count = in_memory_repo.get_number_of_podcasts_by_author(author)
#     assert count == 1


# PHASE 2 TESTING

# test whether adding user to mem repo works
def test_can_add_user(in_memory_repo):
    user = User(1, "name", "password")  # initialise User for mem repo
    in_memory_repo.add_user(user)  # adds user to mem repo
    assert in_memory_repo.get_user("name") == user  # checks whether it exist


# test it can get all playlist
def test_get_playlists(in_memory_repo):
    # no playlist at the start
    assert in_memory_repo.get_playlists() == []
    user1 = User(1, "name", "password")  # initialise User for mem repo
    user2 = User(2, "other", "GoodPass1")
    in_memory_repo.add_user(user1)  # adds user to mem repo
    in_memory_repo.add_user(user2)
    playlist1 = Playlist(1, user1, "title")  # initialise Playlist object
    playlist2 = Playlist(2, user2, "NamedPlaylist")
    in_memory_repo.add_playlist(playlist1)  # Added playlists to the list of playlist in repo
    in_memory_repo.add_playlist(playlist2)
    assert in_memory_repo.get_playlists() == [playlist1, playlist2]  # Checking it returns with all the playlist added


# testing adding a playlist
def test_add_playlist(in_memory_repo):
    user = User(1, "name", "password")  # initialise User for mem repo
    in_memory_repo.add_user(user)  # adds user to mem repo
    playlist = Playlist(1, user, "title")  # initialise Playlist object
    assert in_memory_repo.get_playlists() == []  # Empty playlist list at the start
    in_memory_repo.add_playlist(playlist)
    assert in_memory_repo.get_playlists() != []  # check after adding it is not empty
    assert in_memory_repo.get_playlists() == [playlist]  # Checks that it contains the playlist added
    assert in_memory_repo.get_playlists()[0].title == "title"  # checking title is correct


# Test that playlist can be retrieved with User object
def test_get_playlist_by_user(in_memory_repo):
    user = User(1, "name", "password")  # initialise User for mem repo
    in_memory_repo.add_user(user)  # adds user to mem repo
    playlist = Playlist(1, user, "title")  # initialise Playlist object
    in_memory_repo.add_playlist(playlist)
    user_playlist = in_memory_repo.get_playlist_by_user(user)
    assert user_playlist == playlist  # check if the method retrieved the correct playlist


# Test the retrival on number of episodes in repo
def test_get_number_of_episodes(in_memory_repo):
    # there are currently 20 episodes in repo
    assert in_memory_repo.get_number_of_episodes() == 20
    episode1 = Episode(1, 1, "Episode 1", pub_date="2023-08-19 10:00:00+0000")
    episode2 = Episode(2, 2, "Episode 2", pub_date="2023-08-18 09:00:00+0000")
    episode3 = Episode(3, 3, "Episode 3", pub_date="2023-08-20 11:00:00+0000")
    in_memory_repo.add_episode(episode3)  # Added episodes to test number change
    in_memory_repo.add_episode(episode2)  # Added episodes to test number change
    assert in_memory_repo.get_number_of_episodes() == 22
    in_memory_repo.add_episode(episode1)
    assert in_memory_repo.get_number_of_episodes() == 23  # Checking the change in episodes as it is added


# Testing the playlist can be updated
def test_update_users_playlist(in_memory_repo):
    user = User(1, "name", "password")  # initialise User for mem repo
    in_memory_repo.add_user(user)  # adds user to mem repo
    playlist = Playlist(1, user, "title")  # initialise Playlist object
    in_memory_repo.add_playlist(playlist)
    assert in_memory_repo.get_playlists() == [playlist]  # Check playlist being added
    assert in_memory_repo.get_playlists()[0].list_of_episodes == []  # showing list of episodes is empty at start

    user_playlist = in_memory_repo.get_playlist_by_user(user)
    episode1 = Episode(1, 1, "Episode 1", pub_date="2023-08-19 10:00:00+0000")  # Initialise episodes
    episode2 = Episode(2, 2, "Episode 2", pub_date="2023-08-18 09:00:00+0000")
    episode3 = Episode(3, 3, "Episode 3", pub_date="2023-08-20 11:00:00+0000")
    user_playlist.add_episode(episode1)  # Added episodes to a playlist object
    user_playlist.add_episode(episode2)
    user_playlist.add_episode(episode3)
    in_memory_repo.update_users_playlist(user_playlist)  # Updates playlist
    assert in_memory_repo.get_playlists() == [user_playlist]
    # Checks that it has the episodes that was added to that playlist
    assert in_memory_repo.get_playlists()[0].list_of_episodes == [episode1, episode2, episode3]


# testing retrieval of all reviews in repo
def test_get_reviews(in_memory_repo):
    # starts with no reviews

    assert in_memory_repo.get_reviews() == []  # see that reviews list in repo is empty
    user = User(1, "name", "password")  # initialise User for review object
    user2 = User(2, "other", "BadPass")
    author = Author(1, "Audioboom")  # initialise Author
    podcast1 = Podcast(101, author, "Zebra Podcast", "image_url", "Description", "website", 111111, "English")
    # initialise Podcast for review object
    review1 = Review(1, user, podcast1, 5, "This is okay")
    review2 = Review(2, user2, podcast1, 10, "This is Great")
    in_memory_repo.add_review(review1)
    assert in_memory_repo.get_reviews() == [review1]  # check that review got added
    in_memory_repo.add_review(review2)
    assert in_memory_repo.get_reviews() == [review1, review2]


# testing adding of review to repo
def test_add_review(in_memory_repo):
    # setup some test data
    user = User(1, "name", "password")
    author = Author(888, "tttttttttest")
    podcast = Podcast(6353, author, "Test Podcast", "image_url", "Description", "website", 111111, "English")

    # setup a review
    review = Review(1, user, podcast, 5, "Amazing podcast!")

    # add reviews to podcast
    in_memory_repo.add_podcast(podcast)

    # call add_review
    in_memory_repo.add_review(review)

    # check that the review is in the repo
    assert review in in_memory_repo.get_reviews()
    assert review in podcast.reviews


def test_add_review_key_error_handling(in_memory_repo):
    # setup some test data
    user = User(1, "name", "password")
    author = Author(1314, "testing")
    podcast = Podcast(999, author, "Non-existent Podcast", "image_url", "Description", "website", 999999, "English")
    review = Review(1, user, podcast, 4, "Good podcast!")

    assert in_memory_repo.get_podcast(999) is None  # check that such podcast does not exist in mem_repo
    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_reviews()
    assert len(podcast.reviews) == 0  # Since podcast does not exist it should not be able to be added to reviews


# testing getting reviews from the podcast id
def test_get_reviews_from_podcast(in_memory_repo):
    # setup some test data
    user = User(1, "name", "password")
    author = Author(666, "testMan")
    podcast1 = Podcast(2333, author, "Podcast 1", "image_url", "Description", "website", 111111, "English")
    podcast2 = Podcast(2334, author, "Podcast 2", "image_url", "Description", "website", 222222, "English")

    # setup reviews
    review1 = Review(1, user, podcast1, 5, "Amazing podcast!")
    review2 = Review(2, user, podcast2, 4, "Pretty good!")
    review3 = Review(3, user, podcast1, 3, "Could be better.")

    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)
    in_memory_repo.add_review(review3)

    # get podcast1's reviews
    reviews_for_podcast1 = in_memory_repo.get_reviews_for_podcast(2333)
    assert len(reviews_for_podcast1) == 2  # There should be 2 comments associated with podcast 1
    assert review1 in reviews_for_podcast1
    assert review3 in reviews_for_podcast1

    # get podcast1's reviews
    reviews_for_podcast2 = in_memory_repo.get_reviews_for_podcast(2334)
    assert len(reviews_for_podcast2) == 1  # There should be 1 comments associated with podcast 2
    assert review2 in reviews_for_podcast2

    # get reviews from podcast that does not exist
    reviews_for_non_existent_podcast = in_memory_repo.get_reviews_for_podcast(999)
    assert len(reviews_for_non_existent_podcast) == 0  # return empty list


def test_search_podcast_by_author(in_memory_repo):
    # get list that is filter by the specific search
    filtered_list = in_memory_repo.search_podcast_by_author("Audioboom")
    assert len(filtered_list) == 2  # Checking its correct length (only 2 Audioboom podcast in test files)
    # Checking it is the correct podcast:
    assert filtered_list[0].title == "Crawlspace: True Crime & Mysteries"
    assert filtered_list[1].title == "AHDB"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = in_memory_repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_title(in_memory_repo):
    # get list that is filter by the specific search
    filtered_list = in_memory_repo.search_podcast_by_title("radio")
    assert len(filtered_list) == 3  # 3 podcast that has radio in its title in test CSV files
    # Checking that it is the correct podcasts
    assert filtered_list[0].title == "D-Hour Radio Network"
    assert filtered_list[1].title == "Brian Denny Radio"
    assert filtered_list[2].title == "Onde Road - Radio Popolare"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = in_memory_repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_category(in_memory_repo):
    # get list that is filter by the specific search
    filtered_list = in_memory_repo.search_podcast_by_category("Comedy")
    assert len(filtered_list) == 2  # 2 podcast has Comedy in its categories from test files
    # Checking that it is the correct podcasts
    assert filtered_list[0].title == "Brian Denny Radio"
    assert filtered_list[1].title == "The Mandarian Orange Show"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = in_memory_repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_language(in_memory_repo):
    # get list that is filter by the specific search
    filtered_list = in_memory_repo.search_podcast_by_language("Italian")
    assert len(filtered_list) == 1  # Only 1 Italian podcast
    # Checking it is the right podcast
    assert filtered_list[0].title == "Onde Road - Radio Popolare"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = in_memory_repo.search_podcast_by_author("NotExist")
    assert nothing_list == []