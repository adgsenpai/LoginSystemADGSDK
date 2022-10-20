#ADGSTUDIOS - server.py

from flask import Flask,render_template,send_from_directory

app = Flask(__name__,template_folder='./pages')

# allows for files to be refreshed in server
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
  return send_from_directory('static',path)

@app.route('/signin')
def signin():
  return render_template('sign-in.html')

@app.route('/signup')
def signup():
  return render_template('sign-up.html')

#running server on port 8000 - you can change the values here
if __name__ == "__main__":
  app.run(host="0.0.0.0",port=8000,debug=True)