class RSSReaderService(object):
    def __init__(self, parsed_rss, fields: list = None):
        self.parsed_rss = parsed_rss
        self.attribute = 'entries'
        self.fields = ['link', 'title', 'published', 'author', 'summary'] if fields is None else fields

    def read_rss(self):
        list_of_parsed_rss_fields = []
        parsed_rss_attribute_list = self.parsed_rss.get(self.attribute)

        for parsed_rss_attribute in parsed_rss_attribute_list:
            parsed_rss_fields = {}
            for field in self.fields:
                parsed_rss_fields[field] = parsed_rss_attribute.get(field)
            list_of_parsed_rss_fields.append(parsed_rss_fields)
        return list_of_parsed_rss_fields
