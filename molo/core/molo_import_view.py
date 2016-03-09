import requests
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from unicore.content.models import Localisation, Category, Page
from molo.core.models import (
    SiteLanguage, SectionPage, ArticlePage, FooterPage)
from elasticgit.workspace import RemoteWorkspace
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from molo.core.models import Main


@api_view(['GET'])
def get_repos(request):
    response = requests.get('http://localhost:6543/repos.json').json()
    return Response({
        'repos': [repo.get('name') for repo in response]})


@api_view(['GET'])
def get_repo_languages(request, name):
    ws = RemoteWorkspace('http://localhost:6543/repos/%s.json' % name)
    ws.sync(Localisation)

    return Response({
        'locales': [l.locale for l in ws.S(Localisation).all()],
    })


@api_view(['GET'])
def get_available_languages(request):
    return Response({
        'locales': [{
            'locale': l.locale,
            'name': l.get_locale_display(),
            'is_main_language': l.is_main_language}
            for l in SiteLanguage.objects.all()],
    })


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def import_content(request, name):

    def get_or_create(cls, obj, parent):
        if cls.objects.filter(uuid=obj.uuid).exists():
            instance = cls.objects.get(uuid=obj.uuid)
            instance.title = obj.title
            instance.save_revision().publish()
            print 'updated', obj.title
            return instance

        instance = cls(uuid=obj.uuid, title=obj.title)
        parent.add_child(instance=instance)
        instance.save_revision().publish()
        print 'created', obj.title
        return instance

    ws = RemoteWorkspace('http://localhost:6543/repos/%s.json' % name)
    ws.sync(Localisation)
    ws.sync(Category)
    ws.sync(Page)

    # create wagtail content

    locales = request.data.get('locales')
    for selected_locale in locales:
        for l in ws.S(Localisation).filter(
                locale=selected_locale.get('locale')):
            print "we're here"
        site_language = SiteLanguage.objects.get(
            locale=selected_locale.get('site_language'))
        if site_language.is_main_language:
            main = Main.objects.all().first()
            for c in ws.S(Category).filter(
                    language=selected_locale.get('locale')):
                get_or_create(SectionPage, c, main)

            for p in ws.S(Page).filter(language=selected_locale.get('locale')):
                if p.primary_category:
                    section = SectionPage.objects.get(uuid=p.primary_category)
                    get_or_create(ArticlePage, p, section)
                else:
                    # special case for articles with no primary category
                    # this assumption is probably wrong..but we have no where
                    # else to put them
                    get_or_create(FooterPage, p, main)
    return Response()
