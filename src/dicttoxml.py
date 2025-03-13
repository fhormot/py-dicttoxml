class dicttoxml(object):
    """docstring for dicttoxml."""
    def __init__(self):
        pass

    def xml_array(self, input):
        keys = list(input.keys())

        tags = []

        for key in keys:
            value = input[key] if input[key] is not None else ''

            tags.extend([f'{subtag}' for subtag in self.xml({key: value})])

        return tags

    def xml(self, input):
        keys = list(input.keys())

        tags = []

        for key in keys:
            value = input[key] if input[key] is not None else ''

            if key == '#text':
                continue

            if key[0] == '@':
                continue

            if isinstance(value, list):
                subtags = []
                for item in value:
                    subtags.extend(self.xml_array({key: item}))

                # subtags = [f'\t{subtag}' for subtag in subtags]

                tags.extend(subtags)
                continue

            if isinstance(value, dict):
                subkeys = list(value.keys())

                text = ''

                if '#text' in subkeys:
                    text = value['#text']
                    subkeys.remove('#text')

                attributes = ['']
                for subkey in list(value.keys()):
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

            if not isinstance(value, dict):
                tags.append(f'<{key}>{value}</{key}>')
                continue

        return tags

    def return_xml(self, input):
        return '<?xml version="1.0"?>\n'+'\n'.join(self.xml(input))