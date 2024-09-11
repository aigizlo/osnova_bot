from flask import Flask, render_template
# -*- coding: utf-8 -*-
import sub
import user_data

app = Flask(__name__)


@app.route('/')
def index():
    user_data_ = user_data.show_user_data()
    links = user_data.show_links_info()
    sale_stats = sub.get_sale_stats()
    sale_paracents = sub.sale_paracent(sale_stats)
    count = user_data.all_users()
    return render_template('index.html', users=user_data_, links=links, sale_stats=sale_stats, sale_paracents = sale_paracents, count = count)


if __name__ == '__main__':
    app.run(debug=True)
