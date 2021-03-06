# Generated by Django 4.0.2 on 2022-03-11 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    replaces = [
        ("people", "0001_initial"),
        ("people", "0002_user_bio_alter_user_business_area_and_more"),
        ("people", "0002_remove_usertopic_people_user_user_id_fe678a_idx_and_more"),
        ("people", "0003_merge_20220213_1607"),
        ("people", "0004_user_last_login_user_password_and_more"),
        ("people", "0005_user_admin_user_staff"),
        ("people", "0006_user_is_active"),
        ("people", "0007_remove_usertopic_people_user_user_id_7f44ed_idx_and_more"),
        ("people", "0008_alter_user_user_type_alter_usertopic_usertype"),
        ("people", "0009_alter_user_user_type_alter_usertopic_usertype"),
        ("people", "0010_remove_planofactiontarget_achieved_at_and_more"),
        ("people", "0009_notification_title_alter_notification_content"),
        ("people", "0010_notification_link"),
        ("people", "0011_merge_20220228_2112"),
        ("people", "0012_mentormentee_created_at_mentormentee_updated_at"),
        ("people", "0013_remove_rating_associated_topic"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessArea",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("business_area", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="PlanOfAction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("topic", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("business_area", models.CharField(max_length=50)),
                ("user_type", models.CharField(max_length=50)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("type", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="UserTopic",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="people.topic"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("rating", models.IntegerField()),
                (
                    "associated_topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="people.topic"
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor_rating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlanOfActionTarget",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=200)),
                ("achieved_at", models.DateTimeField(auto_now=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "associated_poa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.planofaction",
                    ),
                ),
                (
                    "set_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="planofaction",
            name="associated_mentee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plan_of_action_mentee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="planofaction",
            name="associated_mentor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plan_of_action_mentor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.CharField(max_length=200)),
                ("read", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MentorMentee",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("approved", models.BooleanField(default=False)),
                (
                    "mentee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.CharField(max_length=200)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="people.chat"
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chat",
            name="mentee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chat_mentee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="chat",
            name="mentor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chat_mentor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name="usertopic",
            index=models.Index(
                fields=["user", "topic"], name="people_user_user_id_fe678a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="mentormentee",
            index=models.Index(
                fields=["mentee", "mentor"], name="people_ment_mentee__aee93a_idx"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="business_area",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="people.businessarea"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="people.usertype"
            ),
        ),
        migrations.RemoveIndex(
            model_name="usertopic",
            name="people_user_user_id_fe678a_idx",
        ),
        migrations.AddField(
            model_name="usertopic",
            name="usertype",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="people.usertype",
            ),
        ),
        migrations.AddIndex(
            model_name="usertopic",
            index=models.Index(
                fields=["user", "topic", "usertype"],
                name="people_user_user_id_7f44ed_idx",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="password",
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=128,
                verbose_name="password",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="business_area",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="people.businessarea",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="people.usertype",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.RemoveIndex(
            model_name="usertopic",
            name="people_user_user_id_7f44ed_idx",
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentormentee"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="usertopic",
            name="usertype",
            field=models.CharField(
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentormentee"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddIndex(
            model_name="usertopic",
            index=models.Index(
                fields=["user", "topic", "usertype"],
                name="people_user_user_id_092cdd_idx",
            ),
        ),
        migrations.DeleteModel(
            name="UserType",
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentor & Mentee"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="usertopic",
            name="usertype",
            field=models.CharField(
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentor & Mentee"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentor & Mentee"),
                    ("None", "Neither"),
                ],
                default="None",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="usertopic",
            name="usertype",
            field=models.CharField(
                choices=[
                    ("Mentor", "Mentor"),
                    ("Mentee", "Mentee"),
                    ("MentorMentee", "Mentor & Mentee"),
                    ("None", "Neither"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.RemoveField(
            model_name="planofactiontarget",
            name="achieved_at",
        ),
        migrations.AddField(
            model_name="planofactiontarget",
            name="achieved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="notification",
            name="title",
            field=models.CharField(default="default", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="notification",
            name="content",
            field=models.CharField(max_length=500),
        ),
        migrations.AddField(
            model_name="notification",
            name="link",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="mentormentee",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mentormentee",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name="rating",
            name="associated_topic",
        ),
    ]
