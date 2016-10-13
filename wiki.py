from flask import Flask, render_template
app = Flask("My Wiki")

@app.route('/')
def home():
    return render_template(
    'home.html',
    )
@app.route('/<page_name>')
def page_name(page_name):
    return render_template(
    'placeholder.html',
    page_name = page_name
    )

if __name__ == '__main__':
    app.run(debug=True)
