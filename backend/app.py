from flask import Flask, request, jsonify
from flask_cors import CORS
from run_analyzer import run_analysis

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    site = data.get('site', 'https://www.viteyes.com')
    sitemap = data.get('sitemap', 'https://www.viteyes.com/page-sitemap.xml')
    
    result = run_analysis(site, sitemap)
    return result, 200

if __name__ == '__main__':
    # Change port from 80 to 5000 so that it matches docker-compose.yml mapping
    app.run(host='0.0.0.0', port=5000)
