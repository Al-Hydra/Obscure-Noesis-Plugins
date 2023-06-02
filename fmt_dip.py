from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("HydraVision Obscure Texture Container", ".dip")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)

    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)

    if bs.getSize() < 8:
        return 0
    
    elif bs.readUInt64() == 0:
        return 0
    
    else:
        return 1

def dipRead(data):
    texList = []
    bs = NoeBitStream(data)
    bs.seek(4, NOESEEK_REL)
    
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


def noepyLoadRGBA(data, texList):
    dip = dipRead(data)
    if dip is None:
        return 0
    for tex in dip:
        texList.append(tex)
    return 1
