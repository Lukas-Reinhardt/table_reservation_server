from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    seat_data = pd.read_csv('data/seats.csv').to_dict(orient='records')
    table_html = '<table>'
    table_html += '<tr><th>Seat #</th><th>Status</th><th>Name</th><th>Reserve</th></tr>'
    for seat in seat_data:
        status = 'green' if seat['status'] == 'available' else 'red'
        name = seat['name'] if seat['name'] else ''
        reserve_button = f'<button class="reserve-btn" data-seat="{seat["number"]}">Reserve</button>'
        table_html += f'<tr><td>{seat["number"]}</td><td><div class="status {status}"></div></td><td><div class="name">{name}</div></td><td>{reserve_button}</td></tr>'
    table_html += '</table>'
    return render_template('index.html', table_html=table_html)


@app.route('/reserve', methods=['POST'])
def reserve():
    seat_data = pd.read_csv('data/seats.csv')
    seat_number = int(request.form['seat'])
    name = request.form['name']
    seat_data.loc[seat_data['number'] == seat_number, 'status'] = 'reserved'
    seat_data.loc[seat_data['number'] == seat_number, 'name'] = name
    seat_data.to_csv('data/seats.csv', index=False)
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run()
