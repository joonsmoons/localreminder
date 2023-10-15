from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model to categorize events in the reminder app.

    Attributes:
        name (str): The name of the category.
    """

    name = models.CharField(max_length=20, default="General")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name


# class User(models.Model):
#     """
#     Model to store user information.

#     Attributes:
#         name (str): The user's name.
#         birth_date (date): The user's date of birth.
#         is_married (bool): Indicates if the user is married.
#         email (str): The user's email address.
#     """

#     name = models.CharField(max_length=150)
#     birth_date = models.DateField(null=True, blank=True)
#     is_married = models.BooleanField(default=False)
#     email = models.EmailField()

#     class Meta:
#         ordering = ["name", "birth_date"]

#     def __str__(self):
#         """String for representing the Model object."""
#         return f"{self.name}"


class Entity(models.Model):
    """
    Model to represent entities with names and phone numbers.

    Attributes:
        name (str): The name of the entity.
        user (ForeignKey to User): The user to whom the entity belongs.
    """

    name = models.CharField(max_length=150)
    # phone_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        verbose_name = "Entity"
        verbose_name_plural = "Entities"

    def get_absolute_url(self):
        """Returns the URL to access a particular entity instance."""
        return reverse("entity-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Notification(models.Model):
    """
    Model to store information about event notifications.

    Attributes:
        remaining_days (int): The remaining days left in the notification.
    """

    remaining_days = models.IntegerField(default=0)

    class Meta:
        ordering = ["remaining_days"]

    def __str__(self):
        """String for representing the Model object."""
        return f"Notification with {self.remaining_days} days remaining"


class Event(models.Model):
    """
    Model to represent events with various attributes.

    Attributes:
        name (str): The name of the event.
        date (date): The date of the event.
        category (ForeignKey to Category): The category of the event.
        year_type (str): The type of year (e.g., Gregorian).
        recurrence (str): The recurrence pattern (None, Yearly, Monthly, Weekly, Daily).
        entities (ManyToMany to Entity): Entities associated with the event.
        notifications (ManyToMany to Notification): Notifications associated with the event.
        user (ForeignKey to User): The user who created the event.
    """

    name = models.CharField(max_length=100)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_lunar_year = models.BooleanField(default=False)
    recurrence_choices = [
        ("없음", "none"),
        ("매년", "year"),
        ("매월", "month"),
        ("매주", "week"),
        ("매일", "day"),
    ]
    recurrence = models.CharField(
        max_length=10, choices=recurrence_choices, default="none"
    )
    entities = models.ManyToManyField(Entity, related_name="events")
    notifications = models.ManyToManyField(Notification, related_name="events")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this event."""
        return reverse("event-detail", args=[str(self.id)])

    def display_entity(self):
        """Create a string for the Entity. This is required to display entity in Admin."""
        return ", ".join(entity.name for entity in self.entities.all()[:3])

    display_entity.short_description = "Entity"

    def __str__(self):
        """String for representing the Model object."""
        return f"{', '.join(self.entities.all().values_list('name', flat=True))} {self.name} ({self.date})"


class EventInstance(models.Model):
    """
    Model to represent specific instances or occurrences of events.

    Attributes:
        event (ForeignKey to Event): The event associated with the instance.
        date (date): The date of the event instance.
        user (ForeignKey to User): The user to whom the event instance is associated.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this event instance across whole events",
    )
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model object."""
        return f"EventInstance for {self.id} ({self.event.name}) on {self.date}"

    @property
    def is_complete_display(self):
        return "Complete" if self.is_complete else "Incomplete"
