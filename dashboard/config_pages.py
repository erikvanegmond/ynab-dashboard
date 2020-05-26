from collections import OrderedDict

from layout.pages import main, sunburst, networth

config_pages = OrderedDict(
    [
        ('main_page', {
            'name': 'Home',
            'link': ['/main_page', '/main_page/', '/'],
            'body': main
        }),
        ('sunburst_page', {
            'name': 'Sunburst',
            'link': ['/sunburst', '/sunburst/', ],
            'body': sunburst
        }),
        ('networth', {
            'name': 'Networth',
            'link': ['/networth', '/networth/', ],
            'body': networth
        })
    ]
)
