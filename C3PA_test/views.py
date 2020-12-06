import asyncio
import json
import logging

import httpx
from django.views.generic.edit import FormView
from django.utils.decorators import classonlymethod
from django.shortcuts import render
from asgiref.sync import sync_to_async
from .forms import PersonForm

logger = logging.getLogger(__name__)


# helpers

async def async_get(url: str) -> None:
    await asyncio.sleep(3)
    async with httpx.AsyncClient() as client:
        rez = await client.get(url)
        logger.info(f"{rez}, {url}")


# views

class PersonView(FormView):
    form_class = PersonForm
    template_name = 'person_form.html'

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    async def post(self, request, *args, **kwargs):
        """Async post"""
        form = PersonForm(request.POST)
        form_is_valid = await sync_to_async(form.is_valid)()

        if form_is_valid:
            await sync_to_async(form.save)()

            # non-blocking get requests
            loop = asyncio.get_event_loop()
            loop.create_task(async_get("https://httpbin.org/"))
            loop.create_task(async_get("https://www.google.com/"))

            response = json.dumps({
                "success": True
            })

            return render(request, 'person_success.html', {"response": response})

        invalid_fields = list(form.errors)

        response = json.dumps({
            "success": False,
            "fields": invalid_fields
        })

        return render(request, 'person_failed.html', {"response": response, "invalid_fields": invalid_fields})
