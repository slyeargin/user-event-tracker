from flask import abort, request, jsonify
from models import Event, User, db
from config import Config

user_eid = Config.USER_EID

def init_routes(app):
    @app.get('/')
    def home():
        return "User Event Tracker"
    
    @app.get('/user')
    def generate_user():
        user = User()
        db.session.begin()
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "eid": user.eid
        }), 201

    @app.get('/events')
    def get_events():
        events = db.session.execute(
            db.select(Event)
            .where(Event.created_by == user_eid)
            .where(Event.active == True)).scalars().all()
        return jsonify([event.serialized for event in events])

    @app.post('/events')
    def search_events():
        input = request.json

        title = input.get("title")
        description = input.get("description")

        if not any([title, description]):
            abort(400)

        query = db.select(Event).where(Event.created_by == user_eid).where(Event.active == True)

        if title:
            query = query.filter(Event.title.ilike(f'%{title}%'))

        if description:
            query = query.filter(Event.description.ilike(f'%{description}%'))

        events = db.session.execute(query).scalars().all()
        return jsonify([event.serialized for event in events])

    @app.post('/event')
    def create_event():
        input = request.json
        try: 
            event = Event(**input)
            event.created_by = user_eid
            db.session.begin()
            db.session.add(event)
            db.session.commit()
        except:
            db.session.rollback()
            abort(400)
        return '', 201

    @app.get('/event/<uuid:event_eid>')
    def get_event(event_eid):
        event = db.one_or_404(
            db.select(Event).where(Event.eid == event_eid),
            description=f"No event found for {event_eid}.")
        return jsonify(event.serialized)

    @app.put('/event/<uuid:event_eid>')
    def deactivate_event(event_eid):
        db.session.begin()
        try:
            event = db.session.execute(
                db.select(Event)
                .where(Event.created_by == user_eid)
                .where(Event.active == True)
                .where(Event.eid == event_eid)).scalar_one_or_none()
            if not event:
                abort(400)
            event.active = False
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        else:
            return '', 204

    @app.delete('/event/<uuid:event_eid>')
    def delete_event(event_eid):
        db.session.begin()
        try:
            event = db.session.execute(
                db.select(Event)
                .where(Event.created_by == user_eid)
                .where(Event.eid == event_eid)).scalar_one_or_none()
            if not event:
                abort(400)
            db.session.delete(event)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        return '', 204
