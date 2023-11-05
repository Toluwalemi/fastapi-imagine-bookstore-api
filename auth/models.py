from tortoise import fields

from helpers.base_abstract_model_helper import BaseAbstractModel
from helpers.password_hashing import Hasher
from helpers.utils import normalize_email


class User(BaseAbstractModel):
    """User Model"""

    first_name = fields.CharField(
        max_length=100, description="user first name", null=True, default=None
    )
    last_name = fields.CharField(
        max_length=100, description="user last name", null=True, default=None
    )
    email = fields.CharField(
        max_length=255, unique=True, description="User email address", null=True
    )
    password = fields.CharField(
        description="User password", max_length=255, null=True, default=None
    )
    email_verified = fields.BooleanField("Email Verification Status", default=False)
    """USER_TYPES = [
        ("CONSUMER", "CONSUMER"),
        ("ADMIN", "ADMIN"),
    ]
    """
    user_types = fields.JSONField(
        default=list, description="User Types the user belong to"
    )
    # added just in case we need to add other details to prevent frequent migrations
    meta_data = fields.JSONField(default=dict, null=True)

    class Meta:
        table = "user"

    def __str__(self):
        return self.display_name

    def create_user(self, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        email = kwargs.get("email")
        password = kwargs.get("password")
        user_type = kwargs.get("user_type")
        if first_name:
            first_name = first_name.capitalize()
        if last_name:
            last_name = last_name.capitaliz()
        if email:
            email = normalize_email(email)
        if password:
            password = Hasher.create_password_hash(password)
        if user_type:
            user_type = [user_type]
        return self.save(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            user_types=user_type,
        )

    @property
    def display_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def delete(self, soft_delete: bool = True, actor=None):
        import uuid

        generated_key = f"DELETED-{uuid.uuid4().hex}"
        self.email = f"{generated_key}-{self.email}"
        super().delete(soft_delete)
