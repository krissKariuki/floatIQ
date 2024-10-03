from flask import Flask,render_template,send_from_directory
from flask_cors import CORS

app=Flask(__name__,template_folder='../html')
CORS(app)

@app.route('/floatIQ/app')
def render () :
    return render_template('index_1.0.html')

def SFD(dirs):
    for DIR in dirs:
        app.add_url_rule(f'/{DIR}/<path:file>',f'{DIR}_endpoint',view_func=lambda file,directory=DIR:send_from_directory(f'../{directory}',file))
        
SFD(['css','py','js','db','media'])

if __name__=='__main__' :
    app.run(debug=True,host='0.0.0.0',port='5000')