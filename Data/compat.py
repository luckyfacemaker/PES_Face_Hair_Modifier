def link_alpha(material, source, destination):
    threshold = material.get('pes_alpha_clip_threshold')
    if threshold is not None:
        node = material.node_tree.nodes.get('PES Alpha Clip')
        if node is None:
            node = material.node_tree.nodes.new('ShaderNodeMath')
            node.name = 'PES Alpha Clip'
        node.operation = 'GREATER_THAN'
        node.inputs[1].default_value = max(0.0, threshold - 0.000001)
        material.node_tree.links.new(source, node.inputs[0])
        source = node.outputs[0]
    material.node_tree.links.new(source, destination)
