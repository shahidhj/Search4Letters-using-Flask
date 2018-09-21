from flask import Flask,redirect
from vsearchWithDefandAnno import search_for_letters
from flask import render_template
from flask import request,escape
from DBcm import UseDatabase


app = Flask(__name__)


app.config['dbconfig']={'host':'127.0.0.1',
                        'user':'root',
                        'password':'*****',
                        'database':'*****'}


""" def log_request(req :'flask_request',res :str) ->None:
    with open('vSearch.log','a') as log:
        print(req.form,req.remote_addr,req.user_agent,res,file=log,sep='|')"""


def log_request_database(req : 'flask_request',res:str) ->None:
    """Log Details of the web request and results"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
              (phrase,letters,ip,browser_string,results)
              values
              (%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                         req.user_agent.browser,
                         res))                     

    
@app.route('/viewlog')
def view_log() ->'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase,letters,ip,browser_string,results
                  from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ['Phrase','Letters','Remote_Addr','User_Agent','Response']
    return render_template('viewlog.html',
                           the_title = 'View Log',
                           the_row_titles = titles,
                           the_data = contents)


@app.route('/search4',methods=['POST'])
def do_search() ->'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search_for_letters(phrase,letters))
    log_request_database(request,results)    
    return render_template('results.html',the_title = 'Here are your results',
                           the_phrase = phrase,the_letters = letters,
                           the_results = str(search_for_letters(phrase,letters)))
@app.route('/')
@app.route('/entry')
def entry_page() ->'html':
    return render_template('entry.html',the_title ='Welcome to search4letters on the web!')


if __name__ =='__main__':
    app.run(debug=True)
