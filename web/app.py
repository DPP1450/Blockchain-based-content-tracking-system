from flask import *
from werkzeug.utils import secure_filename
import os 
import IPFS_API
app = Flask(__name__, template_folder='Templates')
UPLOAD_FOLDER = '/home/server/eth/web/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return redirect(url_for('index',))

@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                filename))
            cid = IPFS_API.Publish(os.path.join(app.config['UPLOAD_FOLDER'],
                                filename))
            print(cid)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)