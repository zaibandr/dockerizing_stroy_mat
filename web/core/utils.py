
def url_params_create(**kwargs):
    return '?{}'.format('&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
