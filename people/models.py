import uuid

from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Changing this to override the default model!


class UserType(models.TextChoices):
    Mentor = "Mentor"
    Mentee = "Mentee"
    MentorMentee = "MentorMentee", "Mentor & Mentee"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # Main user model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    business_area = models.ForeignKey(
        "BusinessArea", on_delete=models.CASCADE, null=True
    )
    bio = models.TextField(blank=True)
    user_type = models.CharField(
        choices=UserType.choices, max_length=50, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField("active", default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return self.admin
        # Simplest possible

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class BusinessArea(models.Model):
    # Business areas within the company
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_area = models.CharField(max_length=50)

    def __str__(self):
        return self.business_area


class MentorMentee(models.Model):
    # Mentor-mentee relationship
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor", db_index=True
    )
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentee", db_index=True
    )
    approved = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["mentee", "mentor"])]


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.topic


class UserTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    usertype = models.CharField(choices=UserType.choices, max_length=50, null=True)

    class Meta:
        indexes = [models.Index(fields=["user", "topic", "usertype"])]


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor_rating", db_index=True
    )
    rating = models.IntegerField()
    associated_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    rated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rated_by",
        db_index=True,
        blank=True,
        null=True,
    )


class PlanOfAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    associated_mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plan_of_action_mentor",
        db_index=True,
    )
    associated_mentee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plan_of_action_mentee",
        db_index=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PlanOfActionTarget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    achieved_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    associated_poa = models.ForeignKey(
        PlanOfAction, on_delete=models.CASCADE, db_index=True
    )
    set_by = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_mentor", db_index=True
    )
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_mentee", db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    content = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
