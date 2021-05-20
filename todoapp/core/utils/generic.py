import urllib.parse as urlparse

def add_queries_to_url(url, **queries):
	# Split URL
	url_parts = list(urlparse.urlparse(url))
	current_qs = url_parts[4]
	qs_dict = dict(urlparse.parse_qsl(current_qs))
	# Update old queries with new ones
	qs_dict.update(queries)
	# Re-encode the URL
	url_parts[4] = urlparse.urlencode(qs_dict)
	new_url = urlparse.urlunparse(url_parts)
	return new_url