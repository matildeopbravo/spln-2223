import newspaper
import traceback
import sys

url = "https://www.jn.pt"
jn = newspaper.build(url)
xml_file = open("jn.xml", "w")
xml_file.write("<articles>\n")

print("Number of articles :", jn.size())

for article in jn.articles:
    print(article.url)
    ar = newspaper.Article(article.url)
    print(f"Downloading...")
    ar.download()
    ar.parse()
    try:
        xml_file.write(
            f"""<article>
                    <title>{ar.title}</title>
                    <url>{ar.url}</url>
                    <author>{ar.authors}</author>
                    <date>{ar.publish_date}</date>
                    <text>{ar.text}</text>
                </article>
        """
        )
    except Exception:
        continue

xml_file.write("<articles>")
xml_file.close()
