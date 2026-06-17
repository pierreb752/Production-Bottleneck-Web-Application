from flask import Flask, jsonify, render_template

app = Flask(__name__)

BOTTLENECKS = {
    1: {
        "name": "Cutting",
        "bullets": [
            "Difficulty locating the correct metal stock can increase production time by up to twenty minutes due to material disorganization and scrap accumulation."
        ]
    },
    2: {
        "name": "Assembly and Grinding",
        "bullets": [
            "Locating the cut pieces for a specific project can take up to ten minutes of production time.",
            "Inexperienced welders require a much longer time to complete a frame weld compared to an experienced welder."
        ]
    },
    3: {
        "name": "Straightening",
        "bullets": [
            "The current straightening process (impacting a corner of the frame against the floor) frequently results in weld failures. If a weld fails, the product must be returned to the assembly stage for rework. This can create production delays of up to two hours."
        ]
    },
    4: {
        "name": "Painting",
        "bullets": [
            "The paint booth is not compartmentalized, allowing only one paint type to be applied during a production cycle. This results in underutilized booth capacity for specialized orders and requires additional paint cycles which can take up to two hours."
        ]
    },
    5: {
        "name": "Glazing",
        "bullets": [
            "The vacuum glass lifter occasionally malfunctions, resulting in broken glass and production delays of up to thirty minutes.",
            "Manual handling of large workpieces often requires assistance from employees assigned to other workstations. Coordinating personnel and positioning the workpiece can add up to fifteen minutes to the process."
        ]
    },
    6: {
        "name": "Lock and Prep",
        "bullets": [
            "The templated lock locations specified on the traveler frequently contain incorrect dimensions. As a result, lock openings must be re-measured and cut on the production floor, adding up to twenty minutes of additional labor per product."
        ]
    }
}

TOP_BOTTLENECKS = [
    {
        "rank": 1,
        "operation": "Operation #3: Straightening",
        "delay": "Up to 2 hours",
        "description": "The current straightening process (impacting a corner of the frame against the floor) frequently results in weld failures. If a weld fails, the product must be returned to the assembly stage for rework. This can create production delays of up to two hours."
    },
    {
        "rank": 2,
        "operation": "Operation #4: Painting",
        "delay": "Up to 2 hours",
        "description": "The paint booth is not compartmentalized, allowing only one paint type to be applied during a production cycle. This results in underutilized booth capacity for specialized orders and requires additional paint cycles which can take up to two hours."
    },
    {
        "rank": 3,
        "operation": "Operation #1: Cutting",
        "delay": "Up to 20 minutes",
        "description": "Difficulty locating the correct metal stock can increase production time by up to twenty minutes due to material disorganization and scrap accumulation."
    },
    {
        "rank": 4,
        "operation": "Operation #6: Lock and Prep",
        "delay": "Up to 20 minutes",
        "description": "The templated lock locations specified on the traveler frequently contain incorrect dimensions. As a result, lock openings must be re-measured and cut on the production floor, adding up to twenty minutes of additional labor per product."
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/operations')
def list_operations():
    operations = [{"id": op_id, "name": op["name"]} for op_id, op in BOTTLENECKS.items()]
    return jsonify(operations)


@app.route('/api/operations/<int:op_id>')
def get_operation(op_id):
    op = BOTTLENECKS.get(op_id)
    if not op:
        return jsonify({"error": "Operation not found"}), 404
    return jsonify({"id": op_id, "name": op["name"], "bullets": op["bullets"]})


@app.route('/api/top-bottlenecks')
def top_bottlenecks():
    return jsonify(TOP_BOTTLENECKS)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
