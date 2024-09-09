from flask import Flask, render_template
import sub
import user_data

app = Flask(__name__)


@app.route('/')
def index():
    user_data_ = user_data.show_user_data()
    links = user_data.show_links_info()
    sale_stats = sub.get_sale_stats()
    return render_template('index.html', users=user_data_, links=links, sale_stats=sale_stats)


if __name__ == '__main__':
    app.run(debug=True)
