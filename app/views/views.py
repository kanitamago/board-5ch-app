from app import app
from flask import render_template, url_for, redirect, request
from app import db
from app.models.thread import Thread
from app.models.response import Response
from datetime import datetime
from random import randint
import re

def check_links(content):
    if "http" in content:
        links = []
        replace_links = []
        pattern = "(http|https)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)"
        result = re.findall(pattern, content)
        original_links = [link[0]+link[1] for link in result]
        i_links = [link.replace("//i.", "//p.") for link in original_links]
        replace_links = ["<a href='{}' target='blank_'>{}</a>".format(link, link) for link in i_links]
        for before, after in zip(original_links, replace_links):
            content = content.replace(before, after)
        return content
    else:
        return content

@app.route("/")
def index():
    q = randint(1, 99999)
    items = Thread.query.order_by(Thread.id.desc()).all()
    responses = Response.query.order_by(Response.id.desc()).all()
    output = {}
    for item in items:
        responses = Response.query.filter(Response.thread_id == item.id).all()
        output[item] = len(responses)
    return render_template("index.html", output=output, title="", content="", error=None, q=q)

@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        pub_date = datetime.now()
        title = request.form["title"]
        password = request.form["password"]
        content = request.form["content"]
        if title == "" or password == "" or content == "":
            q = randint(1, 99999)
            output = Thread.query.order_by(Thread.id.desc()).all()
            title = request.form["title"]
            content = request.form["content"]
            return render_template("index.html", output=output, title=title, content=content, error="空欄を埋めてください", q=q)
        note = Thread(pub_date=pub_date, title=title, password=password, content=content)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("index"))
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    if request.method == "POST":
        check_password = request.form["password"]
        item = Thread.query.get(id)
        responses = Response.query.filter(Response.thread_id == id).all()
        if check_password == item.password:
            for response in responses:
                db.session.delete(response)
                db.session.commit()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            q = randint(1, 99999)
            responses = Response.query.filter(Response.thread_id == id).all()
            clean_responses = []
            responses_pub_dates = []
            responses_ids = []
            for idx, response in enumerate(responses):
                responses_ids.append(idx)
                responses_pub_dates.append(response.pub_date)
                response = response.response.replace("　", " ")
                response = response.split("　")
                response = response[0].replace("\r\n", "<br>")
                response = check_links(response)
                clean_responses.append(response)
            print(clean_responses)
            response_set = zip(responses_ids, clean_responses, responses_pub_dates)
            pub_date = item.pub_date
            title = item.title
            content = item.content.replace("　", " ")
            content = content.split("　")
            content = content[0].replace("\r\n", "<br>")
            content = check_links(content)
            return render_template("detail.html", id=item.id, pub_date=pub_date, title=title, error="パスワードが違います", content=content, response_set=response_set, q=q)
    return redirect(url_for("index"))

@app.route("/detail/<int:id>", methods=["POST", "GET"])
def detail(id):
    if request.method == "POST":
        q = randint(1, 99999)
        item = Thread.query.get(id)
        responses = Response.query.filter(Response.thread_id == id).all()
        clean_responses = []
        responses_pub_dates = []
        responses_ids = []
        for idx, response in enumerate(responses):
            responses_ids.append(idx)
            responses_pub_dates.append(response.pub_date)
            response = response.response.replace("　", " ")
            response = response.split("　")
            response = response[0].replace("\r\n", "<br>")
            response = check_links(response)
            clean_responses.append(response)
        response_set = zip(responses_ids, clean_responses, responses_pub_dates)
        pub_date = item.pub_date
        title = item.title
        content = item.content.replace("　", " ")
        content = content.split("　")
        content = content[0].replace("\r\n", "<br>")
        content = check_links(content)
        return render_template("detail.html", id=id, pub_date=pub_date, title=title, error=None, content=content, response_set=response_set, q=q)
    else:
        q = randint(1, 99999)
        item = Thread.query.get(id)
        responses = Response.query.filter(Response.thread_id == id).all()
        clean_responses = []
        responses_pub_dates = []
        responses_ids = []
        for idx, response in enumerate(responses):
            responses_ids.append(idx)
            responses_pub_dates.append(response.pub_date)
            response = response.response.replace("　", " ")
            response = response.split("　")
            response = response[0].replace("\r\n", "<br>")
            response = check_links(response)
            clean_responses.append(response)
        response_set = zip(responses_ids, clean_responses, responses_pub_dates)
        pub_date = item.pub_date
        title = item.title
        content = item.content.replace("　", " ")
        content = content.split("　")
        content = content[0].replace("\r\n", "<br>")
        content = check_links(content)
        return render_template("detail.html", id=id, pub_date=pub_date, title=title, error=None, content=content, response_set=response_set, q=q)

@app.route("/post-res/<int:id>", methods=["POST", "GET"])
def post_res(id):
    if request.method == "POST":
        pub_date = datetime.now()
        response = request.form["response"]
        if response == "":
            return redirect(url_for("index"))
        res = Response(pub_date=pub_date, thread_id=id, response=response)
        db.session.add(res)
        db.session.commit()
        return redirect(url_for("detail", id=id))
    return redirect(url_for("index"))
