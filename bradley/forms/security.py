from flask import Markup, request, current_app
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    validators, ValidationError
)
from flask_security.utils import (
    _datastore, config_value, get_message, verify_and_update_password
)
from flask_security.confirmable import requires_confirmation
from flask_security.forms import (
    Form, RegisterFormMixin, NewPasswordFormMixin, NextFormMixin,
    get_form_field_label, password_required
)


username_required = validators.InputRequired(message='Username not provided')
username_validator = validators.Regexp(r"[A-Za-z0-9_]+", message='Invalid username')


def unique_user_username(form, field):
    if _datastore.get_user(field.data) is not None:
        raise ValidationError(
            "{username} is already in use.".format(username=field.data)
        )


class UniqueUsernameFormMixin:
    username = StringField(
        'Username',
        validators=[username_required, username_validator, unique_user_username]
    )


class ConfirmRegisterForm(Form, RegisterFormMixin,
                          UniqueUsernameFormMixin, NewPasswordFormMixin):
    pass


class LoginForm(Form, NextFormMixin):
    username = StringField('Username',
                        validators=[username_required])
    password = PasswordField(get_form_field_label('password'),
                             validators=[password_required])
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', '')
        self.remember.default = config_value('DEFAULT_REMEMBER_ME')
        if current_app.extensions['security'].recoverable and \
                not self.password.description:
            html = Markup(u'<a href="{url}">{message}</a>'.format(
                url=url_for_security("forgot_password"),
                message=get_message("FORGOT_PASSWORD")[0],
            ))
            self.password.description = html

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = _datastore.get_user(self.username.data)

        if self.user is None:
            self.username.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not self.user.password:
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if requires_confirmation(self.user):
            self.username.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
            return False
        if not self.user.is_active:
            self.username.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True
