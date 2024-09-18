import requests
import argparse
import subprocess

def build_search_url(base_url, search_terms):
    url = base_url + "+" + "+".join(search_terms)
    return url

def search_github(search_url, search_in_code=False):
    if search_in_code:
        search_url += "&in:file"

    # Initialize variables for pagination
    all_results = []
    page = 1
    per_page = 100  # Max results per page (GitHub API limit)

    while True:
        # Append pagination parameters to the search URL
        paginated_url = f"{search_url}&page={page}&per_page={per_page}"
        response = requests.get(paginated_url)
        response_json = response.json()

        # Append current page results to the list of all results
        all_results.extend(response_json["items"])

        # Check if there are more pages to fetch
        if len(response_json["items"]) < per_page:
            break  # No more items to fetch

        # Increment page number for next request
        page += 1

    return all_results

def extract_repo_urls(search_results):
    repo_urls = []
    for item in search_results:
        repo_urls.append(item["html_url"])
    return repo_urls
    
def check_for_api_spec(url):
	subprocess.run(["python", "git_search_file.py", url])

def main():
    base_url = "https://api.github.com/search/repositories?q="

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Search GitHub repositories.")
    parser.add_argument("search_terms", nargs="+", help="Search terms")
    parser.add_argument("--code", action="store_true", help="Search in code")
    args = parser.parse_args()

    search_url = build_search_url(base_url, args.search_terms)
    search_results = search_github(search_url, args.code)
    repo_urls = extract_repo_urls(search_results)

    print("Found Repositories:")
    for url in repo_urls:
        print(url)

if __name__ == "__main__":
    main()
