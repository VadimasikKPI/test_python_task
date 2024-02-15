from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from db import Database

app = Flask(__name__)
db = Database()

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Test task"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/filter', methods=['GET'])
def filter_data():
    """
    This is the filter endpoint.
    ---
    parameters:
      - name: category
        in: query
        description: Filter by category.
        required: false
        type: string
      - name: gender
        in: query
        description: Filter by gender.
        required: false
        type: string
      - name: birthDate
        in: query
        description: Filter by Date of Birth.
        required: false
        type: string
      - name: age
        in: query
        description: Filter by age.
        required: false
        type: integer
      - name: age_range
        in: query
        description: Filter by age range like 25-30.
        required: false
        type: string
    responses:
      200:
        description: Filtered data.
      200:
        description: Error on server side.
    """
    filters = request.args.to_dict()
    page = int(filters.pop('page', 1))
    limit = int(filters.pop('limit', 10))
    offset = (page - 1) * limit
    data = db.fetch_data(filters, limit=limit, offset=offset)
    response = []
    for row in data:
        entry = {
            "category": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "email": row[3],
            "gender": row[4],
            "birthDate": row[5]
        }
        response.append(entry)

    return jsonify(response)

@app.route('/export', methods=['GET'])
def export_data():
    """
    This is the export endpoint.
    ---
    parameters:
        - name: category
          in: query
          description: Filter by category.
          required: false
          type: string
        - name: gender
          in: query
          description: Filter by gender.
          required: false
          type: string
        - name: dob
          in: query
          description: Filter by Date of Birth.
          required: false
          type: string
        - name: age
          in: query
          description: Filter by age.
          required: false
          type: integer
    responses:
        200:
            description: Export data to CSV according to the specified filters.
    """
    filters = request.args.to_dict()
    filtered_data = db.fetch_dataset(filters)
    fieldnames = ['category', 'firstname', 'lastname', 'email', 'gender', 'birthDate']
    output = ','.join(fieldnames) + '\n'
    for row in filtered_data:
        output += ','.join(str(item) for item in row) + '\n'

    with open('output.csv', 'w') as csvfile:
        csvfile.write(output)
    return "Data exported to output.csv"


if __name__ == '__main__':
    app.run()
