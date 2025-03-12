class dicttoxml(object):
    """docstring for dicttoxml."""
    def __init__(self):
        pass

    def xml(self, input):
        keys = list(input.keys())

        tags = []

        for key in keys:
            value = input[key] if input[key] is not None else ''

            if key == '#text':
                continue

            if key[0] == '@':
                continue

            if not isinstance(value, dict):
                tags.append(f'<{key}>{value}</{key}>')
                continue

            if isinstance(value, list):
                # Check if text present

                subtags = []
                for item in value:
                    subtags.append(self.xml(item))

                subtags = [f'\t{subtag}' for subtag in subtags]

                tags.extend(subtags)
                continue

            subkeys = list(value.keys())

            text = ''

            if '#text' in subkeys:
                text = value['#text']
                subkeys.remove('#text')

            attributes = ['']
            for subkey in subkeys:
                if subkey[0] == '@':
                    attributes.append(f'{subkey[1:]}="{value[subkey]}"')
                    subkeys.remove(subkey)

            attributes = ' '.join(attributes)

            if not subkeys:
                tags.append(f'<{key}{attributes}>{text}</{key}>')
                continue

            tags.append(f'<{key}{attributes}>{text}')
            tags.extend([f'\t{subtag}' for subtag in self.xml(value)])
            tags.append(f'</{key}>')

        return tags
