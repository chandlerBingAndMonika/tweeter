import requests
import json

def save_user_tweets_to_file(bearer_token: str, user_id: str, max_results: int = 10, output_file: str = "tweets.json"):
    """
    מוריד ציוצים של משתמש ושומר לקובץ JSON את כל המידע האפשרי לפי גישת API רגילה.
    """
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    # שדות שניתן לבקש ב-Twitter API v2 - גישת Basic
    tweet_fields = [
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "geo",
        "id",
        "in_reply_to_user_id",
        "lang",
        "public_metrics",
        "possibly_sensitive",
        "referenced_tweets",
        "reply_settings",
        "source",
        "text",
        "withheld"
    ]

    params = {
        "max_results": max_results,
        "tweet.fields": ",".join(tweet_fields)
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} - {response.text}")

    data = response.json()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(data.get('data', []))} tweets to '{output_file}'.")

# 🧪 דוגמה לשימוש:
if __name__ == "__main__":
    bearer = "AAAAAAAAAAAAAAAAAAAAACfH3QEAAAAAqNrCg8F3TTyI8cM1%2BdFi3zd%2FA%2BE%3DFAOsTeMniuhoUxaezzRULDdDRqguQrmYDugeA1IjKhVB5epNDT"
    user_id = "1786136347163443200"  
    save_user_tweets_to_file(bearer, user_id)





