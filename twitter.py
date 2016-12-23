import json
import merger
from twython import Twython


def post_to_twitter(filename):
    """
    Posts the actual image to the twitters.
    Requires a keys.json file saved in the same directory, which looks like:
    {
        "app_key": "my_app_key",
        "app_secret": "my_app_secret",
        "oauth_token": "my_oauth_token",
        "oauth_token_secret": "my_oauth_token_secret"
    }
    """

    with open('keys.json') as key_file:
        keys = json.load(key_file)

    #Grabs the connection to twitter
    twitter = Twython(
        keys['app_key'], keys['app_secret'], keys['oauth_token'],
        keys['oauth_token_secret'])

    
    image_open = open(filename, 'rb')
    response = twitter.upload_media(media=image_open)
    twitter.update_status(
        status='Thanks Starbucks', media_ids=[response['media_id']])


if __name__ == '__main__':
    #merger.main()
    post_to_twitter('test_file.jpg')