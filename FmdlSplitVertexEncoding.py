from . import FmdlFile

def topologicalKey(encodedVertex, vertexFields):
	if vertexFields.hasBoneMapping:
		return (encodedVertex.position, tuple(encodedVertex.boneMapping))
	else:
		return encodedVertex.position

def nontopologicalEncoding(encodedVertex, vertexFields):
	encoding = bytearray()
	if vertexFields.hasNormal:
		encoding += encodedVertex.normal
	if vertexFields.hasColor:
		encoding += encodedVertex.color
	for i in range(4):
		if vertexFields.uvCount > i:
			encoding += encodedVertex.uv[i]
	if vertexFields.hasTangent:
		encoding += encodedVertex.tangent
	return bytes(encoding)

def replaceFaceVertices(faces, replacedVertices):
	return [
	 FmdlFile.FmdlFile.Face(*[
	  (replacedVertices[vertex] if vertex in replacedVertices else vertex) for vertex in face.vertices
	 ]) for face in faces
	]

def encodeMeshVertexLoopPreservation(mesh):

	topologicallyEquivalentVertices = {}

	splitVertices = {}
 
	for encodedVertex in mesh.vertexEncoding:
		key = topologicalKey(encodedVertex, mesh.vertexFields)
  
		if encodedVertex.vertex.position not in splitVertices:
			splitVertices[encodedVertex.vertex.position] = []
   
			if key not in topologicallyEquivalentVertices:
				topologicallyEquivalentVertices[key] = []
			topologicallyEquivalentVertices[key].append(encodedVertex.vertex.position)
		splitVertices[encodedVertex.vertex.position].append(encodedVertex)

	replacedVertices = {}
	for key in splitVertices:
		loops = {}
		for encodedVertex in splitVertices[key]:
			encoding = nontopologicalEncoding(encodedVertex, mesh.vertexFields)
			if encoding in loops:
				replacedVertices[encodedVertex.vertex] = loops[encoding].vertex
			else:
				loops[encoding] = encodedVertex
		splitVertices[key] = [loops[encoding] for encoding in sorted(loops.keys())]

	for (key, positions) in topologicallyEquivalentVertices.items():
		topologicallyEquivalentVertices[key] = sorted(positions, reverse = True, key = (
		 lambda position : nontopologicalEncoding(splitVertices[position][0], mesh.vertexFields)
		))
 
	encodedVertices = []
	addedTopologicalKeys = set()
	for encodedVertex in mesh.vertexEncoding:
		key = topologicalKey(encodedVertex, mesh.vertexFields)
		if key not in addedTopologicalKeys:
			addedTopologicalKeys.add(key)
   
			for position in topologicallyEquivalentVertices[key]:
				encodedVertices += splitVertices[position]
 
	output = FmdlFile.FmdlFile.Mesh()
	output.boneGroup = mesh.boneGroup
	output.materialInstance = mesh.materialInstance
	output.alphaEnum = mesh.alphaEnum
	output.shadowEnum = mesh.shadowEnum
	output.vertexFields = mesh.vertexFields
	output.vertices = [encodedVertex.vertex for encodedVertex in encodedVertices]
	output.faces = replaceFaceVertices(mesh.faces, replacedVertices)
	output.vertexEncoding = encodedVertices
	output.extensionHeaders = mesh.extensionHeaders.copy()
 
	return output

def encodeFmdlVertexLoopPreservation(fmdl):
	fmdl.precomputeVertexEncoding()
 
	output = FmdlFile.FmdlFile()
	output.bones = fmdl.bones
	output.materialInstances = fmdl.materialInstances
	output.meshes = []
	meshMap = {}
	for mesh in fmdl.meshes:
		encodedMesh = encodeMeshVertexLoopPreservation(mesh)
		output.meshes.append(encodedMesh)
		meshMap[mesh] = encodedMesh
	output.meshGroups = []
	meshGroupMap = {}
	for meshGroup in fmdl.meshGroups:
		encodedMeshGroup = FmdlFile.FmdlFile.MeshGroup()
		output.meshGroups.append(encodedMeshGroup)
		meshGroupMap[meshGroup] = encodedMeshGroup
	for meshGroup in fmdl.meshGroups:
		encodedMeshGroup = meshGroupMap[meshGroup]
		encodedMeshGroup.name = meshGroup.name
		encodedMeshGroup.boundingBox = meshGroup.boundingBox
		encodedMeshGroup.visible = meshGroup.visible
		if meshGroup.parent == None:
			encodedMeshGroup.parent = None
		else:
			encodedMeshGroup.parent = meshGroupMap[meshGroup.parent]
		encodedMeshGroup.children = []
		for child in meshGroup.children:
			encodedMeshGroup.children.append(meshGroupMap[child])
		encodedMeshGroup.meshes = []
		for mesh in meshGroup.meshes:
			encodedMeshGroup.meshes.append(meshMap[mesh])
	output.extensionHeaders = {}
	for (key, value) in fmdl.extensionHeaders.items():
		output.extensionHeaders[key] = value[:]
	if 'X-FMDL-Extensions' not in output.extensionHeaders:
		output.extensionHeaders['X-FMDL-Extensions'] = []
	output.extensionHeaders['X-FMDL-Extensions'].append("vertex-loop-preservation")
	return output

def decodeMeshVertexLoopPreservation(mesh):
	vertexEncoding = []
	vertices = []
	replacedVertices = {}
 
	previousEncodedVertex = None
	for encodedVertex in mesh.vertexEncoding:
		if (
		        previousEncodedVertex != None
		 and    topologicalKey(encodedVertex, mesh.vertexFields)
		     == topologicalKey(previousEncodedVertex, mesh.vertexFields)
		 and    nontopologicalEncoding(previousEncodedVertex, mesh.vertexFields)
		     <  nontopologicalEncoding(encodedVertex, mesh.vertexFields)
		):
			vertex = FmdlFile.FmdlFile.Vertex()
			vertex.position = previousEncodedVertex.vertex.position
			vertex.normal = encodedVertex.vertex.normal
			vertex.tangent = encodedVertex.vertex.tangent
			vertex.color = encodedVertex.vertex.color
			vertex.boneMapping = previousEncodedVertex.vertex.boneMapping
			vertex.uv = encodedVertex.vertex.uv[:]
   
			encoding = FmdlFile.FmdlFile.VertexEncoding()
			encoding.vertex = vertex
			encoding.position = encodedVertex.position
			encoding.normal = encodedVertex.normal
			encoding.tangent = encodedVertex.tangent
			encoding.color = encodedVertex.color
			encoding.boneMapping = encodedVertex.boneMapping
			encoding.uv = encodedVertex.uv[:]
   
			vertexEncoding.append(encoding)
			vertices.append(vertex)
			replacedVertices[encodedVertex.vertex] = vertex
			previousEncodedVertex = encoding
		else:
			vertexEncoding.append(encodedVertex)
			vertices.append(encodedVertex.vertex)
			previousEncodedVertex = encodedVertex
 
	output = FmdlFile.FmdlFile.Mesh()
	output.boneGroup = mesh.boneGroup
	output.materialInstance = mesh.materialInstance
	output.alphaEnum = mesh.alphaEnum
	output.shadowEnum = mesh.shadowEnum
	output.vertexFields = mesh.vertexFields
	output.vertices = vertices
	output.faces = replaceFaceVertices(mesh.faces, replacedVertices)
	output.vertexEncoding = vertexEncoding
	output.extensionHeaders = mesh.extensionHeaders.copy()
 
	return output

def decodeFmdlVertexLoopPreservation(fmdl):
	if fmdl.extensionHeaders == None or "vertex-loop-preservation" not in fmdl.extensionHeaders['x-fmdl-extensions']:
		return fmdl
 
	output = FmdlFile.FmdlFile()
	output.bones = fmdl.bones
	output.materialInstances = fmdl.materialInstances
	output.meshes = []
	meshMap = {}
	for mesh in fmdl.meshes:
		encodedMesh = decodeMeshVertexLoopPreservation(mesh)
		output.meshes.append(encodedMesh)
		meshMap[mesh] = encodedMesh
	output.meshGroups = []
	meshGroupMap = {}
	for meshGroup in fmdl.meshGroups:
		encodedMeshGroup = FmdlFile.FmdlFile.MeshGroup()
		output.meshGroups.append(encodedMeshGroup)
		meshGroupMap[meshGroup] = encodedMeshGroup
	for meshGroup in fmdl.meshGroups:
		encodedMeshGroup = meshGroupMap[meshGroup]
		encodedMeshGroup.name = meshGroup.name
		encodedMeshGroup.boundingBox = meshGroup.boundingBox
		encodedMeshGroup.visible = meshGroup.visible
		if meshGroup.parent == None:
			encodedMeshGroup.parent = None
		else:
			encodedMeshGroup.parent = meshGroupMap[meshGroup.parent]
		encodedMeshGroup.children = []
		for child in meshGroup.children:
			encodedMeshGroup.children.append(meshGroupMap[child])
		encodedMeshGroup.meshes = []
		for mesh in meshGroup.meshes:
			encodedMeshGroup.meshes.append(meshMap[mesh])
	return output
