from v1.models.base import CFGOVPage, RelatedPostsCategory


def run():
    for page in CFGOVPage.objects.all():
        sidefoot = page.sidefoot
        if sidefoot:
            stream_data = sidefoot.stream_data
            related_posts = filter(
                lambda item: item['type'] == 'related_posts',
                stream_data
            )
            if related_posts:
                cats = related_posts[0]['value']['specific_categories']
                for cat in cats:
                    if not cat:
                        continue
                    if cat == 'Policy &amp; Compliance':
                        new_cat = RelatedPostsCategory(
                            page=page,
                            name='policy-compliance'
                        )
                        new_cat.save()
                    elif cat == 'Info for Consumers':
                        new_cat = RelatedPostsCategory(
                            page=page,
                            name='info-for-consumers'
                        )
                        new_cat.save()
                    elif cat == 'Data, Research &amp; Reports':
                        new_cat = RelatedPostsCategory(
                            page=page,
                            name='data-research-reports'
                        )
                        new_cat.save()
                    elif cat == 'At the CFPB':
                        new_cat = RelatedPostsCategory(
                            page=page,
                            name='at-the-cfpb'
                        )
                        new_cat.save()
                    elif cat == 'Press Release':
                        new_cat = RelatedPostsCategory(
                            page=page,
                            name='press-release'
                        )
                        new_cat.save()
        for cat in page.categories.get_object_list():
            if cat.name == 'policy_compliance':
                cat.name = 'policy-compliance'
                cat.save()
