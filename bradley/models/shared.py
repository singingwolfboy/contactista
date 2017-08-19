from bradley.models import db


class Pronouns(db.Model):
    """
    The set of pronouns used by a person. This encompasses both commonly
    used pronouns like "he/him" and "she/her", but also less commonly used
    pronouns like "they/them" and "e/em".
    """
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    object = db.Column(db.String(50), nullable=False)
    possessive_determiner = db.Column(db.String(50), nullable=False)
    possessive = db.Column(db.String(50), nullable=False)
    reflexive = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return "{subject}/{object}".format(
            subject=self.subject,
            object=self.object,
        )

    def __repr__(self):
        return "<Pronouns {subj}/{obj}/{poss_det}/{poss}/{reflex}>".format(
            subj=self.subject,
            obj=self.object,
            poss_det=self.possessive_determiner,
            poss=self.possessive,
            reflex=self.reflexive,
        )
