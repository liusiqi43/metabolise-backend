import re
from unicodedata import normalize as _normalize
from pattern.en import singularize as _singularize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def normalize(word):
    if is_number(word):
        return float(word)
    word = re.sub(r'\([^)]*\)', '', word)
    word = re.sub(r',|\.|\?|!|:|;', ' ', word)
    word = _normalize('NFKD', word.decode('utf-8')).encode('ascii', 'ignore')
    return word.lower().strip()


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return unicode(delim.join(result))


_invalid_tokens = set([u'with', u'items', u'add', u'null', u'specialty',
                       u'your', u'all', u'and', u'or', u'the', u'be', u'to',
                       u'from', u'it', u'have'])


def is_token_valid(t):
    return t[1] == 'NN' and t[0] not in _invalid_tokens and 10 > len(
        t[0]) > 2 and t[0].isalpha()


def is_plural(token):
    singular_form = singularize(token)
    plural = True if token is not singular_form else False
    return plural, singular_form


def tokenize(*sentences):
    res = []
    for sentence in sentences:
        if not callable(getattr(sentence, 'split', None)):
            continue
        res.extend(sentence.split())
    return res


_blacklist = set(['slice', 'pasta', 'sundae', 'boneless'])
def singularize(s):
    if s in _blacklist:
        return s
    return _singularize(s)


_unit_mapping = {
    '#8 scoop': (4, 'cup'),
    '12oz oatmeal': (12, 'oz'),
    '4.5oz bagel': 'bagel',
    '5oz muffin': 'muffin',
    '5oz muffins': 'muffin',
    '8oz oatmeal': (8, 'oz'),
    'as prepared': 'serving',
    'big': 'large',
    'concrete serving': 'serving',
    'cups': 'cup',
    'ea': 'each',
    'eggs': 'egg',
    'entire plate': 'plate',
    'entr': 'entree',
    'extra large portion': 'large',
    'fl oz cup': 'fl oz',
    'fl oz. ladle': (4, 'fl oz'),
    'fl oz.': 'fl oz',
    'fl. oz': 'fl oz',
    'fl. oz.': 'fl oz',
    'fl.oz': 'fl oz',
    'fl.oz.': 'fl oz',
    'fluid ounce': 'fl oz',
    'fluid ounces': 'fl oz',
    'fluid oz.': 'fl oz',
    'flz': 'cup',
    'full dish': 'dish',
    'full order': 'order',
    'full salad': 'salad',
    'gm': 'g',
    'gms': 'g',
    'gram': 'g',
    'grams': 'g',
    'grand': 'grande',
    'half cup': (0.5, 'cup'),
    'half grinder': (0.5, 'grinder'),
    'half rack': (0.5, 'rack'),
    'half salad': (0.5, 'salad'),
    'half sandwich': (0.5, 'sandwich'),
    'half/mini': 'mini',
    'handful serving': 'handful',
    'kids tacos': 'kids taco',
    'large portion': 'large',
    'large size': 'large',
    'lbs': 'lb',
    'links': 'link',
    'medium portion': 'medium',
    'medium size': 'medium',
    'medium size': 'medium',
    'mini size': 'mini',
    'mini size': 'mini',
    'nachos': 'nacho',
    'ounce': 'oz',
    'ounce-weight': 'oz',
    'ounces': 'oz',
    'oz cup': 'fl oz',
    'oz.': 'oz',
    'pancakes': 'pancake',
    'pc': 'piece',
    'pc.': 'piece',
    'pcs': 'piece',
    'pieces': 'piece',
    'portion for 1 slice': 'slice',
    'quarter grinder': (0.25, 'grinder'),
    'roll-ups': 'roll-up',
    'sandwiches': 'sandwich',
    'scoops': 'scoop',
    'serv': 'serving',
    'servings': 'serving',
    'slice of 8': 'slice',
    'slices': 'slice',
    'small portion': 'small',
    'small serving': 'small',
    'small size': 'small',
    'standard portion size': 'portion',
    'standard portion': 'portion',
    'sticks': 'stick',
    'strips': 'strip',
    't': 'tsp',
    'tablespoon': 'tbsp',
    'tablespoons': 'tbsp',
    'taco sandwich': 'taco',
    'tacos': 'taco',
    'tall': 'tall cup',
    'tbl': 'tbsp',
    'tbl.': 'tbsp',
    'tbls': 'tbsp',
    'tbsp.': 'tbsp',
    'total meal': 'meal',
    'whole grinder': 'grinder',
    'whole grinder': 'grinder',
    'whole pizza': 'pizza',
    'whole wrap': 'wrap',
    'wings': 'wing',
}


def unit_normalization(qty, unit):
    mapped = _unit_mapping[unit] if unit in _unit_mapping else unit
    if isinstance(mapped, tuple):
        qty /= mapped[0]
        return qty, mapped[1]
    return qty, mapped
