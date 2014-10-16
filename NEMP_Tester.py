# Change mod to the mod you want to test
mod = "ChickenChunks"




from commands.NEMP import NEMP_Class

NEM = NEMP_Class.NotEnoughClasses()

print getattr(NEM, NEM.mods[mod]["function"])(mod)