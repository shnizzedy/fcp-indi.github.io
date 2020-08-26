from pybtex.style.formatting import toplevel
from pybtex.style.formatting.unsrtalpha import Style as UnsrtAlphaStyle
from pybtex.style.names.lastfirst import NameStyle as LastFirst
from pybtex.style.template import field, href, optional, optional_field, \
                                  sentence, tag, words


date = words [field('year'), optional_field('month')]


class CPAC_DocsStyle(UnsrtAlphaStyle):
    def __init__(self, *args, **kwargs):
        super().__init__(abbreviate_names=True, name_style=LastFirst)

    def get_misc_template(self, entry):
        template = toplevel [
            optional[ sentence [self.format_names('author')] ],
            sentence[
                optional[ field('howpublished') ],
                optional[ date ],
            ],
            optional[ href [
                optional_field('url'),
                optional[ self.format_title(entry, 'title') ]
            ] ],
            optional [ tag('em') [sentence [ optional_field('journal') ] ] ],
            sentence [ optional_field('note') ],
        ]
        return template