from flask import Flask, request, jsonify
import logging
import json
from pyseoanalyzer import analyze
from urllib.parse import urlparse
import requests
from xml.etree import ElementTree

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def extract_urls_from_sitemap(sitemap_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(sitemap_url, headers=headers)
        response.raise_for_status()
        sitemap_content = response.content
        tree = ElementTree.fromstring(sitemap_content)
        urls = [elem.text for elem in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if elem.text]
        return urls
    except Exception as e:
        logger.error(f"Error extracting URLs from sitemap: {str(e)}")
        return []

def run_analysis(site="https://www.viteyes.com", sitemap="https://www.viteyes.com/page-sitemap.xml"):
    try:
        if not (validate_url(site) and validate_url(sitemap)):
            raise ValueError(f"Invalid URL format: {site} or {sitemap}")

        logger.info(f"Starting analysis of site: {site} with sitemap: {sitemap}")

        urls = extract_urls_from_sitemap(sitemap)
        if not urls:
            raise Exception("No URLs found in sitemap")

        pages = []
        for url in urls:
            try:
                head_resp = requests.head(url, allow_redirects=False, headers={"User-Agent": "Mozilla/5.0"})
                if 300 <= head_resp.status_code < 400:
                    logger.error(f"Skipping redirect: {url}")
                    pages.append({"url": url, "error": "Redirect detected"})
                    continue

                result = analyze(url, analyze_headings=True, analyze_extra_tags=True, follow_links=False)
                if result is None:
                    error_msg = "Analysis returned None"
                    logger.error(f"Error analyzing {url}: {error_msg}")
                    pages.append({"url": url, "error": error_msg})
                else:
                    pages.append(result)
            except Exception as e:
                logger.error(f"Error occurred during crawling {url}: {str(e)}")
                pages.append({"url": url, "error": str(e)})

        return json.dumps({"pages": pages, "status": "success"})

    except Exception as e:
        error_data = {
            "error": str(e),
            "status": "failed",
            "pages": [],
            "keywords": [],
            "errors": [str(e)],
            "total_time": 0,
            "duplicate_pages": []
        }
        logger.error(f"Error during analysis: {str(e)}")
        return json.dumps(error_data, indent=2)

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    data = request.get_json()
    site = data.get('site', 'https://www.viteyes.com')
    sitemap = data.get('sitemap', 'https://www.viteyes.com/page-sitemap.xml')
    result = run_analysis(site, sitemap)
    return jsonify(json.loads(result))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)