from django.shortcuts import render
from .models import Event, EventInstance, Entity
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_events = Event.objects.count()
    num_birthday_events = Event.objects.filter(category__name="Birthday").count()
    num_instances = EventInstance.objects.count()
    num_instances_available = EventInstance.objects.filter(is_complete=False).count()
    num_entities = Entity.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_events": num_events,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_entities": num_entities,
        "num_birthday_events": num_birthday_events,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    paginate_by = 2
    context_object_name = "event_list"
    template_name = (
        "reminder/event_list.html"  # Specify your own template name/location
    )

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EventListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context["some_data"] = "This is just some data"
        return context


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event

    def get(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        return render(request, "reminder/event_detail.html", context={"event": event})


class EntityListView(LoginRequiredMixin, generic.ListView):
    model = Entity
    context_object_name = "entity_list"
    template_name = "reminder/entity_list.html"

    def get_queryset(self):
        return Entity.objects.filter(user=self.request.user)


class EntityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Entity

    def get(self, request, pk, *args, **kwargs):
        entity = get_object_or_404(Entity, pk=pk)
        events = Event.objects.filter(entities=entity)
        print(events)
        return render(
            request,
            "reminder/entity_detail.html",
            context={"entity": entity, "events": events},
        )
