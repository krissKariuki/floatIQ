from flask import Flask,render_template,send_from_directory
from flask_cors import CORS

app=Flask(__name__,template_folder='../html')
CORS(app)

fileMap={
    'app':'floatIQ.html',
    'chart':'chart.html'
}

@app.route('/floatIQ/<file>')
def render (file) :
    return render_template(fileMap[file])

def SFD(dirs):
    for DIR in dirs:
        app.add_url_rule(f'/{DIR}/<path:file>',f'{DIR}_endpoint',view_func=lambda file,directory=DIR:send_from_directory(f'../{directory}',file))
        
SFD(['css','py','js','db','media'])

if __name__=='__main__' :
    app.run(debug=True,host='0.0.0.0',port='5000')