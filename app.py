from flask import Flask, request, jsonify, render_template
import re

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

KEYWORDS = {
    1: ["cutting", "cut"],
    2: ["assembly", "grinding", "grind", "weld", "welding", "assembly and grinding"],
    3: ["straightening", "straighten"],
    4: ["painting", "paint", "booth"],
    5: ["glazing", "glaze", "glass", "vacuum", "lifter"],
    6: ["lock and prep", "lock", "prep", "traveler"]
}

def find_operation(query):
    query_lower = query.lower()

    match = re.search(r'operation\s*#?\s*([1-6])', query_lower)
    if match:
        return int(match.group(1))

    # Multi-word keywords first (longest match wins)
    for op_num in KEYWORDS:
        for kw in sorted(KEYWORDS[op_num], key=len, reverse=True):
            if kw in query_lower:
                return op_num

    # Bare number fallback
    match = re.search(r'\b([1-6])\b', query_lower)
    if match:
        return int(match.group(1))

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({'response': 'Please enter a command.'})

    lower = user_input.lower()

    if any(phrase in lower for phrase in ['top bottleneck', 'top 4', 'worst bottleneck', 'biggest bottleneck']):
        lines = ['TOP BOTTLENECKS — Ranked by Production Time Impact', '']
        for item in TOP_BOTTLENECKS:
            lines.append(f'  #{item["rank"]}  [{item["delay"]}]  {item["operation"]}')
            lines.append(f'      {item["description"]}')
            lines.append('')
        return jsonify({'response': '\n'.join(lines).rstrip()})

    if any(word in lower for word in ['help', 'list', 'operations', '--help', '-h']):
        lines = ['Available operations:', '']
        for k, v in BOTTLENECKS.items():
            lines.append(f'  Operation #{k}: {v["name"]}')
        lines += ['', 'Commands:',
                  '  "top bottlenecks"  — show the 4 biggest production time impacts',
                  '  "help" / "list"    — show this menu',
                  '  "clear"            — reset terminal',
                  '',
                  'Usage: ask about any operation by name or number.',
                  'Example: "bottlenecks for operation 3" or "painting"']
        return jsonify({'response': '\n'.join(lines)})

    if lower in ('clear', 'cls'):
        return jsonify({'response': '__CLEAR__'})

    op_num = find_operation(user_input)

    if op_num:
        op = BOTTLENECKS[op_num]
        bullets = '\n'.join([f'  • {b}' for b in op['bullets']])
        response = f'Operation #{op_num}: {op["name"]}\n\n{bullets}'
        return jsonify({'response': response})

    return jsonify({
        'response': 'Operation not recognized.\nType "help" or "list" to see all available operations.'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
