from fakepinterest.models import Fotos
fotos_do_usuario = Fotos.query.all()
print(fotos_do_usuario)  # Isso mostrará todas as fotos registradas