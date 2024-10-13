from application import app, db
from flask import jsonify, request


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/getmsg/", methods=["GET"])
def respond():
    name = request.args.get("name", None)
    print(f"got name {name}")

    response = {}

    if not name:
        response["ERROR"] = "no name found, please send a name."
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    else:
        response["MESSAGE"] = f"Welcome {name} to the academy!"

    return jsonify(response)


@app.route("/post/", methods=["POST"])
def post_something():
    param = request.form.get("name")
    print(param)
    if param:
        return jsonify(
            {
                "Message": f"Welcome {param} to our awesome platform!!",
                "METHOD": "POST",
            }
        )
    else:
        return jsonify({"ERROR": "no name found, please send a name."})


if __name__ == "__main__":
    app.run(port=5000, threaded=True)
