from django.contrib import admin

from airport.models import Airport, Route, Airplane, Order, Ticket, Flight, Crew

admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Airplane)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Flight)
admin.site.register(Crew)