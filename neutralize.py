"""
Script para neutralizar el español en archivos Markdown.
Reemplaza conjugaciones de voseo argentino y modismos regionales
por español latinoamericano neutro y formal.

Uso:
    python3 neutralize.py <archivo.md>
    python3 neutralize.py clase_1/practica_django.md

Para procesar todos los .md de una carpeta:
    for f in *.md; do python3 neutralize.py "$f"; done
"""
import sys
import re
import os


def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"Archivo no encontrado: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        # ── Verbos en presente (voseo → tuteo) ──
        (r'\btenés\b', 'tienes'),
        (r'\bpodés\b', 'puedes'),
        (r'\bquerés\b', 'quieres'),
        (r'\bsabés\b', 'sabes'),
        (r'\bhacés\b', 'haces'),
        (r'\bdecís\b', 'dices'),
        (r'\bvenís\b', 'vienes'),
        (r'\bseguís\b', 'sigues'),
        (r'\bponés\b', 'pones'),
        (r'\bcreés\b', 'crees'),
        (r'\bleés\b', 'lees'),
        (r'\bentendés\b', 'entiendes'),
        (r'\bconocés\b', 'conoces'),
        (r'\bestás\b', 'estás'),

        # ── Imperativos (voseo → tuteo) ──
        (r'\bhacé\b', 'haz'),
        (r'\bponé\b', 'pon'),
        (r'\bdecí\b', 'di'),
        (r'\bvení\b', 'ven'),
        (r'\bseguí\b', 'sigue'),
        (r'\bmirá\b', 'mira'),
        (r'\bfijate\b', 'fíjate'),
        (r'\bacordate\b', 'acuérdate'),
        (r'\bolvidate\b', 'olvídate'),
        (r'\basegurate\b', 'asegúrate'),
        (r'\banotá\b', 'anota'),
        (r'\bbuscá\b', 'busca'),
        (r'\bcreá\b', 'crea'),
        (r'\babrí\b', 'abre'),
        (r'\bejecutá\b', 'ejecuta'),
        (r'\bnavegá\b', 'navega'),
        (r'\bprobá\b', 'prueba'),
        (r'\bcorré\b', 'corre'),
        (r'\brevisá\b', 'revisa'),
        (r'\bagregá\b', 'agrega'),
        (r'\bmodificá\b', 'modifica'),
        (r'\brenombrá\b', 'renombra'),
        (r'\bactualizá\b', 'actualiza'),
        (r'\bescribí\b', 'escribe'),
        (r'\bguardá\b', 'guarda'),
        (r'\bcargá\b', 'carga'),
        (r'\biniciá\b', 'inicia'),
        (r'\bverificá\b', 'verifica'),
        (r'\binstalá\b', 'instala'),
        (r'\brecordá\b', 'recuerda'),
        (r'\bentrá\b', 'entra'),
        (r'\bdejalo\b', 'déjalo'),
        (r'\bdescargalo\b', 'descárgalo'),
        (r'\blocalizá\b', 'localiza'),
        (r'\bvolvé\b', 'vuelve'),
        (r'\bbajá\b', 'baja'),
        (r'\btipear\b', 'escribir'),
        (r'\brepetila\b', 'repítela'),

        # ── Mayúsculas ──
        (r'\bTenés\b', 'Tienes'),
        (r'\bPodés\b', 'Puedes'),
        (r'\bQuerés\b', 'Quieres'),
        (r'\bSabés\b', 'Sabes'),
        (r'\bHacés\b', 'Haces'),
        (r'\bHacé\b', 'Haz'),
        (r'\bPoné\b', 'Pon'),
        (r'\bMirá\b', 'Mira'),
        (r'\bFijate\b', 'Fíjate'),
        (r'\bAsegurate\b', 'Asegúrate'),
        (r'\bAnotá\b', 'Anota'),
        (r'\bBuscá\b', 'Busca'),
        (r'\bCreá\b', 'Crea'),
        (r'\bAbrí\b', 'Abre'),
        (r'\bEjecutá\b', 'Ejecuta'),
        (r'\bNavegá\b', 'Navega'),
        (r'\bProbá\b', 'Prueba'),
        (r'\bCorré\b', 'Corre'),
        (r'\bRevisá\b', 'Revisa'),
        (r'\bAgregá\b', 'Agrega'),
        (r'\bModificá\b', 'Modifica'),
        (r'\bRenombrá\b', 'Renombra'),
        (r'\bActualizá\b', 'Actualiza'),
        (r'\bEscribí\b', 'Escribe'),
        (r'\bGuardá\b', 'Guarda'),
        (r'\bCargá\b', 'Carga'),
        (r'\bIniciá\b', 'Inicia'),
        (r'\bVerificá\b', 'Verifica'),
        (r'\bInstalá\b', 'Instala'),
        (r'\bRecordá\b', 'Recuerda'),
        (r'\bEntrá\b', 'Entra'),
        (r'\bLocalizá\b', 'Localiza'),
        (r'\bVolvé\b', 'Vuelve'),

        # ── Modismos y pronombres ──
        (r'\bacá\b', 'aquí'),
        (r'\bAcá\b', 'Aquí'),
        (r'\bVos\b', 'Tú'),
        (r'\bvos\b', 'tú'),
    ]

    new_content = content
    changes = 0
    for pattern, replacement in replacements:
        new_content, count = re.subn(pattern, replacement, new_content)
        changes += count

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Modificado ({changes} cambios): {filepath}")
    else:
        print(f"✔️  Sin cambios: {filepath}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 neutralize.py <archivo.md>")
        print("     python3 neutralize.py archivo1.md archivo2.md ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        process_file(filepath)
