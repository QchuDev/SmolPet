import os
from pathlib import Path
import subprocess

def buscar_en_multiples_fuentes(lista_carpetas, max_fotos=10):
    # Usamos un set para evitar rutas duplicadas si una carpeta está dentro de otra
    rutas_encontradas = set()
    extensiones = {'.jpg', '.jpeg', '.png'}

    for carpeta in lista_carpetas:
        path_raiz = Path(carpeta).expanduser().resolve()
        
        if not path_raiz.exists():
            print(f"⚠️ Saltando: {carpeta} (No existe)")
            continue

        print(f"🔍 Buscando en: {path_raiz}")

        try:
            # Usamos rglob('*') para recorrer una sola vez y filtrar manualmente
            # Esto es MUCHO más rápido que rglob por cada extensión
            for archivo in path_raiz.rglob('*'):
                if len(rutas_encontradas) >= max_fotos:
                    return list(rutas_encontradas)

                # Verificamos si es un archivo y si su extensión nos sirve
                if archivo.is_file() and archivo.suffix.lower() in extensiones:
                    rutas_encontradas.add(str(archivo.absolute()))
                    
        except PermissionError:
            print(f"🚫 Permiso denegado en alguna subcarpeta de: {path_raiz}")
            continue
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            continue
                    
    return list(rutas_encontradas)

# --- CONFIGURACIÓN ---
fuentes = [
    "~/Desktop",        # Escritorio
    "~/Downloads",      # Descargas (Usar ~ es más seguro que C:/)
    "~/Pictures"        # Carpeta de imágenes
]

mis_10_imagenes = buscar_en_multiples_fuentes(fuentes, max_fotos=10)

print(f"\n✅ Total encontradas: {len(mis_10_imagenes)}")
for i, path in enumerate(mis_10_imagenes, 1):
    print(f"{i}. {path}")

fuentes = [
    "~/Desktop",        # Escritorio
    "~/Downloads",      # Descargas (Usar ~ es más seguro que C:/)
    "~/Pictures"        # Carpeta de imágenes
]
#mis_10_imagenes = images_search_testing.buscar_en_multiples_fuentes(fuentes, max_fotos=10)
#img_surface = pygame.image.load(mis_10_imagenes[2])
#SCREEN.blit(pygame.transform.scale(img_surface,(300,300)), (0, 0))