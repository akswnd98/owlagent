from langchain_community.utilities.searx_search import SearxSearchWrapper

search = SearxSearchWrapper(
  searx_host="http://localhost:20202",
  unsecure=True,
  headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/108.0.0.0 Safari/537.36"
  },
  
)
print(search.run("current president"))