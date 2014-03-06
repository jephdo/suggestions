from __future__ import division

from . import settings
from .models import Tag

def declare_weights(session):
    ranking = TagRanking()

    return ranking.build_weights(session)

def _normalize_weights(weights):
    """
    Normalize dictionary of tag weights by scaling values from 0 to 1.
    """
    max_weight = max(weights.values())

    return {k: v/max_weight for k,v in weights.items()}


class TagRanking(object):

    def __init__(self):
        self.tags = []
        self.tag_weights = {}

    def build_weights(self, session):
        self.load_tags(session)

        self.tag_weights = self.weight_by_occurence(self.tags)

        return self.tag_weights

    def load_tags(self, session):
        self.tags = session.query(Tag).all()

    def mix_weights(self, weights):
        pass

    def weight_by_occurence(self, tags):
        """
        Weigh tags by how often they appear in other documents.
        """
        unique_tag_names = set(tag.name.lower() for tag in tags)

        unique_weights = {}
        for tag in unique_tag_names:
            # total number of times a tag appears in all documents
            tag_count = sum(1 for t in tags if t.name.lower() == tag)

            # relative proportion that tag appears compared to all other tags
            unique_weights[tag] = tag_count / len(unique_tag_names)

        # assign weight to each tag, by id
        weights = {tag.id: unique_weights[tag.name.lower()] for tag in tags}

        return _normalize_weights(weights)

    def weight_by_content(self, tags):
        pass
