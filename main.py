import flask,os
app = Flask(__name__)
@app.route('/')
def main():
    return "Marko"
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))