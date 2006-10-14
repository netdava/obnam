import wibbrlib.cmp


class Mappings:

    def __init__(self):
        self.dict = {}
        self.new_keys = {}


def create():
    """Create a new object ID to block ID mapping"""
    return Mappings()


def count(mapping):
    """Return the number of mappings in 'mapping'"""
    return len(mapping.dict.keys())


def add(mapping, object_id, block_id):
    """Add a mapping from object_id to block_id"""
    _add_old(mapping, object_id, block_id)
    if object_id not in mapping.new_keys:
        mapping.new_keys[object_id] = 1


def _add_old(mapping, object_id, block_id):
    """Add a mapping from object_id to block_id"""
    if object_id in mapping.dict:
        mapping.dict[object_id].append(block_id)
    else:
        mapping.dict[object_id] = [block_id]


def get(mapping, object_id):
    """Return the list of blocks, in order, that contain parts of an object"""
    return mapping.dict.get(object_id, None)


def get_new(mapping):
    """Return list of new mappings"""
    return mapping.new_keys.keys()


def reset_new(mapping):
    """Reset list of new mappings"""
    mapping.new_keys = {}


def encode_new(mapping):
    """Return a list of encoded components for the new mappings"""
    list = []
    for key in get_new(mapping):
        objref = wibbrlib.cmp.create(wibbrlib.cmp.CMP_OBJREF, key)
        blockrefs = mapping.dict[key]
        blockrefs = [wibbrlib.cmp.create(
                        wibbrlib.cmp.CMP_BLOCKREF, x) 
                     for x in blockrefs]
        component = wibbrlib.cmp.create(wibbrlib.cmp.CMP_OBJMAP, 
                        [objref] + blockrefs)
        component = wibbrlib.cmp.encode(component)
        list.append(component)
    return list


def encode_new_to_block(mapping, block_id):
    """Encode new mappings into a block"""
    c = wibbrlib.cmp.create(wibbrlib.cmp.CMP_BLKID, block_id)
    list = encode_new(mapping)
    block = "".join([wibbrlib.cmp.encode(c)] + list)
    return block


def decode_block(mapping, mapping_block):
    """Decode a block with mappings, add them to mapping object"""
    list = wibbrlib.cmp.decode_all(mapping_block, 0)
    maps = wibbrlib.cmp.find_by_type(list, wibbrlib.cmp.CMP_OBJMAP)
    for map in maps:
        subs = wibbrlib.cmp.get_subcomponents(map)
        assert len(subs) == 2
        object_id = wibbrlib.cmp.first_string_by_type(subs, 
                                               wibbrlib.cmp.CMP_OBJREF)
        block_ids = wibbrlib.cmp.find_strings_by_type(subs, 
                                           wibbrlib.cmp.CMP_BLOCKREF)
        if object_id and block_ids:
            for block_id in block_ids:
                _add_old(mapping, object_id, block_id)
