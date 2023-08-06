# Larry Birdy

`Larry Birdy` is based on ['birdy'](https://github.com/inueni/birdy) and
is sentence-oriented (i.e. sprinkled with syntactic sugar).
Through an experimental (and fuzzy oop design) and proof-of-concept way,
you can make API calls with exprensiveness (and verbosity).

### Install
`pip install larry-birdy`

### Example
```python
from larry.twitter import RestAPI, p

API = RestAPI(CONSUMER_KEY,
              CONSUMER_SECRET,
              ACCESS_TOKEN,
              ACCESS_TOKEN_SECRET)
			  
OWNER = API.verify_account_credentials(skip_status=True)

query = '#python #twitter -rt'
tweet_instances = API.search_tweets(q=query,
                                    result_type='recent',
                                    lang='en',
                                    count=10,
                                    tweet_mode='extended')

# You can write "sentences" like the following:

content_has_media = p.Does.this(status=tweet_instance).have_element('media')
                        # Does this [status] have (the) element ['media']?

hashtags_number = p.Find.for_element('hashtags').its_number_within(tweet_instance)
                    # Find, for (the) element ['hashtags'], its number within (this) [status].

mentions = p.Get.element('user_mentions').from_(tweet_instance)
            # Get (the) element ['user_mentions'], from (this) [status].

user = tweet_instance.user
user_is_following_owner = p.Is.this(user).following(OWNER)
                            # Is this [user] following [OWNER]?

try:
    API.retweet(tweet=tweet_instance, trim_user=True)
except Exception as error_message:
    print(error_message)
```
