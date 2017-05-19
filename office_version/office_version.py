#!/usr/bin/python


from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from inventory.models import InventoryItem
from server.models import *
import server.utils as utils


class OfficeVersion(IPlugin):
    name = "OfficeVersion"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return "builtin"

    def get_description(self):
        return "Microsoft Office Version"

    def widget_content(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to -
        # front, bu_dashboard and group_dashboard. If page is set to
        # bu_dashboard, or group_dashboard, you will be passed a business_unit
        # or machine_group id to use (mainly for linking to the right search).
        if page == "front":
            t = loader.get_template(
                "kvnjcby/office_version/templates/front.html")
        elif page in ("bu_dashboard", "group_dashboard"):
            t = loader.get_template(
                "kvnjcby/office_version/templates/id.html")

        data = InventoryItem.objects.filter(machine__in=machines,
                                            application__name="Microsoft Outlook",
                                            application__bundleid__startswith="com.microsoft") \
                                    .values("version") \
                                    .annotate(count=Count("version")) \
                                    .order_by("version")

        c = Context({
            "title": self.get_description(),
            "data": data,
            "theid": theid,
            "page": page})

        return t.render(c)

    def filter_machines(self, machines, data):
        machines = machines.filter(inventoryitem__application__name="Microsoft Outlook",
                                   inventoryitem__version=data,
                                   inventoryitem__application__bundleid__startswith="com.microsoft")

        return machines, "Machines with version {} of Microsoft Office".format(data)
