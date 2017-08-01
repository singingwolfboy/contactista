from bradley.models import db


class Pronouns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_pronoun = db.Column(db.String(50), nullable=False)
    object_pronoun = db.Column(db.String(50), nullable=False)
    possessive_determiner = db.Column(db.String(50), nullable=False)
    possessive_pronoun = db.Column(db.String(50), nullable=False)
    reflexive_pronoun = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return "{subject}/{object}".format(
            subject=self.subject_pronoun,
            object=self.object_pronoun,
        )

    def __repr__(self):
        return "<Pronouns {subj}/{obj}/{poss_det}/{poss}/{reflex}>".format(
            subj=self.subject_pronoun,
            obj=self.object_pronoun,
            poss_det=self.possessive_determiner,
            poss=self.possessive_pronoun,
            reflex=self.reflexive_pronoun,
        )
