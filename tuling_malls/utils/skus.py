from goods.models import GoodsCategory,GoodsChannel
from collections import OrderedDict
def goods_channel():
    channe=GoodsChannel.objects.order_by('group_id','sequence')
    categories=OrderedDict()
    for channel in channe:
        category=GoodsCategory.objects.get(id=channel.category_id)
        group_id=channel.group_id
        # print(channel.url,channel.category_id)
        if  group_id not in categories:
            categories[group_id]={'channels':[],'sub_cats':[]}
        categories[group_id]['channels'].append({
            'id':category.id,
            'url':channel.url,
            'name':category.name
        })
        categorys=GoodsCategory.objects.filter(parent_id=channel.id)
        for sku in categorys:
            category = GoodsCategory.objects.filter(parent_id=sku.id)
            sub_cats=[]
            for skus in category:
                sub_cats.append({
                    'id':skus.id,
                    'name':skus.name
                })
            categories[group_id]['sub_cats'].append({
                'sub_cats':sub_cats,
                'name':sku.name
            })
    return categories
def mianbaoxie(id):
    dict={
        'cat1':'',
        'cat2': '',
        'cat3': '',
    }
    category=GoodsCategory.objects.get(id=id)
    if category.parent is None:
        dict['cat1']=category.name
    elif category.parent.parent is None:
        dict['cat1'] = category.parent.name
        dict['cat2']=category.name
    else:
        dict['cat3']=category.name
        dict['cat1'] = category.parent.parent.name
        dict['cat2'] = category.parent.name
    return dict
from goods.models import SKU
def get_goods_specs(sku):
    # 构建当前商品的规格键
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)

    # 获取当前商品的所有SKU
    skus = sku.spu.sku_set.all()
    # 构建不同规格参数（选项）的sku字典
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.specs.order_by('spec_id')
        # 用于形成规格参数-sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数-sku字典添加记录
        spec_sku_map[tuple(key)] = s.id

    # 以下代码为：在每个选项上绑定对应的sku_id值
    # 获取当前商品的规格信息
    goods_specs = sku.spu.specs.order_by('id')
    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(goods_specs):
        return
    for index, spec in enumerate(goods_specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = spec.options.all()
        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        spec.spec_options = spec_options

    return goods_specs