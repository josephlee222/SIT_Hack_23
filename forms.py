import shelve
from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, StringField, PasswordField, RadioField, validators, EmailField, DateField, ValidationError, \
    SubmitField, TextAreaField, IntegerField, DecimalField, BooleanField, MultipleFileField, SelectField, TimeField


# Put all forms here with a comment describing the form

# ADMIN USERS FORMS

# Sample form for test page
class testForm(Form):
    test = StringField("Testing Field", [
        # Validators in here, write error messages in the "message" parameter and use flashFormErrors() when
        # validating on post
        validators.Length(3, 64, message="The input must be between 3 to 64 characters"),
        validators.DataRequired(message="The input is required")
    ])


# User login form
class loginUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail is required to login")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="Password must be at least 8 characters"),
        validators.DataRequired(message="Password is required to login")
    ])

    submit = SubmitField("Login")

class resetPasswordForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail is required to login")
    ])

    submit = SubmitField("Send Reset E-mail")


# User registration form
class registerUserForm(Form):
    name = StringField("Your name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Username is required for registration")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail address is required for registration")
    ])

    submit = SubmitField("Register")

    def validate_email(form, field):
        with shelve.open("users") as users:
            if form.email.data in users:
                raise ValidationError("This e-mail has an existing account, please try again")


class searchUsersForm(Form):
    name = StringField("Search by name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required to search")
    ])


class editUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True)
    ], render_kw={'readonly': True})
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    birthday = DateField("Birthday", [
        validators.Optional()
    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])
    submit = SubmitField("Edit User")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class editProfileForm(Form):
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    birthday = DateField("Birthday", [
        validators.Optional()
    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])

    submit = SubmitField("Update Profile")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class changeUserPasswordForm(Form):
    password = PasswordField("Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])

    submit = SubmitField("Change Password")


class addUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail Address is required")
    ])
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    password = PasswordField("New Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])
    birthday = DateField("Birthday", [
        validators.Optional(),

    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])
    accountType = RadioField("Account Type", choices=[
        ("customer", "Normal Account"),
        ("admin", "Doctor/Staff Account"),
        ("council", "Councillor Account")
    ], validators=[
        validators.DataRequired("Account type is required")
    ])
    submit = SubmitField("Create User")

    def validate_email(form, field):
        with shelve.open("users") as users:
            if form.email.data in users:
                raise ValidationError("This e-mail has an existing account, please try again")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class addEpaForm(Form):
    name = StringField("PFA Name", [
        validators.DataRequired(message="PFA Name is required")
    ])
    description = TextAreaField("Description", [
        validators.Length(20, 1024, message="PFA Description must range from 20-1024 characters"),
        validators.DataRequired(message="Description is required")
    ])
    duration = IntegerField("Duration", [
        validators.NumberRange(1, 12, "Duration must be a range between 1 to 12 hours"),
        validators.DataRequired(message="Duration is required")
    ])
    location = StringField("Location", [
        validators.DataRequired(message="PFA location is required")
    ])
    mode = RadioField("PFA Mode", choices=[
        ("Virtual", "Virtual Learning"),
        ("Hybrid", "Hybrid"),
        ("Physical", "Physical Meeting")
    ], validators=[
        validators.DataRequired("PFA course mode is required")
    ])
    submit = SubmitField("Create PFA")


class addAddressForm(Form):
    name = StringField("Address Name", [
        validators.Length(1, 64, message="Address name must be between 1 to 64 characters"),
        validators.DataRequired(message="Address name is required")
    ])
    location = StringField("Location", [
        validators.Length(16, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Location is required")
    ])

    submit = SubmitField("Add Address")


class editAddressForm(Form):
    name = StringField("Address Name", [
        validators.Length(1, 64, message="Address name must be between 1 to 64 characters"),
        validators.DataRequired(message="Address name is required")
    ])
    location = StringField("Location", [
        validators.Length(16, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Location is required")
    ])
    submit = SubmitField("Edit Address")


class deleteUserForm(Form):
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])

    submit = SubmitField("Confirm Delete")

# ADMIN BLOG FORMS
class createArticleForm(FlaskForm):
    title = StringField("Title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters."),
        validators.DataRequired(message="Blog title is required.")
    ])
    brief = StringField("Brief Description", [
        validators.Length(3, 128, message="Brief description must be between 3 to 128 characters."),
        validators.DataRequired(message="Brief description is required.")
    ])
    content = TextAreaField("Article Content", [
        validators.DataRequired(message="Article content is required.")
    ])
    articleImage = FileField("Article Cover Image", validators=[
        FileRequired("Cover image is required"),
        FileAllowed(['jpg', 'png', 'webp'], message='Images files only!'),
    ])

    submit = SubmitField("Create Article")


class editArticleForm(FlaskForm):
    title = StringField("Title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters."),
        validators.DataRequired(message="Blog title is required.")
    ])
    brief = StringField("Brief Description", [
        validators.Length(3, 128, message="Brief description must be between 3 to 128 characters."),
        validators.DataRequired(message="Brief description is required.")
    ])
    content = TextAreaField("Article Content", [
        validators.DataRequired(message="Article content is required.")
    ])
    articleImage = FileField("Article Cover Image", validators=[
        validators.Optional(),
        FileAllowed(['jpg', 'png', 'webp'], message='Images files only!'),
    ])

    submit = SubmitField("Save")

class connectionForm(Form):
    councilId = StringField("Counsellor E-mail", [
        validators.DataRequired(message="Message is required")
    ])
    message = StringField("Message", [
        validators.Length(3, 64, message="Message must be between 3 to 64 characters"),
        validators.DataRequired(message="Message is required")
    ])

class feedbackForm(Form):
    q1 = IntegerField("q1", [
        validators.NumberRange(1, 5, "Rating must be a range between 1 to 12 hours"),
        validators.DataRequired(message="Rating is required")
    ])
    q2 = IntegerField("q2", [
        validators.NumberRange(1, 5, "Rating must be a range between 1 to 12 hours"),
        validators.DataRequired(message="Rating is required")
    ])
    experience_details = TextAreaField("Both positve and negative feeedback appreciated...", [
        validators.Length(20, 1024, message="Experience Feedback Details must range from 20-1024 characters"),
        validators.DataRequired(message="Feedback is required")
    ],render_kw={"placeholder": "Both positve and negative feeedback appreciated..."})
    comments = TextAreaField("comments", [
        validators.Length(20, 1024, message="comments must range from 20-1024 characters"),
    ],render_kw={"placeholder": ""})