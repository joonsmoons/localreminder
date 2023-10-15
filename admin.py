from django.contrib import admin
from .models import Category, Entity, Notification, Event, EventInstance


class EventsInline(admin.TabularInline):
    model = Event
    extra = False


class EventsInstanceInline(admin.TabularInline):
    model = EventInstance
    extra = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    name = "Category"
    verbose_name = "Categories"
    list_display = ("name",)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    name = "Entity"
    verbose_name = "Entities"
    list_display = ("name", "user")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("remaining_days",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_entity",
        "date",
        "category",
        "is_lunar_year",
        "recurrence",
        "user",
    )
    inlines = [EventsInstanceInline]


@admin.register(EventInstance)
class EventInstanceAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "date", "is_complete")
    list_filter = ("user", "is_complete")
    exclude = ("id",)
    fieldsets = (
        (None, {"fields": ("event", "user")}),
        ("Completion", {"fields": ("date", "is_complete")}),
    )
