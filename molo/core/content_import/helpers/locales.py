from babel import Locale
from babel.core import UnknownLocaleError

from unicore.content.models import Localisation


def get_locales(repos):
    parsed = parse_repos_locales(repos)
    uniqs = uniqs_from_parsed(parsed)

    return {
        'locales': locales_from_parsed(parsed, uniqs),
        'warnings': warnings_from_parsed(parsed, uniqs)
    }


def locales_from_parsed(parsed, uniqs):
    return sorted_uniq_locales([
        locale
        for d in parsed
        for locale in d['locales']
        if locale['locale'] in uniqs
    ])


def warnings_from_parsed(parsed, uniqs):
    warnings = [warning for d in parsed for warning in d['warnings']]
    return warnings + stray_warnings_from_parsed(parsed, uniqs)


def stray_warnings_from_parsed(parsed, uniqs):
    return [
        stray_warning(d['repo'], locale)
        for d in parsed
        for locale in d['locales']
        if locale['locale'] not in uniqs
    ]


def stray_warning(repo, locale):
    return {
        'type': 'stray_locale',
        'details': conj(locale, {
            'repo': repo.name,
        })
    }


def uniqs_from_parsed(parsed):
    return set.intersection(*[
        set(locale['locale'] for locale in d['locales'])
        for d in parsed
    ])


def parse_repos_locales(repos):
    return [
        conj(parse_repo_locales(repo), {'repo': repo})
        for repo in repos]


def parse_repo_locales(repo):
    locales = []
    warnings = []

    for l in sorted_uniq_locales(repo.workspace.S(Localisation).all()):
        try:
            locales.append({
                'locale': l.locale,
                'name': Locale.parse(l.locale).english_name
            })
        except UnknownLocaleError:
            warnings.append({
                'type': 'unknown_locale',
                'details': {
                    'repo': repo.name,
                    'locale': l.locale
                }
            })

    return {
        'locales': locales,
        'warnings': warnings,
    }


def sorted_uniq_locales(locales):
    locales = uniq_by(locales, get_locale_key)
    return sorted(locales, key=get_locale_key)


def get_locale_key(d):
    return d['locale']


def conj(a, b):
    res = {}
    res.update(a)
    res.update(b)
    return res


def uniq_by(collection, fn):
    res = []
    seen = set()

    for d in collection:
        k = fn(d)

        if k not in seen:
            res.append(d)
            seen.add(k)

    return res
