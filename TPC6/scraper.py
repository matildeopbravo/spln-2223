import newspaper
import traceback
import datetime
import os
import sys

def create_daily_dir():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    dir_name = f"{articles_dir}/{now}"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def get_curr_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def fetch_articles():
    jn = newspaper.build(url)

    log.write(f"[{get_curr_time()}] Fetched {jn.size()} articles\n")

    for article in jn.articles:
        ar = newspaper.Article(article.url)
        log.write(f"[{get_curr_time()}] Downloading {ar.url}\n")
        ar.download()

        try:
            ar.parse()
            current_file = open(f"{day_dir}/{ar.title}.xml", "w")
            print(f"{day_dir}/{ar.title}.xml")
            current_file.write(
                f"""<article>
                        <title>{ar.title}</title>
                        <url>{ar.url}</url>
                        <author>{ar.authors}</author>
                        <date>{ar.publish_date}</date>
                        <tags> {ar.tags} </tags>
                        <text>{ar.text}</text>
                    </article>
            """)
            log.write(f"[{get_curr_time()}] Saved {ar.url}\n")
            current_file.close()
        except Exception:
            continue


url = "https://www.jn.pt"
articles_dir = f"{sys.argv[1]}/news"
day_dir = create_daily_dir()
log = open(f"{day_dir}/log.txt", "a")
fetch_articles()
log.close()
