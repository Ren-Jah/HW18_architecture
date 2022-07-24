from flask import request
from flask_restx import Resource, Namespace

from app.dao.models.directors import DirectorSchema, Director
from app.database import db

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        query_all = db.session.query(Director)
        final_query = query_all.all()

        return directors_schema.dump(final_query), 200

    def post(self):
        new_data = request.json

        director_ = director_schema.load(new_data)
        new_director = Director(**director_)
        with db.session.begin():
            db.session.add(new_director)

        return "Created", 201


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did):
        query_one = Director.query.get(did)

        if not query_one:
            return "Not found", 404

        return director_schema.dump(query_one), 200

    def put(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "Not found", 404

        new_data = request.json
        director_selected.update(new_data)
        db.session.commit()

        return "No Content", 204

    def delete(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "Not found", 404

        rows_deleted = director_selected.delete()
        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "Bad request", 400

        db.session.commit()
        return "No Content", 204