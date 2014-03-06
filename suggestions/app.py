from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import settings
from .models import Document, Tag
from .suggestions import declare_weights

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

TAG_WEIGHTS = declare_weights(session)

def tag_suggestions(request):
    """
    Returns a list of potential tags in the most "relevant" order.
    """

    document_id = int(request.matchdict['document_id'])
    tags = session.query(Tag).filter_by(document_id=document_id).all()

    sorted_tags = sorted(tags, key=lambda t: TAG_WEIGHTS[t.id], reverse=True)
    return [tag.to_dict() for tag in sorted_tags]

def _save_click(tag_id, session):
    pass


config = Configurator()
config.add_route('tag_suggestions', '/document/{document_id}/tags/')
config.add_view(tag_suggestions, route_name='tag_suggestions', renderer='json')
app = config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
