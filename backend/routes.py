from flask import Blueprint, render_template
from robot import robot

api = Blueprint('api', __name__)

@api.route("/")
def hello_world():
    return "Index"

@api.route("/robot", methods=["GET"])
def get_robot():
    return robot.model_dump(mode="json")