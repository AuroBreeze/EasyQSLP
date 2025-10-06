import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Ensure a superuser exists based on ADMIN_* environment variables; also add to Operator group. Idempotent."

    def handle(self, *args, **options):
        U = get_user_model()
        email = os.environ.get("ADMIN_EMAIL")
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        if not (email and username and password):
            self.stdout.write(self.style.WARNING("ADMIN_* envs not set; skip superuser creation"))
            return

        user = U.objects.filter(email=email).first() or U.objects.filter(username=username).first()
        if not user:
            user = U.objects.create(
                email=email,
                username=username,
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {username} <{email}>"))
        else:
            changed = False
            if not user.is_staff:
                user.is_staff = True; changed = True
            if not user.is_superuser:
                user.is_superuser = True; changed = True
            # Always reset password to keep dev access predictable
            user.set_password(password); changed = True
            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Updated superuser flags/password for: {username} <{email}>"))
            else:
                self.stdout.write(f"Superuser already present: {username} <{email}>")

        # Ensure Operator group and membership
        op, _ = Group.objects.get_or_create(name="Operator")
        user.groups.add(op)
        self.stdout.write("Ensured Operator group and added admin to it")
