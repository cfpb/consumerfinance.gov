def first_site_for_page(page):
    for a in reversed(page.get_ancestors()):
        sites = a.sites_rooted_here.all()
        if len(sites) > 0:
            return sites.first()
