import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

def get_profile_image_url(username: str) -> str | None:
    """Return the user's Twitter profile image URL (if available).
    Accepts a raw username or a full twitter/x URL.
    """
    if not username:
        return None

    # Normalize from URL to username, if needed
    if username.startswith("https://"):
        import re
        m = re.search(r'(?:twitter\.com|x\.com)/([A-Za-z0-9_]{1,15})', username)
        if m:
            username = m.group(1)
        else:
            return None

    import re
    if not re.match(r'^[A-Za-z0-9_]{1,15}$', username):
        return None

    try:
        resp = twitter_client.get_user(username=username, user_fields=["profile_image_url"])
        if resp and resp.data and getattr(resp.data, "profile_image_url", None):
            # Return the higher-res version when possible
            url = resp.data.profile_image_url or None
            if url and "_normal" in url:
                url = url.replace("_normal", "_400x400")
            return url
    except Exception:
        return None

    return None

def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    if not username:
        print("❌ No username provided")
        return []
    
    # Clean up username - remove URL parts if present
    if username.startswith("https://"):
        import re
        match = re.search(r'(?:twitter\.com|x\.com)/([A-Za-z0-9_]{1,15})', username)
        if match:
            username = match.group(1)
        else:
            print(f"❌ Could not extract username from URL: {username}")
            return []
    
    # Validate username format
    import re
    if not re.match(r'^[A-Za-z0-9_]{1,15}$', username):
        print(f"❌ Invalid Twitter username format: {username}")
        return []
    
    try:
        print(f"Attempting to scrape tweets for username: @{username}")
        
        # Get user information first
        user_response = twitter_client.get_user(username=username)
        if not user_response.data:
            print(f"❌ User @{username} not found")
            return []
            
        user_id = user_response.data.id
        print(f"✅ Found user ID: {user_id} for @{username}")
        
        # Get user's tweets
        tweets_response = twitter_client.get_users_tweets(
            id=user_id, 
            max_results=min(num_tweets, 100),  # Twitter API limit
            exclude=["retweets", "replies"],
            tweet_fields=["created_at", "public_metrics"]
        )
        
        if not tweets_response.data:
            print(f"❌ No tweets found for @{username}")
            return []

        tweet_list = []
        for tweet in tweets_response.data:
            tweet_dict = {
                "text": tweet.text,
                "url": f"https://twitter.com/{username}/status/{tweet.id}",
                "created_at": tweet.created_at.isoformat() if hasattr(tweet, 'created_at') and tweet.created_at else None,
                "retweet_count": tweet.public_metrics.get("retweet_count", 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0,
                "like_count": tweet.public_metrics.get("like_count", 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0,
            }
            tweet_list.append(tweet_dict)

        print(f"✅ Successfully scraped {len(tweet_list)} tweets for @{username}")
        return tweet_list
        
    except tweepy.TooManyRequests:
        print(f"❌ Twitter API rate limit exceeded for @{username}")
        return []
    except tweepy.Unauthorized:
        print(f"❌ Twitter API unauthorized - check your API credentials")
        return []
    except tweepy.NotFound:
        print(f"❌ Twitter user @{username} not found")
        return []
    except Exception as e:
        print(f"❌ Error scraping Twitter for @{username}: {e}")
        return []

    return tweet_list