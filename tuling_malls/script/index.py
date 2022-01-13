from django.template import loader
def index():
    from goods.models import SKU,ContentCategory,Content
    from utils.skus import mianbaoxie, goods_channel, get_goods_specs
    from django.template import loader
    categories = goods_channel()
    content = ContentCategory.objects.all()
    contents = {}
    for i in content:
        print(i.id)
        contents[i.key] = Content.objects.filter(category_id=i.id, status=True).order_by('sequence')
    context = {
        'categories': categories,
        'contents': contents
    }
    index = loader.get_template('index.html')
    indexs = index.render(context)
    import os
    from tuling_malls import settings
        # file_path = os.path.join(os.path.dirname(settings.BASE_DIR), '?front_end_pc/goods/%s.html' % sku.id)
    paths = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
    with open(paths, 'w', encoding='utf8')as f:
        f.write(indexs)
