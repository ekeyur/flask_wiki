from flask import Flask, render_template, redirect, request
import pg, time

app = Flask("My Wiki")
db = pg.DB(dbname='wiki_db')


@app.route('/')
def home():
    return render_template(
    'home.html'
    )

@app.route('/<page_name>')
def page_name(page_name):
    q = db.query("Select * from wiki where title = '%s'" % page_name)
    print len(q.namedresult())

    if len(q.namedresult()) < 1:
        db.insert(
            'wiki',{
            'title':page_name,
            'content':" "
            })
        query = ""        
    else:
        query = q.namedresult()[0]

    return render_template(
        'wiki.html',
        page_name = page_name,
        query = query
    )


@app.route('/<page_name>/edit')
def page_name_edit(page_name):
    return render_template(
    'edit.html',
    page_name = page_name
    )

@app.route('/<page_name>/save', methods=['POST'])
def page_name_save(page_name):
    content = request.form.get('content')
    title = request.form.get('title')
    db.insert('wiki',{'title':title, 'content':content, 'last_date':time.strftime("%x"),'last_author':'keyur'})
    return redirect('/<page_name>')




if __name__ == '__main__':
    app.run(debug=True)
