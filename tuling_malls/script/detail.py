from goods.models import SKU
from utils.skus import mianbaoxie,goods_channel,get_goods_specs
from django.template import loader
def detail(id):
    sku =SKU.objects.get(id=id)
    breadcrumb =mianbaoxie(sku.category_id)
    goods_specs =get_goods_specs(sku)
    categories = goods_channel()
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs
    }
    index=loader.get_template('detail.html')
    indexs=index.render(context)
    import os
    from tuling_malls import settings
    # file_path = os.path.join(os.path.dirname(settings.BASE_DIR), '?front_end_pc/goods/%s.html' % sku.id)
    paths = os.path.join(os.path.dirname(settings.BASE_DIR),'front_end_pc/goods/%s.html' % sku.id)
    with open(paths,'w',encoding='utf8')as f:
        f.write(indexs)
sku=SKU.objects.all()
for i in sku:
    detail(i.id)