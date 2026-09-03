from pathlib import Path
import runpy
import re

# Reutiliza toda la capa Universal 1.3.1 y añade compensación de overscan para TV/TV Box.
runpy.run_path('scripts/customize_mi_youtube_131.py', run_name='__main__')

root = Path('MiYouTube-src')
res = root / 'app/src/main/res'

# Nueva versión 1.3.2
p = root / 'app/build.gradle.kts'
s = p.read_text(encoding='utf-8')
s = re.sub(
    r'versionCode\s*=\s*System\.getProperty\("versionCodeOverride"\)\?\.toInt\(\) \?: \d+',
    'versionCode = System.getProperty("versionCodeOverride")?.toInt() ?: 1320',
    s,
)
s = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.3.2"', s, count=1)
p.write_text(s, encoding='utf-8')

# Más margen estático en layouts nativos de TV.
for rel in ['layout-television/fragment_main.xml', 'layout-television/list_stream_item.xml']:
    path = res / rel
    text = path.read_text(encoding='utf-8')
    text = text.replace('android:paddingStart="32dp"', 'android:paddingStart="56dp"')
    text = text.replace('android:paddingEnd="32dp"', 'android:paddingEnd="56dp"')
    text = text.replace('android:layout_marginStart="28dp"', 'android:layout_marginStart="48dp"')
    text = text.replace('android:layout_marginEnd="28dp"', 'android:layout_marginEnd="48dp"')
    path.write_text(text, encoding='utf-8')

# Compensación dinámica para TV Box que no se identifican como Android TV.
# Si no hay pantalla táctil o Android reporta modo TV, se aplica un área segura
# proporcional al tamaño real de la pantalla. Esto evita que el borde izquierdo,
# derecho, superior o inferior quede fuera de la zona visible por overscan.
p = root / 'app/src/main/java/org/schabi/newpipe/MainActivity.java'
s = p.read_text(encoding='utf-8')

needle = '        setContentView(mainBinding.getRoot());\n'
replacement = needle + '        applyTelevisionSafeArea();\n'
if needle not in s:
    raise RuntimeError('No se encontró setContentView en MainActivity')
s = s.replace(needle, replacement, 1)

marker = '    @Override\n    protected void onPostCreate(final Bundle savedInstanceState) {'
method = '''    private void applyTelevisionSafeArea() {\n        final boolean noTouchscreen = !getPackageManager().hasSystemFeature(\n                PackageManager.FEATURE_TOUCHSCREEN);\n        final Object uiModeService = getSystemService(Context.UI_MODE_SERVICE);\n        final boolean televisionMode = uiModeService instanceof android.app.UiModeManager\n                && ((android.app.UiModeManager) uiModeService).getCurrentModeType()\n                == android.content.res.Configuration.UI_MODE_TYPE_TELEVISION;\n\n        if (!noTouchscreen && !televisionMode) {\n            return;\n        }\n\n        final View root = mainBinding.getRoot();\n        root.post(() -> {\n            final int width = root.getWidth();\n            final int height = root.getHeight();\n            if (width <= 0 || height <= 0) {\n                return;\n            }\n\n            final float density = getResources().getDisplayMetrics().density;\n            final int minHorizontal = Math.round(36 * density);\n            final int maxHorizontal = Math.round(96 * density);\n            final int minVertical = Math.round(20 * density);\n            final int maxVertical = Math.round(64 * density);\n\n            final int horizontalSafe = Math.max(minHorizontal,\n                    Math.min(maxHorizontal, Math.round(width * 0.055f)));\n            final int verticalSafe = Math.max(minVertical,\n                    Math.min(maxVertical, Math.round(height * 0.040f)));\n\n            root.setPadding(horizontalSafe, verticalSafe,\n                    horizontalSafe, verticalSafe);\n        });\n    }\n\n'''
if marker not in s:
    raise RuntimeError('No se encontró onPostCreate en MainActivity')
s = s.replace(marker, method + marker, 1)
p.write_text(s, encoding='utf-8')

# Nota de versión.
(root / 'MI-YOUTUBE-NOTICE.txt').write_text('''Mi YouTube 1.3.2 Universal TV Safe Area\nBasado en TeamNewPipe/NewPipe v0.29.0 y NewPipeExtractor.\nLicencia GPL-3.0-or-later.\nMantiene la interfaz Universal 1.3.1 y añade compensación dinámica de overscan para TV Box,\nAndroid TV y Google TV. El área segura se aplica cuando el dispositivo no tiene pantalla táctil\no cuando Android informa modo televisión. También aumenta los márgenes de los layouts TV.\nNo es una aplicación oficial de YouTube ni de NewPipe.\n''', encoding='utf-8')

print('Mi YouTube 1.3.2 Universal TV Safe Area personalizado')
