# simple file uploader and downloader service

import os
import urllib
import cgi
from flask import Flask, request, redirect, url_for, send_from_directory
from secure_file import secure_filename

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

BASE_DIR = os.path.dirname(__file__)

print ("dir:%s" % BASE_DIR)

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt','jpg','pdf','apk','ppt','doc','png','img','tgz','zip','tar','bz2'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def list_directory(path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            return "No permission to list directory"
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(path))
        f.write("<body><h2>Directory listing for %s</h2>" % displaypath)
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")

        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="uploads/%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        #self.send_response(200)
        #self.send_header("Content-type", "text/html")
        #self.send_header("Content-Length", str(length))
        #self.end_headers()
        return f


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(BASE_DIR, UPLOAD_FOLDER)
    return send_from_directory(directory=uploads, filename=filename)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('filename:%s' % file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    %s
    """ % "<br>".join(list_directory(app.config['UPLOAD_FOLDER']))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
