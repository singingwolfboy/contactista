from flask import redirect, url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView as BaseModelView
from flask_admin import helpers as admin_helpers
from wtforms import PasswordField
from flask_security import current_user, login_required
from contactista.models import (
    db, security, User, Role,
    Contact, ContactName, ContactPronouns, ContactEmail
)


admin = Admin(template_mode='bootstrap3')


class ModelView(BaseModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


def admin_context():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


class UserView(ModelView):
    column_exclude_list = ('password',)
    column_auto_select_related = True
    form_columns = (
        'username', 'new_password', 'roles', 'active', 'confirmed_at'
    )
    form_extra_fields = {
        'new_password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if getattr(model, "new_password"):
            model.set_password(model.new_password)


class ContactView(ModelView):
    column_auto_select_related = True
    inline_models = (ContactName, ContactPronouns, ContactEmail)


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ContactView(Contact, db.session))
