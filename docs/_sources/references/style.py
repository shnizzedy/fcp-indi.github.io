from collections import Counter
from pybtex.style.formatting import toplevel
from pybtex.style.formatting.plain import Style
from pybtex.style.labels import BaseLabelStyle
from pybtex.style.labels.alpha import _strip_nonalnum
from pybtex.style.names.lastfirst import NameStyle as LastFirst
from pybtex.style.sorting.none import SortingStyle as NoSort
from pybtex.style.template import field, href, join, optional, \
                                  optional_field, sentence, tag, words


date = words [ field('year'), optional_field('month') ]


class CPAC_DocsStyle(Style):
    def __init__(self, *args, **kwargs):
        super().__init__(
            abbreviate_names=True,
            name_style=LastFirst,
            sorting_style=NoSort,
            label_style=LabelStyle
        )

    def get_book_template(self, entry):
        template = toplevel [
            optional [ sentence [ self.format_names('author') ] ],
            optional [ sentence [ date ] ],
            optional [ sentence [ href [
                field('url'),
                optional [ tag('em') [ self.format_title(entry, 'title') ] ]
            ] ] ] if entry.fields.get('url') else optional [ sentence [
                tag('em') [ self.format_title(entry, 'title') ]
            ] ],
            optional [ sentence [
                join(sep=': ') [
                    optional_field('address'),
                    optional_field('publisher')
                ],
            ] ],
            sentence [ optional_field('note') ],
        ]
        return template

    def get_misc_template(self, entry):
        template = toplevel [
            optional [ sentence [ self.format_names('author') ] ],
            optional [ sentence [
                optional[ field('howpublished') ],
                optional[ date ],
            ] ],
            optional [ sentence [ join(sep=', ') [
                href [
                    optional_field('url'),
                    optional [
                        self.format_title(entry, 'title', as_sentence=False)
                    ]
                ] if entry.fields.get('url') else optional [
                    self.format_title(entry, 'title')
                ],
                optional [ tag('em') [
                    self.format_title(entry, 'journal')
                ] ],
            ] ] ],
            sentence [ optional_field('note') ],
        ]
        return template


class LabelStyle(BaseLabelStyle):
    def format_label(self, entry):
        label = '({})'.format(', '.join([
            self.format_label_names(entry.persons['author']),
            str(entry.fields['year'])
        ]))
        return label

    def format_label_names(self, persons):
        print(persons)
        numnames = len(persons)
        if numnames > 2:
            result = f'{_strip_nonalnum(persons[0].last_names)}, et al.'
        elif numnames == 2:
            result = ' & '.join([
                _strip_nonalnum(person.last_names) for person in persons
            ])
        else:
            result = _strip_nonalnum(persons[0].last_names)
        return result

    def format_labels(self, sorted_entries):
        labels = [self.format_label(entry) for entry in sorted_entries]
        count = Counter(labels)
        counted = Counter()
        for label in labels:
            if count[label] == 1:
                yield label
            else:
                yield label + chr(ord('a') + counted[label])
                counted.update([label])
