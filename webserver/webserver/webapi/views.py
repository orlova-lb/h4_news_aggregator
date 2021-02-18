from django.http import JsonResponse
from django.core import serializers
import json
from webserver.webapi.models import News, Tags, NewsToTags


def news(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            id = int(request.GET['id'])
            news = [News.objects.get(pk=id)]
        else:
            # TODO: better
            # TODO: this should be sequential filtering, not if-elif-elif
            if 'source_api' in request.GET:
                source_api = request.GET['source_api']
                news = News.objects.filter(source_api=source_api)
            elif 'published_date' in request.GET:
                published_date = request.GET['published_date']
                news = News.objects.filter(published_date=published_date)
            else:
                news = News.objects.all()
        # TODO: use _serialize_to_json(news)
        news = _serialize_to_json(news)
        return JsonResponse({'response': news})


def _serialize_to_json(data):
    """
    Will get a queryset, serialize it to JSON in a format:
    [{"id": pk, "%model_field_1%": "%model_value_1%", [...]}]
    :param data:
    :return:
    """
    raw_data = json.loads(serializers.serialize('json', data))
    # TODO: add dicts reformatting
    raw_data = list()
    for item in raw_data:
        item_dict = {'id': item['pk']}
        item_dict.update(item)
        raw_data.append(item_dict)
    return raw_data
