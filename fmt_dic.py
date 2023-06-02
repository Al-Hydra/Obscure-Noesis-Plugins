from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("HydraVision Obscure 2 Texture Container", ".dic")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)

    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data, NOE_BIGENDIAN)

    if bs.getSize() < 8:
        return 0
    
    elif bs.readUInt() == 0:
        return 0
    
    else:
        return 1

def dicRead(data):
    texList = []
    bs = NoeBitStream(data, NOE_BIGENDIAN)
    bs.seek(0, NOESEEK_ABS)
    
    TexturesCount = bs.readUInt()

    for i in range(TexturesCount):
        bs.seek(4, NOESEEK_REL)
        TextureName = noeStrFromBytes(bs.readBytes(bs.readUInt()))
        MipMapsCount = bs.readUInt()
        AlphaFlag = bs.readUInt()
        OneBitAlphaFlag = bs.readUInt()
        Width = bs.readUInt()
        Height = bs.readUInt()
        PixelFormat = bs.readUInt()

        MipMaps = []
        for i in range(MipMapsCount):
            MipMapSize = bs.readUInt()
            MipMapData = bs.readBytes(MipMapSize)
            MipMaps.append(MipMapData)
        
        if PixelFormat == 21:
            TextureData = rapi.imageDecodeRaw(MipMaps[0], Width, Height, "b8 g8 r8 a8")
            texList.append(NoeTexture(TextureName, Width, Height, TextureData, noesis.NOESISTEX_RGBA32))
        
        elif PixelFormat == 23:
            #B5G6R5
            TextureData = rapi.imageDecodeRaw(MipMaps[0], Width, Height, "b5 g6 r5")
            texList.append(NoeTexture(TextureName, Width, Height, TextureData, noesis.NOESISTEX_RGBA32))
        
        elif PixelFormat == 25:
            #B5G5R5A1
            TextureData = rapi.imageDecodeRaw(MipMaps[0], Width, Height, "b5 g5 r5 a1")
            texList.append(NoeTexture(TextureName, Width, Height, TextureData, noesis.NOESISTEX_RGBA32))
    return texList

def noepyLoadRGBA(data, texList):
    dic = dicRead(data)
    for tex in dic:
        texList.append(tex)
    
    return 1
