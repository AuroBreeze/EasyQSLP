from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Initialize demo data and ensure admin user exists (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--admin-email", dest="admin_email", default=None)
        parser.add_argument("--admin-username", dest="admin_username", default=None)
        parser.add_argument("--admin-password", dest="admin_password", default=None)
        parser.add_argument("--create-demo", action="store_true", help="Create demo user demo/demo123456 if not exists")
        # optional single user seed
        parser.add_argument("--user-email", dest="user_email", default=None)
        parser.add_argument("--user-username", dest="user_username", default=None)
        parser.add_argument("--user-password", dest="user_password", default=None)
        parser.add_argument("--update-user-password", action="store_true", help="Update seed user's password if exists")

    def handle(self, *args, **options):
        import os

        User = get_user_model()

        # Prefer CLI args, then env vars, then safe defaults
        admin_email = options.get("admin_email") or os.getenv("ADMIN_EMAIL")
        admin_username = options.get("admin_username") or os.getenv("ADMIN_USERNAME", "admin")
        admin_password = options.get("admin_password") or os.getenv("ADMIN_PASSWORD")

        # Ensure admin exists
        if admin_email and admin_password:
            admin, created = User.objects.get_or_create(
                email=admin_email,
                defaults={
                    "username": admin_username or admin_email.split("@")[0],
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            # Set password only when created, to avoid overriding manual changes.
            if created:
                admin.set_password(admin_password)
                admin.save()
                self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_email}"))
            else:
                # Ensure flags are correct without changing password.
                changed = False
                if not admin.is_staff or not admin.is_superuser or not admin.is_active:
                    admin.is_staff = True
                    admin.is_superuser = True
                    admin.is_active = True
                    admin.save()
                    changed = True
                self.stdout.write(self.style.SUCCESS(
                    f"Admin user ensured: {admin_email} (updated_flags={changed})"
                ))
        else:
            self.stdout.write(self.style.WARNING(
                "ADMIN_EMAIL/ADMIN_PASSWORD not provided; skip ensuring admin user"
            ))

        # Optional demo user
        if options.get("create_demo") or os.getenv("CREATE_DEMO_USER") == "1":
            demo, created = User.objects.get_or_create(
                username="demo",
                defaults={
                    "email": "demo@example.com",
                    "is_staff": False,
                    "is_superuser": False,
                    "is_active": True,
                },
            )
            if created:
                # Some custom user models use email as USERNAME_FIELD; make sure password set
                demo.set_password("demo123456")
                demo.save()
                self.stdout.write(self.style.SUCCESS("Demo user created: demo/demo123456"))
            else:
                self.stdout.write(self.style.SUCCESS("Demo user already exists"))

        # Optional: create a specific user via CLI/env variables
        seed_email = options.get("user_email") or os.getenv("SEED_USER_EMAIL")
        seed_username = options.get("user_username") or os.getenv("SEED_USER_USERNAME")
        seed_password = options.get("user_password") or os.getenv("SEED_USER_PASSWORD")
        update_pwd_flag = options.get("update_user_password") or (os.getenv("SEED_UPDATE_PASSWORD") == "1")
        if seed_email and seed_username and seed_password:
            user, created = User.objects.get_or_create(
                email=seed_email,
                defaults={
                    "username": seed_username,
                    "is_active": True,
                },
            )
            if created:
                user.set_password(seed_password)
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Seed user created: {seed_username} <{seed_email}>"
                ))
            else:
                if seed_password and update_pwd_flag:
                    user.set_password(seed_password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"Seed user password updated: {seed_username} <{seed_email}>"
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f"Seed user already exists: {seed_username} <{seed_email}> (password unchanged)"
                    ))

        self.stdout.write(self.style.SUCCESS("init_demo_data completed."))
