TRACK_WORDS = [""]
TABLE_NAME = ""
TABLE_ATTRIBUTES = "id_str BIGINT(20), created_at DATETIME, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_name VARCHAR(255), user_screen_name VARCHAR(255)," \
            "user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INT, favorite_count INT, lang VARCHAR(250), emotion VARCHAR(250), PRIMARY KEY(id_str)"
