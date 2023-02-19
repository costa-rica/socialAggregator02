# ![alt text](/images/aggregate-2-48.png) Social Aggregator 


## Description
This application runs a cron scheduler daily to collect social media posts on:
- stackoverflow
- github
- twitter

Then sends a post request in json to your personal website or wherever you want this data.

## Install

### Step 1: clone this repo
`git clone https://github.com/costa-rica/socialAggregator02.git`

### Step 2: create venv and pip install requirements
```
python -m venv social_agg02
source social_agg02/bin/activate
pip install -r requirements.txt
```

### Step 3: edit .ENV in this repo

Using .ENV is pretty new to me. I use the python-dotenv package in pip to use .ENV in my package. It's sort of like a config but it goes inside the pacakge no sensitive information just useful for paths and other environment varable type data. Here is what I have in mine:
```
PROJ_ROOT_PATH = "/Users/nick/Documents/socialAggregator02/"
PROJ_DB_PATH = "/Users/nick/Documents/_databases/socialAggregator02/"
CONFIG_PATH="/Users/nick/Documents/_config_files/"
CONFIG_FILE_NAME="config_sa02.json"
CONFIG_TYPE='local'
```
Explaination for my .ENV items:
PROJ_ROOT_PATH is the path to socialAggregator02 - it's really just for the log files.
PROJ_DB_PATH is the directory where you want the sqlite and df_mirror.pkl files to be created.
CONFIG_PATH is for where to find my config file
CONFIG_TYPE (local, dev, prod). you can see inside the config.py file the differences between each.

### Step 4: make a config.json
Put your config.json file in teh location you set in the .ENV file for `CONFIG_PATH` and make sure you have the same name as you put in `CONFIG_FILE_NAME`. Then here is an example of what mine looks like
you'll need:

```
{
  "API_ENDPOINT_TESTER_URL":"https://endpointtester.dashanddata.com/posts",
	"API_ENDPOINT_TESTER_PASSWORD": "rebirth_of_slick",
	"HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND":10,
	"USE_MIRROR_DF": false,
	"TWITTER_BEARER_TOKEN": "[YOUR TOKEN HERE]",
	"TWITTER_ID": "138768918",
	"TWITTER_USERNAME":"EvryMnRodriguez",
	"STACK_OVERFLOW_ID": "11925053",
	"GITHUB_USERNAME": "costa-rica",
	"GITHUB_TOKEN": "[YOUR TOKEN HERE]",
	"UPDATE_DESTINATION_URL_LOCAL": "http://localhost:5001/posts",
	"UPDATE_DESTINATION_URL": "https://iamnick.info/collect_new_activity"
}
```

** For Twitter bearer token, I think I used <a href="https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a">this article</a>.
** API_ENDPOINT_TESTER_URL and API_ENDPOINT_TESTER_PASSWORD is another application I made that is sort of like a POSTMAN. If you want to use it you're welcome to as well but this should run fine with both these as blank or altogether removed from your config.json.

Destination to send posts
UPDATE_DESTINATION_URL_LOCAL
UPDATE_DESTINATION_URL

There are two methods:
1. Easiest plug and play is to set USE_MIRROR_DF: false and HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND to the number days back you want to send data.
2. Using MIRROR_DF: true creates a df_mirror.pkl file in a database directory set by .ENV and then every time the cron scheulder sends data it adds it to this mirror df. This is supposed to mirror whatever you have on the receiveing end. It's just another way to reduce the amount of data you're sending each time to the receving end.



## More on how to use it

Here is a somewhat formatted version of what is in my post request:
![alt text](/images/socialAgg02_post.png)

Ths post requests contents sent by Social Aggregator include data/payload/dictioanry item called "new_activity". So you'll do something like  `request.get_json().get("new_activity")` to get a list of dictionaries from the database (see models.py for schema). In the above figure you'll see two posts, one from Github and another from Twitter.

If you'd like to see how I use this for go to: https://iamnick.info/ and see my recent activity section.

To edit the time the cron scheduler fires each day go to main.py and see 
`job_collect_socials = scheduler.add_job(social_aggregator,'cron', day='*', hour='06', minute='01', second='05')`
to edit the time.

## :point_right: Feedback greatly appreciated :point_left:
I'd love get feedback on this repo/markdown to make it more user friendly. If you need help or have suggestions I'd be happy help/edit/update. Email me at nrodrig1@gmail.com :smile: