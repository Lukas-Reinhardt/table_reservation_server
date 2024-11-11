from flask import Flask, render_template, jsonify, request
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def index():
    # Read seat data from CSV file and convert it to a list of dictionaries
    seat_data = pd.read_csv('data/seats.csv').to_dict(orient='records')
    
    # Generate an HTML table for the seat data
    table_html = '<table>'
    table_html += '<tr><th>Seat #</th><th>Status</th><th>Name</th><th>Reserve</th></tr>'
    for seat in seat_data:
        # Determine seat status (green for available, red for reserved)
        status = 'green' if seat['status'] == 'available' else 'red'
        # Get the name of the person who reserved the seat (if any)
        name = seat['name'] if seat['name'] else ''
        # Create a button for reserving the seat
        reserve_button = f'<button class="reserve-btn" data-seat="{seat["number"]}">Reserve</button>'
        # Add a row to the HTML table
        table_html += f'<tr><td>{seat["number"]}</td><td><div class="status {status}"></div></td><td><div class="name">{name}</div></td><td>{reserve_button}</td></tr>'
    table_html += '</table>'
    
    # Render the 'index.html' template and pass the table HTML
    return render_template('index.html', table_html=table_html)

# Define the route for reserving a seat
@app.route('/reserve', methods=['POST'])
def reserve():
    # Read the CSV file with seat data
    seat_data = pd.read_csv('data/seats.csv')
    # Get the seat number and name from the request data
    seat_number = int(request.form['seat'])
    name = request.form['name']
    # Update the seat status and name in the CSV data
    seat_data.loc[seat_data['number'] == seat_number, 'status'] = 'reserved'
    seat_data.loc[seat_data['number'] == seat_number, 'name'] = name
    # Save the updated data back to the CSV file
    seat_data.to_csv('data/seats.csv', index=False)
    # Return a success response as JSON
    return jsonify({'status': 'success'})

# Run the Flask app
if __name__ == '__main__':
    app.run()