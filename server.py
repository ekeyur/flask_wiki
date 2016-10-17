from flask import Flask, render_template, redirect, request, session, flash
from wiki_linkify import wiki_linkify
import pg, time

app = Flask("My Wiki")
db = pg.DB(dbname='wiki_db')

app.secret_key = 'keyur12345'

# @app.route('/')
# def home():
#     return render_template(
#     'home.html'
#     )

@app.route('/<page_name>')
def page_name(page_name):
    q = db.query("Select * from wiki where title = $1",page_name).namedresult()
    if len(q) < 1:
        db.insert(
            'wiki',{
            'title':page_name,
            'content':page_name,
            'last_date':time.strftime("%Y-%m-%d %H:%M:%S"),
            'last_author': "keyur"
            })
        qu = db.query("Select * from wiki where title = $1",page_name).namedresult()
        query = qu[len(qu)-1]
    else:
        query = q[len(q)-1]

    return render_template(
        'wiki.html',
        page_name = page_name,
        wiki_linkify = wiki_linkify,
        query = query
    )
@app.route('/searchresults', methods=['POST'])
def searchresults():
    sea = request.form.get('search')
    search = "%"+sea+"%"
    query = db.query("Select * from wiki where content like $1",search).namedresult()
    if len(search) < 1:
        return "no results"
    else:
        return render_template(
        'searchresults.html',
        query = query,
        wiki_linkify = wiki_linkify
        )

@app.route('/logout', methods=['POST'])
def logout():
    del session['user']
    return redirect('/')
    flash("You are now logged out.")

@app.route('/login')
def login():
    return render_template(
    'login.html'
    )

@app.route('/submit_login', methods=['POST'])
def submit_login():
    author = request.form.get('author')
    password = request.form.get('password')
    query = db.query("Select * from author where name=$1",author).namedresult()

    print query

    if len(query)>0:
        user = query[0]
        if user.password == password:
            session['user'] = user.name
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/')
def allpages():

    # query_string = "SELECT tt.* from wiki tt inner join(select title as tit, max(last_date) as dat from wiki group by title) as tab on tt.last_date = tab.dat and tt.title = tab.tit"

    query_string = "select tt.* from wiki tt inner join(select title as tit, max(last_date) as dat from wiki group by title) as tab on tt.last_date = tab.dat and tt.title = tab.tit"

    # query_string = "select * from wiki"
    query = db.query(query_string).namedresult()
    return render_template(
    'allpages.html',
    query = query,
    wiki_linkify = wiki_linkify
    )


@app.route('/<page_name>/edit')
def page_name_edit(page_name):
    q = db.query("Select * from wiki where title = $1", page_name).namedresult()
    query = q[len(q)-1]
    print query
    return render_template(
    'edit.html',
    page_name = page_name,
    query = query,
    wiki_linkify = wiki_linkify
    )

@app.route('/<page_name>/save', methods=['POST'])
def page_name_save(page_name):
    content = request.form.get('content')
    title = request.form.get('title')
    # if len(content) < 1:
    db.insert('wiki',{'title':title, 'content':content, 'last_date':time.strftime("%Y-%m-%d %H:%M:%S"),'last_author':'keyur'})
    # else:
    #     db.update('wiki',{'title':title, 'content':content, 'last_date':time.strftime("%Y-%m-%d %H:%M:%S"),'last_author':'keyur'})
    return render_template(
    'save.html',
    content = content,
    title = title,
    wiki_linkify = wiki_linkify
    )





if __name__ == '__main__':
    app.run(debug=True)
