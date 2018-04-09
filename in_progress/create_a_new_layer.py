

# create a new layer, if doesn't exists:
def create_new_layer(a_glyph_name, layer_name):
    if not font.glyphs[a_glyph].layers[layer_name]:
        new_layer = GSLayer()
        new_layer.name = layer_name
        font.glyphs[a_glyph_name].layers.append(new_layer)
        print '"{0}" layer was created.'.format(new_layer.name)
    else:
        print 'The "{0}" layer already exists.'.format(new_layer.name)
