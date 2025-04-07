from flask import Flask, send_file, jsonify, request,redirect
from flask_cors import CORS
from flask_caching import Cache
import getInfo,fileDownload,os,re,dotenv



users = {}
dotenv.load_dotenv()

# Retriving ffmpeg path from environment variables
ffmpeg = os.getenv('FFMPEG')

def formatFilename(fname):
    clean_string = re.sub(r'[^A-Za-z0-9. ]+', '', fname)
    return(clean_string)

app = Flask("YtDownloader")
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "*"}},
)
os.chdir("/tmp")

# Configure Flask-Caching
app.config["CACHE_TYPE"] = "simple" 
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  

# Initialize the cache
cache = Cache(app)

@app.route("/")
def home():
    return redirect("https://clipcatcher.vercel.app")

@app.route("/info", methods=["POST"])
@cache.cached(timeout=6000, key_prefix=lambda: request.get_json()["link"])
def info():
    return getInfo.info(request.get_json()["link"],users)

@app.route("/convert", methods=["POST"])
def convert():
    # return download_video_async("file", "fname")
    id = request.get_json()['id']
    itag = request.get_json()['itag']
    return fileDownload.performDownload(id,itag,users)

@app.route("/download/<file_name>")
def download_file(file_name):
    file = os.path.join(os.getcwd(),file_name)
    return send_file(file, as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
