from flask import Flask, render_template

import sub
import user_data
from links import tracker

app = Flask(__name__)


@app.route('/')
def index():
    user_data_ = user_data.show_user_data()
    links = user_data.show_links_info()
    sale_stats = sub.get_sale_stats()
    dohod = sub.show_total_pribil(sale_stats)
    print(sale_stats, ' sale_stats')
    return render_template('index.html', users=user_data_, links=links, sale_stats=sale_stats, dohod=dohod)


if __name__ == '__main__':
    app.run(debug=True)
# [(502811372, 'Sholcet', 1, Decimal('0.00')), (1139164093, 'sagitow', 1, Decimal('0.00')), (235013345, 'off_radar_support', 0, Decimal('0.00'))]


# [(502811372, 'Sholcet', 1, Decimal('0.00'), 1, datetime.datetime(2024, 9, 5, 16, 8, 29), datetime.datetime(2024, 9, 15, 16, 8, 29)), (1139164093, 'sagitow', 1, Decimal('0.00'), 1, datetime.datetime(2024, 9, 6, 13, 10, 52), datetime.datetime(2024, 10, 6, 13, 10, 53)), (235013345, 'off_radar_support', 0, Decimal('0.00'), None, None, None)]
